import requests
import bs4
import json
import os


        

class current_parser:
    def __init__(self, name:str, url:str) -> None:
        self.url = url
        self.buf = [[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],]]
        self.name = name

    def parse(self):
        r = requests.get(self.url)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        soup_days = soup.find_all('tbody')
        for n_day, day in enumerate(soup_days):
            soup_day = day.find_all('tr')
            for n_lesson, lesson in enumerate(soup_day):
                soup_lesson = lesson.find_all('td')
                for n_lesson_info, lesson_info in enumerate(soup_lesson):
                    if n_lesson_info == 2:
                        test = lesson_info.find('div')                                                                                                              
                        if test:
                            test = test.find_all('div')
                            lesson_info = f'{test[0].text}  /  {test[1].text}'
                        else:
                            lesson_info = str(lesson_info.text)
                    elif n_lesson_info == 4:
                        if len(lesson_info) > 0:
                            lesson_info = '🟡'
                        else:
                            lesson_info = ''
                    else:
                        lesson_info = str(lesson_info.text)
                    rm = self.name.replace('_', '-')
                    self.buf[n_day][n_lesson][n_lesson_info] = lesson_info.replace(f'гр.{rm}РТК', '')
        self.buf[6] = [[1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', '']]


    def lessons_write(self):
        with open(f"groups/{self.name}.json", 'w') as js:
            x = self.buf
            json.dump(x, js)


    def __str__(self) -> str:
        return f'{self.buf}'
    

def next_week_parse(url:str, name:str):
    buf = [[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],],[['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],]]
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    soup_days = soup.find_all('tbody')
    for n_day, day in enumerate(soup_days):
        soup_day = day.find_all('tr')
        for n_lesson, lesson in enumerate(soup_day):
            soup_lesson = lesson.find_all('td')
            for n_lesson_info, lesson_info in enumerate(soup_lesson):
                if n_lesson_info == 2:
                    test = lesson_info.find('div')                                                                                                              
                    if test:
                        test = test.find_all('div')
                        lesson_info = f'{test[0].text}  /  {test[1].text}'
                    else:
                        lesson_info = str(lesson_info.text)
                elif n_lesson_info == 4:
                    if len(lesson_info) > 0:
                        lesson_info = '🟡'
                    else:
                        lesson_info = ''
                else:
                    lesson_info = str(lesson_info.text)
                rm = name.replace('_', '-')
                buf[n_day][n_lesson][n_lesson_info] = lesson_info.replace(f'гр.{rm}РТК', '')
    buf[6] = [[1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', ''], [1, '', '', '', '']]
    with open(f'next_week_groups/{name}.json', 'w') as f:
        json.dump(buf, f)


try:
    os.makedirs('groups')
except FileExistsError:
    pass
try:
    os.makedirs('next_week_groups')
except FileExistsError:
    pass
