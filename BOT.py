import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from key import ID_key, Grop_Id, My_Id
'''
По поводу импорта key.
Id_key = Api ключ группы.
Grop_Id = Айди группы. Только цифры!
My_Id = Ключ пользователя. С разрешением на управление группами!
'''
while True:
    # Узнает, есть ли ты в группе
    def check_user(Grop_Id, from_ID):
        Member = Api_Chat.method('groups.isMember', {'group_id': Grop_Id,
                                                     'user_ids': from_ID})
        return Member

    # Бан по User ID
    def user_del(Grop_Id, from_ID, comment_in_Ban):
        My_Id1.method('groups.ban', {'group_id': Grop_Id,
                                     'owner_id': from_ID,
                                     'comment_visible': 1,
                                     'comment': comment_in_Ban,
                                     'reason': 1})

    # Удаляем смс НЕГОДЯЯ
    def message_del(event, message_ID2):
        Api_Chat.method('messages.delete', {'peer_id': event.message.get('peer_id'),
                                            'message_ids': message_ID2,
                                            'delete_for_all': 1,
                                            'random_id': get_random_id()})

    # Из смс вытягиваем премежуточный User ID
    def check_message_ID(event, message_ID):
        a = Api_Chat.method('messages.getByConversationMessageId', {'peer_id': event.message.get('peer_id'),
                                                                    'conversation_message_ids': message_ID})
        return a
    # Указываем ключик от группы
    Api_Chat = vk_api.VkApi(token=ID_key)
    # Указываем личный ключик
    My_Id1 = vk_api.VkApi(token=My_Id)
    # Подключаем бота
    Type_Poll = VkBotLongPoll(Api_Chat, Grop_Id)
    # Статус старта
    print('Launched')
    try:  # Во избежания сбоев, ловим ошибки
        for event in Type_Poll.listen():   # Запуск бота
            # Ловим смс
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                # Премежуточный ID смс
                message_ID = event.message.get('conversation_message_id')
                # Информация о смс
                message_INFO = check_message_ID(event, message_ID)
                # Реальный ID смс
                message_ID2 = message_INFO['items'][0]['id']
                # User ID отправтеля
                from_ID = event.message.get('from_id')
                comment_in_Ban = 'Текст'
                # Определяем, является ли отправитель участником группы
                Check_User_group = check_user(Grop_Id, from_ID)
                Result_check_user = Check_User_group[0]
                if Result_check_user['member'] == 0:
                    # Если не является участником
                    message_del(event, message_ID2)
                    user_del(Grop_Id, from_ID, comment_in_Ban)
                else:
                    pass
    except Exception:
        try:
            print('\nERROR_VK')
            # Перезапуск через 3 секунды
            time.sleep(3)
        except Exception:
            print('\nERROR_VK')
            # Перезапуск через 10 секунды
            time.sleep(10)
