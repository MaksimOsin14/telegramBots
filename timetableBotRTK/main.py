import asyncio
import json
import myparser
import datetime
import handlers
from handlers import ro
from aiogram import F, Bot, Dispatcher
from aiogram.types import message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

#paste your bot token here
bot_token = ''

#consts__________________________________________________________________________
bot = Bot(token='bot_token')
dp = Dispatcher()
С1_23 = myparser.current_parser('С1_23', 'http://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=61&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ1_22_1 = myparser.current_parser('ИВ1_22_1', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=32&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ1_22_2 = myparser.current_parser('ИВ1_22_2', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=33&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ1_23_1 = myparser.current_parser('ИВ1_23_1', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=67&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ1_23_2 = myparser.current_parser('ИВ1_23_2', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=68&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ1К_22 = myparser.current_parser('ИВ1К_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=34&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИВ2_22 = myparser.current_parser('ИВ2_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=35&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИП1_22 = myparser.current_parser('ИП1_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=36&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИП1_23 = myparser.current_parser('ИП1_23', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=69&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИП2_23 = myparser.current_parser('ИП2_23', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=70&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
ИП2К_22 = myparser.current_parser('ИП2К_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=37&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М1_22_1 = myparser.current_parser('М1_22_1', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=27&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М1_22_2 = myparser.current_parser('М1_22_2', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=28&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М1_23_1 = myparser.current_parser('М1_23_1', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=63&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М1_23_2 = myparser.current_parser('М1_23_2', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=64&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М1_23_3 = myparser.current_parser('М1_23_3', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=65&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
М2_23 = myparser.current_parser('М2_23', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=60&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
МТ1_22 = myparser.current_parser('МТ1_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=38&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
МТ1_23 = myparser.current_parser('МТ1_23', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=62&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
Н1_22 = myparser.current_parser('Н1_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=29&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
Р2_23 = myparser.current_parser('Р2_23', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=66&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
С1_22 = myparser.current_parser('С1_22', 'https://e-spo.ru/org/rasp/export/site/index?pid=1&RaspBaseSearch%5Bgroup_id%5D=31&RaspBaseSearch%5Bsemestr%5D=vesna&RaspBaseSearch%5Bprepod_id%5D=')
groups = [С1_23, ИВ1_22_1, ИВ1_22_2, ИВ1_23_1, ИВ1_23_2, ИВ1К_22, ИВ2_22, ИП1_22, ИП1_23, ИП2_23, ИП2К_22, М1_22_1, М1_22_2, М1_23_1, М1_23_2, М1_23_3, М2_23,  МТ1_22, МТ1_23, Н1_22, Р2_23, С1_22]



#def_____________________________________________________
def get_group(chat_id:int):
    with open('users.json', 'r') as f:
        data = json.load(f)
    return data[str(chat_id)]['group']


def get_date_next_week():
    now = datetime.datetime.now()
    day = now.day + 7 - now.weekday()
    try:
        answer = now.replace(day=day)
    except ValueError:
        day -= int(now.max.day)
        answer = now.replace(day=day)
    return answer.date()


def create_user_js():
    try:
         open('users.json', 'r')
    except:
        with open('users.json', 'w') as f:
            admins = {'5111168208': {
    'everyday': False,
    'everylesson': False,
    'changes': False,
    'group': 'С1_23',
    'admin': True,
    'username': 'MAKS1M_BG'
    }}
            json.dump(admins, f)


def get_day_by_int(n_day:int):
    match n_day:
        case 0:
            return 'понедельник'
        case 1:
            return 'вторник'
        case 2:
            return 'среда'
        case 3:
            return 'четверг'
        case 4:
            return 'пятница'
        case 5:
            return 'суббота'
        case 6:
            return 'воскресенье'


def beautiful_day(day:list):
    text = ''
    for lesson in day:
        if len(lesson[1]) > 1:
            text += f'{lesson[0]}.   {lesson[1]}   {lesson[2]}   {lesson[4]}\n'
    return text


#async def_____________________________________________________________________________________
async def send_notice_changes(old:list, new:list, group:str, weekday:int):
        text = ''
        for lesson in old:
            if len(lesson[1]) != 0:
                text += f'{lesson[0]}.   {lesson[1]}   {lesson[2]}   {lesson[4]}\n'
        text += '\n⬇️⬇️⬇️\n\n'
        for lesson in new:
            if len(lesson[1]) != 0:
                text += f'{lesson[0]}.   {lesson[1]}   {lesson[2]}   {lesson[4]}\n'
        with open('users.json', 'r') as f:
            data = json.load(f)
        for ch_id in data.keys():
            if data[ch_id]['changes'] and data[ch_id]['group'] == group:
                await bot.send_message(ch_id, f'*новое изменение в расписании для группы {group}:* \n({get_day_by_int(weekday)})\n\n{text}', parse_mode="Markdown")


async def check_changes():
    for i in groups:
        i.parse()

    for i in groups:
        with open(f'groups/{i.name}.json', 'r') as f:
            data = json.load(f)
        for n_day, day in enumerate(data):
            if day != i.buf[n_day]:
                await send_notice_changes(day, i.buf[n_day], i.name, n_day)


async def send_everylesson(day, lesson):
    with open('users.json', 'r') as f:
        users = json.load(f)
    for id in users.keys():
        if users[f'{id}']['everylesson']:
            group = get_group(id)
            with open(f'groups/{group}.json', 'r') as f:
                week = json.load(f)
            if len(week[day][lesson][1]) > 1:
                await bot.send_message(id, f'*следующий урок для группы {group}:* \n{week[day][lesson][0]}. {week[day][lesson][1]} {week[day][lesson][2]} {week[day][lesson][4]}', parse_mode='Markdown')


async def everylesson():
    print('start everylesson')
    while True:
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        day = time.weekday()
        if hour == 9 and minute > 45:
            await send_everylesson(day, 1)
            await asyncio.sleep(2400)
        elif hour == 10 and minute > 40:
            await send_everylesson(day, 2)
            await asyncio.sleep(2400)
        elif hour == 11 and minute > 35:
            await send_everylesson(day, 3)
            await asyncio.sleep(2400)
        elif hour == 12 and minute > 40:
            await send_everylesson(day, 4)
            await asyncio.sleep(2400)
        elif hour == 13 and minute > 45:
            await send_everylesson(day, 5)
            await asyncio.sleep(2400)
        elif hour == 14 and minute > 45:
            await send_everylesson(day, 6)
            await asyncio.sleep(2400)
        elif hour == 15 and minute > 40:
            await send_everylesson(day, 7)
            await asyncio.sleep(2400)
        elif hour == 16 and minute > 30:
            await send_everylesson(day, 8)
            await asyncio.sleep(2400)
        elif hour == 17 and minute > 20:
            await send_everylesson(day, 9)
            await asyncio.sleep(2400)
        await asyncio.sleep(60)





#main____________________________________________________________________
async def everyday():
    print('start everyday')
    while True:
        time = datetime.datetime.now()
        if time.hour == 6:
            with open('users.json', 'r') as f:
                users = json.load(f)
            for id in users.keys():
                if users[f'{id}']['everyday']:
                    with open(f'groups/{users[str(id)]['group']}.json', 'r') as f:
                        data = json.load(f)
                    day = beautiful_day(data[time.weekday()])
                    await bot.send_message(id, f'*расписание на сегодня:*\n{day}', parse_mode='Markdown')
        await asyncio.sleep(3600)


async def next_week_parse():
    print('start next week pars')
    while True:
        date = get_date_next_week()
        for group in groups:
            url = group.url.replace('index?', f'index?date={date}&')
            myparser.next_week_parse(url, group.name)
        await asyncio.sleep(7200)


async def bot_pool():
    print('starting bot!')
    create_user_js()
    dp.include_router(ro)
    await dp.start_polling(bot)


async def loop():
    print('start loop parser')
    for i in groups:
        i.parse()
        i.lessons_write()

    while True:
        await check_changes()                 

        for i in groups:
            i.lessons_write()
        await asyncio.sleep(1800)



async def main():
    await asyncio.gather(bot_pool(), loop(), everylesson(), next_week_parse(), everyday())





if __name__ == '__main__':
    try:
        asyncio.run(main())
    except ConnectionError:
        print('соеденение потеряно!')
