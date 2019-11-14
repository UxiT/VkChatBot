import vk_api
import Case
from data import token
import data
import random
import re
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from datetime import datetime


vk_session = vk_api.VkApi(token=token)  # #Регистрация
vk = vk_session.get_api()
today = datetime.today().weekday()  # #номер для недели
upload = VkUpload(vk_session)  # #Для загрузки изображений
longpoll = VkBotLongPoll(vk_session, 178266951)
COMMANDS = [
    '!курс',
    '!иб',
    'извините',
            ]

ANSWERS = [
           'КУПИТЕ КУРС',
           'ИБЭЭЭЭЭ',
           'Прощаю',
           ]
STICK_CMD = ['хоба', 'слышь, работать']
STICKS = [6111, 6138]


def who(rsp, event):
    message = re.findall(r'([^\?])', rsp)  # #Сообщение, разбитое в список без всех вопросительных знаков
    res = ''
    for ch in message:
        res += ch
    res = re.sub(r'!кто', '', res)
    count = vk.messages.getConversationMembers(peer_id=event.object['peer_id'])['count']
    ind = random.randint(0, count)
    del(count)
    person = vk.messages.getConversationMembers(peer_id=event.object['peer_id'])['profiles'][ind - 2][
                 'first_name'] + ' ' + \
             vk.messages.getConversationMembers(peer_id=event.object['peer_id'])['profiles'][ind - 2][
                 'last_name']
    Sending.msg(person + ' ' + res, event)


def msg(mesg, event):
    vk.messages.send(
        peer_id=event.object['peer_id'],
        random_id=get_random_id(),
        message=str(mesg)
    )


def pic(picture, event):
    vk.messages.send(
        peer_id=event.object['peer_id'],
        random_id=get_random_id(),
        attachment=picture
    )


def stick(sticker, event):
    vk.messages.send(
        peer_id=event.object['peer_id'],
        random_id=get_random_id(),
        sticker_id=sticker
    )


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:

            print(event.object['text'])

            print(event.object)

            response = event.object['text'].lower()
            if event.object['peer_id'] == 134534344 & event.object['from_id'] == 134534344:
                vk.messages.send(
                    peer_id = 2000000001,
                    message = str(event.object['text']),
                    random_id = get_random_id(),
                    sticker_id = event.object['attachments'][0]['sticker']['sticker_id']
                )
            try:
                if str(response) in COMMANDS:
                    msg(str(ANSWERS[COMMANDS.index(response)]), event)  # #возвращает соответствующий комманде ответ

                elif str(response) in STICK_CMD:
                    stick(str(STICKS[STICK_CMD.index(response)]), event)

                elif 'хуй' in response or 'пизд' in response or 'хуя' in response:
                    Sending.msg('За мат извенись', event)

                elif random.randint(0, 100) == 1:
                    vk.messages.send(
                        peer_id=event.object['peer_id'],
                        random_id=get_random_id(),
                        message='>'+event.object['text'],
                        attachment='photo-178266951_4562390'+str(random.randint(71, 92))
                    )

                if '!кто' in response:
                    who(response, event)

                elif '!kick антон' in response:
                    vk.messages.removeChatUser(
                        chat_id=1,
                        user_id=95224614
                    )

                if response == '!flip':
                    msg(Case.coin(random.randint(1, 2)),event)

                if response == '!shutdown':
                    raise TypeError

                if response == '!help':
                    out = ''
                    for i in range(len(COMMANDS)):
                        out += COMMANDS[i]+'\n'
                    msg(out, event)
                    del(out)

                if '!список' in response:
                    response = list(response.split())
                    del(response[0])
                    if len(response)==0:
                        for i in range(26):
                            msg(str(1)+'. '+data.student_list(i))
                    msg(data.student_list(response[0]),event)

            except vk_api.ApiError as er_msg:
                print(er_msg)


if __name__ == '__main__':
    main()
