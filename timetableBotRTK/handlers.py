import sys
import asyncio
import json
import datetime
from aiogram import Router, F
from aiogram.types import message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


ro = Router(name=__name__)

class addadmin_state(StatesGroup):
    username = State()

class rmadmin_state(StatesGroup):
    username = State()

choose_group = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='выбрать группу', callback_data='choose_group')]])
groups = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='С1-23', callback_data='С1-23'),InlineKeyboardButton(text='С1-22', callback_data='С1-22'), InlineKeyboardButton(text='ИВ1_22_1', callback_data='ИВ1_22_1')],
                                               [InlineKeyboardButton(text='ИВ1_22_2', callback_data='ИВ1_22_2'),InlineKeyboardButton(text='ИВ1_23_1', callback_data='ИВ1_23_1'), InlineKeyboardButton(text='ИВ1_23_2', callback_data='ИВ1_23_2')],
                                               [InlineKeyboardButton(text='ИВ1К_22', callback_data='ИВ1К_22'),InlineKeyboardButton(text='ИВ2_22', callback_data='ИВ2_22'), InlineKeyboardButton(text='ИП1_22', callback_data='ИП1_22')],
                                               [InlineKeyboardButton(text='ИП1_23', callback_data='ИП1_23'),InlineKeyboardButton(text='ИП2_23', callback_data='ИП2_23'), InlineKeyboardButton(text='ИП2К_22', callback_data='ИП2К_22')],
                                               [InlineKeyboardButton(text='М1_22_1', callback_data='М1_22_1'),InlineKeyboardButton(text='М1_22_2', callback_data='М1_22_2'), InlineKeyboardButton(text='М1_23_1', callback_data='М1_23_1')],
                                               [InlineKeyboardButton(text='М1_23_2', callback_data='М1_23_2'),InlineKeyboardButton(text='М1_23_3', callback_data='М1_23_3'), InlineKeyboardButton(text='М2_23', callback_data='М2_23')],
                                               [InlineKeyboardButton(text='МТ1_22', callback_data='МТ1_22'),InlineKeyboardButton(text='МТ1_23', callback_data='МТ1_23'), InlineKeyboardButton(text='Н1_22', callback_data='Н1_22')],
                                               [InlineKeyboardButton(text='Р2_23', callback_data='Р2_23')]
                                               ])


#func____________________________________________________________________________
def is_admin(id):
    with open('users.json', 'r') as f:
        data = json.load(f)
    return data[str(id)]['admin']


def get_data_of_user(chat_id):
    with open('users.json', 'r') as f:
        data = json.load(f)
    return data[str(chat_id)] 


def create_settings_keyboard(chat_id):
    try:
        user = get_data_of_user(chat_id)
        return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'уведомление каждый урок: {convert_bool(user["everylesson"])}', callback_data='everylesson')],
                [InlineKeyboardButton(text=f'уведомление об изменениях: {convert_bool(user["changes"])}', callback_data='changes')]
                ])
    except KeyError:
        return False

def get_day(day:int, group:str):
    with open(f'groups/{group}.json', 'r') as f:
        data = json.load(f)
    return data[day]


def get_next_week_day(day:int, group:str):
    with open(f'next_week_groups/{group}.json', 'r') as f:
        data = json.load(f)
    return data[day]


def get_group(id:int):
    with open('users.json', 'r') as f:
        data = json.load(f)
    data = data.get(f'{id}')
    if data:
        return data['group']
    else:
        return None


def beautiful_day(day:list):
    text = ''
    for lesson in day:
        if len(lesson[1]) > 1:
            text += f'{lesson[0]}.   {lesson[1]}   {lesson[2]}   {lesson[4]}\n'
    return text


def convert_bool(bool):
    if bool:
        return 'Вкл.'
    else:
        return 'Выкл.'


