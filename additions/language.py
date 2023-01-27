from additions.database import db
import json
import re
from config import available_languages


class Language:


    def __init__(self):

        # open short_text.json
        with open(f'languages/short_massages.json', 'r', encoding='utf-8') as rl:  # rl = read language
            text_db = json.load(rl)  # text_db = text database

        # convert text_db from dict to list
        self.all_text = []  # all text in database
        for topic in text_db:  # go through all topics
            for text in text_db[topic]:  # go through all text in topic
                for lang in text:  # go through all available languages translation in dict
                    text[lang] = re.sub(r"{.*?}", "{}", text[lang])  # remove all text inside curly braces
                self.all_text.append(text)  # add text with translation to list

        print(f'Loaded {len(self.all_text)} short texts')
        print(f'Available languages: {available_languages}')

        # print(f'All avaible text: {self.all_text}')


    async def trans(self, text: str, user, args=None):  # trans = translate
        if user in available_languages:  # if user language given
            user_lang = user  # user language is user language
        else:  # get user language automatically
            user_lang = await self.get_user_lang(user)  # get user language

        text = re.sub(r"{.*?}", "{}", text)  # remove all text inside curly braces

        # print(f'text: {text}')

        # translate text from database of short msgs
        for text_db in self.all_text:  # go through short msgs in database
            for word_lang in text_db:  # go through all available languages translation in dict
                if text_db[word_lang] == text:  # if msg in database
                    found_text = text_db[user_lang]  # get translation to user language
                    if args:  # put variables in f'{var}'
                        if type(args) == list:  # if args is list
                            found_text = found_text.format(*args)
                        elif type(args) == None:  # if args is not given
                            pass
                        else:  # if only one arg is given
                            found_text = found_text.format(args)
                    print(f'Found text: {found_text}')
                    return found_text  # return translation
        
                        
    

    async def full_trans(self, text: str, user, args=None):
        user_lang = await self.get_user_lang(user)

        with open(f'languages/texts/{text}.txt', encoding='utf-8') as ft:
            text_data = ft.read()
        
        print(f'text_data: {text_data}')

        # find index of "```{user_lang}" in text_data
        index = text_data.find(f'```{user_lang}')
        if index == -1:
            raise Exception(f'Language "{user_lang}" not found in "{text}"')
        
        # find index of "```" after "```{user_lang}"
        index_end = text_data.find('```', index + 1)
        if index_end == -1:
            raise Exception(f'Language "{user_lang}" ending "```" was not found in "{text}"')
        
        result_text = text_data[index + 4 + len(user_lang):index_end]  # text from index to index_end
        print(f'Found text: {result_text}')

        result_text = re.sub(r'{.*?}', '{}', result_text)  # remove all text inside curly braces

        if args:  # put variables in curly braces
            if type(args) == list:  # if args is list
                result_text = result_text.format(*args)  # put variables in curly braces
            elif type(args) == None:  # if args is not given
                pass  # don't change text
            else:  # if only one arg is given
                result_text = result_text.format(args)  # put variable in curly braces

        return result_text  # return translation


    async def get_user_lang(self, user):
        # get user language preferebly from database, otherwise from telegram user settings
        tg_lang = user.language_code[:2]  # get user telegram default language
        bd_lang = await db.userSettings.find_one({'telegram_id': user.id})  # get language user language from database

        if bd_lang and bd_lang.get('language'):  # if user in database
            return bd_lang.get('language')
        elif tg_lang in available_languages:  # if user language is available
            return tg_lang
        else:
            return 'ru'  # default language


    async def get_text(self, link: str):
        lang = await self.get_lang(self.user)
        link = link.split('.')

        with open(f'languages/{lang}', 'r', encoding='utf-8') as rl:
            data = json.load(rl)

        for link_module in link:
            data = data.get(link_module)

        if data.find('BIGTEXT:') == -1:
            return data

        file = data[:8]
        text = ''
        with open(f'{lang}/{file}') as ft:
            for line in ft:
                text += line

        return text