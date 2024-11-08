import logging
import os
import random

from telethon import events
from telethon import types

from config import main_account, sources, account_1, account_2, account_3, account_4, account_5, account_6
from modules.openai_module import rewrite_message
from modules.telegram_module import download_all_media_in_group, send_message_to_target_channel

# main_account.start()
account_1.start()
account_2.start()
account_3.start()
account_4.start()
account_5.start()
account_6.start()

@main_account.on(events.NewMessage(list(sources.keys())))
async def handler(event):
    try:
        if event.message.message != '':
            print(event)

            # Текст сообщения
            original_message_text = event.message.message

            # Имя канала
            channel_name = event.chat.username

            # Автор при наличии
            sender = await event.get_sender()
            sender_name = f"@{sender.username}" if isinstance(sender, types.User) else None


            # Скачивание фото
            media_list = []
            if event.message.grouped_id:
                number_of_media = await download_all_media_in_group(main_account, event.message.peer_id.channel_id, event.message)
                for i in range(1, number_of_media + 1):
                    media_list.append(f"photos/{event.message.id}_{i}.jpg")
            elif event.message.media:
                file_name = f'photos/{event.message.id}.jpg'
                await event.message.download_media(file=file_name)
                media_list = [file_name]

            # Рандомный выбор аккаунта ТГ
            client = random.choice([account_1, account_2, account_3, account_4, account_5, account_6])

            # Рерайт оригинала сообщения
            rewrited_message = await rewrite_message(original_message_text)

            # Отправка сообщения
            await send_message_to_target_channel(client, channel_name, sender_name, rewrited_message, media_list)
            print(f"Публикация с {channel_name}")

            # Удаление после отправки
            for media in media_list:
                os.remove(media)



    except Exception as e:
        logging.ERROR(f"Произошла ошибка во время обработки ивента\n{e}")



with main_account:
    main_account.run_until_disconnected()