def adduser(chat_id: int, group: str, username:str):
    with open('users.json', 'r') as f:
        data = json.load(f)
    try:
        if is_admin(chat_id):
            admin = True
    except:
        admin = False
    data.update({f'{chat_id}': {
        'everyday': False,
        'everylesson': False,
        'changes': False,
        'group': group,
        'admin': admin,
        'username': username
    }})
    with open('users.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def change_settings(chat_id:int, sitting:str):
    with open('users.json', 'r') as f:
        data = json.load(f)
    data[f'{chat_id}'][sitting] = not data[f'{chat_id}'][sitting]
    with open('users.json', 'w') as f:
        json.dump(data, f)


def change_admin(username:str, is_admin:bool):
    with open('users.json', 'r') as f:
        data = json.load(f)
    for id in data.keys():
        if data[str(id)]['username'] == username:
            data[str(id)]['admin'] = is_admin
            with open('users.json', 'w') as f:
                json.dump(data, f)
            return True
    return False





#callbacks________________________________________________________________________
@ro.callback_query(lambda c: c.data == 'current_monday')
async def current_monday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(0, group)
        text = beautiful_day(day)
        await callback_query.answer('понедельник')
        await callback_query.message.edit_text(f'расписание на *понедельник* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'current_tuesday')
async def current_tuesday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(1, group)
        text = beautiful_day(day)
        await callback_query.answer('вторник')
        await callback_query.message.edit_text(f'расписание на *вторник* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'current_wednesday')
async def current_wednesday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(2, group)
        text = beautiful_day(day)
        await callback_query.answer('среда')
        await callback_query.message.edit_text(f'расписание на *среду* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'current_thursday')
async def current_thursday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(3, group)
        text = beautiful_day(day)
        await callback_query.answer('четверг')
        await callback_query.message.edit_text(f'расписание на *четверг* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'current_friday')
async def current_friday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(4, group)
        text = beautiful_day(day)
        await callback_query.answer('пятница')
        await callback_query.message.edit_text(f'расписание на *пятницу* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'current_saturday')
async def current_saturday(callback_query: CallbackQuery):
    back_current_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_current_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(5, group)
        text = beautiful_day(day)
        await callback_query.answer('суббота')
        await callback_query.message.edit_text(f'расписание на *субботу* для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_current_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'back_current_week')
async def back_current_week(callback_query: CallbackQuery):
    current_week_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='понедельник', callback_data='current_monday'), InlineKeyboardButton(text='вторник', callback_data='current_tuesday')],
    [InlineKeyboardButton(text='среда', callback_data='current_wednesday'), InlineKeyboardButton(text='четверг', callback_data='current_thursday')],
    [InlineKeyboardButton(text='пятница', callback_data='current_friday'), InlineKeyboardButton(text='суббота', callback_data='current_saturday')]
    ])
    await callback_query.message.edit_text('расписание какого дня недели вам нужно?', reply_markup=current_week_kb)


@ro.callback_query(lambda c: c.data == 'next_monday')
async def next_monday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(0, group)
        text = beautiful_day(day)
        await callback_query.answer('понедельник')
        await callback_query.message.edit_text(f'расписание на *понедельник* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'next_tuesday')
async def next_tuesday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(1, group)
        text = beautiful_day(day)
        await callback_query.answer('вторник')
        await callback_query.message.edit_text(f'расписание на *вторник* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'next_wednesday')
async def next_wednesday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(2, group)
        text = beautiful_day(day)
        await callback_query.answer('среда')
        await callback_query.message.edit_text(f'расписание на *среду* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'next_thursday')
async def next_thursday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(3, group)
        text = beautiful_day(day)
        await callback_query.answer('четверг')
        await callback_query.message.edit_text(f'расписание на *четверг* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'next_friday')
async def next_friday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(4, group)
        text = beautiful_day(day)
        await callback_query.answer('пятница')
        await callback_query.message.edit_text(f'расписание на *пятницу* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'next_saturday')
async def next_saturday(callback_query: CallbackQuery):
    back_next_week = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️назад', callback_data='back_next_week')]])
    group = get_group(callback_query.message.chat.id)
    if group:
        day = get_day(5, group)
        text = beautiful_day(day)
        await callback_query.answer('суббота')
        await callback_query.message.edit_text(f'расписание на *субботу* следующей недели для группы *{group}*:\n\n{text}', parse_mode='Markdown', reply_markup=back_next_week)
    else:
        await callback_query.message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.callback_query(lambda c: c.data == 'back_next_week')
async def back_next_week(callback_query: CallbackQuery):
    next_week_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='понедельник', callback_data='next_monday'), InlineKeyboardButton(text='вторник', callback_data='next_tuesday')],
    [InlineKeyboardButton(text='среда', callback_data='next_wednesday'), InlineKeyboardButton(text='четверг', callback_data='next_thursday')],
    [InlineKeyboardButton(text='пятница', callback_data='next_friday'), InlineKeyboardButton(text='суббота', callback_data='next_saturday')]
    ])
    await callback_query.message.edit_text('расписание какого дня следующей недели вам нужно?', reply_markup=next_week_kb)


@ro.callback_query(lambda c: c.data == 'choose_group')
async def choose_g(callback_query: CallbackQuery):
    await callback_query.message.edit_text('выберите группу:', reply_markup=groups)


@ro.callback_query(lambda c: c.data == 'С1-23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *С1-23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'С1_23', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'С1-22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *С1-22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'С1_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ1_22_1')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ1_22_1*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ1_22_1', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ1_22_2')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ1_22_2*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ1_22_2', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ1_23_1')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ1_23_1*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ1_23_1', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ1_23_2')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ1_23_2*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ1_23_2', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ1К_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ1К_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ1К_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИВ2_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИВ2_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИВ2_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИП1_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИП1_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИП1_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИП1_23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИП1_23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИП1_23', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИП2_23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИП2_23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИП2_23', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'ИП2К_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *ИП2К_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'ИП2К_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М1_22_1')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М1_22_1*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М1_22_1', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М1_22_2')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М1_22_2*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М1_22_2', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М1_23_1')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М1_23_1*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М1_23_1', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М1_23_2')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М1_23_2*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М1_23_2', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М1_23_3')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М1_23_3*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М1_23_3', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'М2_23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *М2_23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'М2_23', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'МТ1_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *МТ1_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'МТ1_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'МТ1_23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *МТ1_23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'МТ1_23', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'Н1_22')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *Н1_22*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'Н1_22', callback_query.from_user.username)


