'''
По поводу импорта key.
Id_key = Api ключ группы.
Group_Id = Айди группы. Только цифры!
My_Id = Ключ пользователя. С разрешением на управление группами!
comment_in_ban = Комментарий для забаненного
'''
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from key import ID_key, Group_Id, My_Id, comment_in_ban

# Во избежания сбоев, ловим ошибки
try:
    while True:
        # Узнает, есть ли НЕГОДЯЙ в группе
        def check_user(Group_Id, from_ID):
            Member = Api_Chat.method('groups.isMember', {'group_id': Group_Id,
                                                         'user_ids': from_ID})
            return Member

        # Бан по User ID
        def user_del(Group_Id, from_ID, comment_in_ban):
            My_Id1.method('groups.ban', {'group_id': Group_Id,
                                         'owner_id': from_ID,
                                         'comment_visible': 1,
                                         'comment': comment_in_ban,
                                         'reason': 1})

        # Удаляем смс НЕГОДЯЯ
        def message_del(event, message_ID2):
            Api_Chat.method('messages.delete', {'peer_id': event.message.get('peer_id'),
                                                'message_ids': message_ID2,
                                                'delete_for_all': 1,
                                                'random_id': get_random_id()})

        # Из смс вытягиваем промежуточный User ID
        def check_message_ID(event, message_ID):
            jls_extract_var = 'messages.getByConversationMessageId'
            a = Api_Chat.method(jls_extract_var, {'peer_id': event.message.get('peer_id'),
                                                  'conversation_message_ids': message_ID})
            return a
        # Присылает сообщение, если увидит в чате #бот
        def check_life(message):
            Api_Chat.method('messages.send', {'peer_id': event.message.get('peer_id'),
                                              'message': message,
                                              'random_id': get_random_id()})
        # Во избежания сбоев, ловим ошибки
        try:
            # Указываем ключик от группы
            Api_Chat = vk_api.VkApi(token=ID_key)
            # Указываем личный ключик
            My_Id1 = vk_api.VkApi(token=My_Id)
            # Подключаем бота
            Type_Poll = VkBotLongPoll(Api_Chat, Group_Id)
            # Статус старта
            print('Status: Launched\n')
            for event in Type_Poll.listen():   # Запуск бота
                # Ловим смс
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    # Блок бана пользователя по айди
                    # Промежуточный ID смс
                    message_ID = event.message.get('conversation_message_id')
                    # Информация о смс
                    message_INFO = check_message_ID(event, message_ID)
                    # Реальный ID смс
                    message_ID2 = message_INFO['items'][0]['id']
                    # User ID отправителя
                    from_ID = event.message.get('from_id')
                    # Определяем, является ли отправитель участником группы
                    Check_User_group = check_user(Group_Id, from_ID)
                    Result_check_user = Check_User_group[0]
                    if Result_check_user['member'] == 0:
                        # Если не является участником
                        message_del(event, message_ID2)
                        user_del(Group_Id, from_ID, comment_in_ban)

                    # Блок для проверки работоспособности бота написав #бот
                    sender_message = event.obj['message']
                    text_user = sender_message['text']
                    if text_user == '#бот':
                        check_life('Бот работает!')
        except Exception as e:
            print('Error: ', e)
            # Перезапуск через 3 секунды
            time.sleep(3)
except Exception as e:
    print('\nError: ', e)
    # Перезапуск через 22 секунды
    time.sleep(22)
