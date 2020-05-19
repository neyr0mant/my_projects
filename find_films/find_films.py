import os
from googletrans import Translator
import re
import time
list_discs = ['E:', 'F:', 'G:']

def transliterate(text):
    translate = "a b v g d e yo zh z i y k l m n o p \
                 r s t u f h ts ch sh shch y y ' e yu ya"
    dic = {chr(ru): translate for ru, translate in zip(
        list(range(1072, 1078)) + [1105] + list(range(1078, 1104)), translate.split())}
    dic.update({chr(ru): translate for ru, translate in zip(
        list(range(1040, 1046)) + [1025] + list(range(1046, 1072)), translate.title().split())})

    new_text = ''
    for char in text:
        if char in dic:
            new_text += dic[char]
        else:
            new_text += char
    return new_text
time_start =  time.time()
google_err = False
while True:
    print("Введите название фильма для поиска")
    name_film = input()
    name_film_ = name_film.lower()
    name_film_translite = transliterate(name_film_)
    exist_films = False
    name_film_translate = " "
    for disc in list_discs:
        google_err = False
        exist_films_disc = False
        for name in os.listdir(disc):
            if "." in name:
                name = name[0:-4]
            name_ = name.lower()
            list_str_split = ['.', "_", "-", "$", "BDRip", "Remux", "Blu-Ray", '1080p', 'BDRip', 'WEB-DL']
            for str_split in list_str_split:
                if str_split in name_:
                    name_ = name_.replace(str_split, " ")
            s1 = time.time()
            if not google_err:
                if len(re.findall(r'[a-z]', name_)) == 0:
                    try:
                        name_film_translate = Translator().translate(name_, dest="ru").text.lower()
                    except:
                        name_film_translate = " "
                        google_err = True
            else:
                name_film_translate = " "
            if name_film_ in name_ or name_film_translite in name_ or name_film_ in name_film_translate:
                if not exist_films_disc:
                    print(r"НА ДИСКЕ %s\ НАЙДЕНЫ ФИЛЬМЫ" % disc)
                    print("   %s\n" % name)
                    exist_films_disc = True
                    exist_films = True
                else:
                    print("   %s\n" % name)
    if not exist_films:
        print("Ни на одном диске ничего не нашли")
    time_finish = time.time()
    print("Отработали за время %s" % (time_finish-time_start))
    print("########## ПОИСК ОКОНЧЕН ##########")
    print(r"Произвести новый  поиск?")
    answer = input()
    if answer:
        continue
    else:
        break