@ro.callback_query(lambda c: c.data == 'Р2_23')
async def С1_23(callback_query: CallbackQuery):
    await callback_query.answer('Успешно!')
    await callback_query.message.edit_text('вы закреплены за группой *Р2_23*. По умолчанию все уведомления выключены. Если вы хотите настроить уведомления используйте комманду   /settings\n🟡 - замена', parse_mode="Markdown")
    adduser(callback_query.message.chat.id, 'Р2_23', callback_query.from_user.username)




@ro.callback_query(lambda c: c.data == 'everyday')
async def choose_everyday(callback_query: CallbackQuery):
    change_settings(callback_query.message.chat.id, 'everyday')
    keyboard = create_settings_keyboard(callback_query.message.chat.id)
    await callback_query.message.edit_text('ваши настройки уведомлений:', reply_markup=keyboard, parse_mode="Markdown")


@ro.callback_query(lambda c: c.data == 'everylesson')
async def choose_everyday(callback_query: CallbackQuery):
    change_settings(callback_query.message.chat.id, 'everylesson')
    keyboard = create_settings_keyboard(callback_query.message.chat.id)
    await callback_query.message.edit_text('ваши настройки уведомлений:', reply_markup=keyboard, parse_mode="Markdown")


@ro.callback_query(lambda c: c.data == 'changes')
async def choose_everyday(callback_query: CallbackQuery):
    change_settings(callback_query.message.chat.id, 'changes')
    keyboard = create_settings_keyboard(callback_query.message.chat.id)
    await callback_query.message.edit_text('ваши настройки уведомлений:', reply_markup=keyboard, parse_mode="Markdown")




#dispatchers_______________________________________________________________________
@ro.message(CommandStart())
async def start(message: message):
    await message.answer('Привет! это бот для удобного просмотра расписания *РТК*', reply_markup=choose_group, parse_mode='Markdown')


