import asyncio
import os
import random

from telethon import events
from telethon import types
from telethon.tl.functions.messages import SendMultiMediaRequest

from config import main_account, sources, account_1, account_2, account_3, account_5, account_6, keywords
# from config import main_account, sources
from database.models import is_message_exist_today, add_message, init_db, add_message_if_not_exists
from modules.openai_module import rewrite_message
from modules.telegram_module import download_all_media_in_group, send_message_to_target_channel, \
    check_is_not_a_service_post, check_by_keywords

# main_account.start()
account_1.start()
account_2.start()
account_3.start()
# account_4.start()
account_5.start()
account_6.start()

# Инициализация таблиц
loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())


@main_account.on(events.NewMessage(list(sources.keys())))
async def handler(event):

    try:
        if event.message.message != '':

            # Текст сообщения
            original_message_text = event.message.message

            # Имя канала
            channel_name = event.chat.username if event.chat.username else None
            # print(f"\n\n\nCHANNEL NAME - {channel_name}\n\n\n")

            # Автор при наличии
            sender = await event.get_sender()
            sender_name = f"@{sender.username}" if isinstance(sender, types.User) else None
            # sender_name = f"@{sender.username}" if isinstance(sender, types.User) and sender.username else "Unknown"
            # print(f"\n\n\nSENDER NAME - {sender_name}\n\n\n")


            if await check_by_keywords(is_channel=event.message.post, message=original_message_text, keywords=keywords) and await check_is_not_a_service_post(sender_name, original_message_text) and await add_message_if_not_exists(original_message_text):
                await add_message(original_message_text)

                # Скачивание фото при наличии
                media_list = []
                if event.message.grouped_id:
                    number_of_media = await download_all_media_in_group(main_account, event.message.peer_id.channel_id,
                                                                        event.message)
                    for i in range(1, number_of_media + 1):
                        media_list.append(f"photos/{event.message.id}_{i}.jpg")
                elif event.message.media:
                    file_name = f'photos/{event.message.id}.jpg'
                    await event.message.download_media(file=file_name)
                    media_list = [file_name]

                # Рандомный выбор аккаунта ТГ
                client = random.choice([account_1, account_2, account_3, account_5, account_6])
                # client = main_account
                # Рерайт оригинала сообщения
                rewrited_message = await rewrite_message(original_message_text)

                if channel_name is None:
                    print(f"Ошибка: у канала нет username, event.chat.id: {event.chat.id}")
                    return

                # Отправка сообщения
                try:
                    await send_message_to_target_channel(client, channel_name, sender_name, rewrited_message,
                                                         media_list)
                    print(f"Публикация с {channel_name}")
                except Exception:
                    # Попытка повторной отправки с оригинальным текстом
                    try:
                        await send_message_to_target_channel(client, channel_name, sender_name, original_message_text, media_list)
                        print(f"Публикация с {channel_name} с оригинальным текстом")
                    except Exception:
                        print(f"Ошибка публикации в канал / чат: {channel_name}")

                # Удаление после отправки
                for media in media_list:
                    os.remove(media)

            else:
                print(f"Не прошел проверки: {channel_name}")



    except Exception as e:
        print(f"Произошла ошибка во время обработки ивента\n{print(event)}\n\n{e}")


with main_account:
    main_account.run_until_disconnected()