@ro.message(Command('settings'))
async def settings(message: message):
    keyboard = create_settings_keyboard(message.chat.id)
    if keyboard:
        await message.answer('ваши настройки уведомлений:', reply_markup=keyboard)
    else:
        await message.answer('вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.message(Command('lessons_now'))
async def lessons_now(message: message):
    time = datetime.datetime.now()
    day = datetime.datetime.weekday(time)
    group = get_group(message.chat.id)
    if group:
        lessons = get_day(day, group)
        day = beautiful_day(lessons)
        if len(day) > 1:
            await message.answer(f'*актуальное расписание для группы {group} на сегодня:*\n{day}', parse_mode='Markdown')
        else:
            await message.answer(f'уроков для группы {group} на завтра нет!')
    else:
        await message.answer(f'вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start')


@ro.message(Command('lessons_tomorrow'))
async def lessons_tomorrow(message: message):
    time = datetime.datetime.now()
    day = datetime.datetime.weekday(time) + 1
    if day == 7:
        day = 0 
    group = get_group(message.chat.id)
    if group:
        lessons = get_day(day, group)
        day = beautiful_day(lessons)
        if len(day) > 1:
            await message.answer(f'*актуальное расписание для группы {group} на завтра:*\n{day}', parse_mode='Markdown')
        else:
            await message.answer(f'уроков для группы {groups} на завтра нет!')
    else:
        await message.answer(f'вы ещё не зарегестрированы! Чтобы зарегистрироваться используйте комманду /start', parse_mode='Markdown')


@ro.message(Command('current_week'))
async def current_week(message:message):
    current_week_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='понедельник', callback_data='current_monday'), InlineKeyboardButton(text='вторник', callback_data='current_tuesday')],
    [InlineKeyboardButton(text='среда', callback_data='current_wednesday'), InlineKeyboardButton(text='четверг', callback_data='current_thursday')],
    [InlineKeyboardButton(text='пятница', callback_data='current_friday'), InlineKeyboardButton(text='суббота', callback_data='current_saturday')]
    ])
    await message.answer(f'расписание какого дня этой недели вам нужно?', reply_markup=current_week_kb)


@ro.message(Command('next_week'))
async def next_week(message:message):
    next_week_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='понедельник', callback_data='next_monday'), InlineKeyboardButton(text='вторник', callback_data='next_tuesday')],
    [InlineKeyboardButton(text='среда', callback_data='next_wednesday'), InlineKeyboardButton(text='четверг', callback_data='next_thursday')],
    [InlineKeyboardButton(text='пятница', callback_data='next_friday'), InlineKeyboardButton(text='суббота', callback_data='next_saturday')]
    ])
    await message.answer(f'расписание какого дня следующей недели вам нужно?', reply_markup=next_week_kb)


@ro.message(Command('crash'))
async def crash(message:message):
    if is_admin(message.chat.id):
        print((1000 - 7) / 0)
    else:
        await message.answer('вы не админ')


@ro.message(Command('addadmin'))
async def addadmin(message:message, state:FSMContext):
    if is_admin(message.chat.id):
        await state.set_state(addadmin_state.username)
        await message.answer('отправте username (без @)')
    else:
        await message.answer('вы не админ')


@ro.message(addadmin_state.username)
async def addadmin_username(message:message, state:FSMContext):
    await state.update_data(username=message.text)
    data = await state.get_data()
    is_correct = change_admin(data['username'], True)
    if is_correct:
        await message.answer(f'пользователь {data['username']} назначен админом')
    else:
        await message.answer('пользователь не найден')
    await state.clear()


@ro.message(Command('rmadmin'))
async def rmadmin(message:message, state:FSMContext):
    if is_admin(message.chat.id):
        await state.set_state(rmadmin_state.username)
        await message.answer('отправте username (без @)')
    else:
        await message.answer('вы не админ')


@ro.message(rmadmin_state.username)
async def rmadmin_username(message:message, state:FSMContext):
    await state.update_data(username=message.text)
    data = await state.get_data()
    is_correct = change_admin(data['username'], False)
    if is_correct:
        await message.answer(f'пользователь {data['username']} теперь не админ')
    else:
        await message.answer('пользователь не найден')
    await state.clear()
