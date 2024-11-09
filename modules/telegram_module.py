import asyncio
import os

from config import sources, target_channel_url, blocked_username, blocked_keywords


async def find_target_id_by_username(username: str):
    if sources[username]:
        return sources[username]
    return None


async def check_is_not_a_service_post(username, original_message: str):
    if username in blocked_username:
        return False
    if username.lower().endswith("bot"):
        return False
    if any(keyword in original_message.lower() for keyword in blocked_keywords):
        return False

    return True


async def download_all_media_in_group(client, chat, original_post, max_amp=10):
    if original_post.grouped_id is None:
        return [original_post] if original_post.media is not None else []

    search_ids = [i for i in range(original_post.id - max_amp, original_post.id + max_amp + 1)]

    posts = await client.get_messages(chat, ids=search_ids)

    media = []
    for post in posts:
        if post is not None and post.grouped_id == original_post.grouped_id and post.media is not None:
            media.append(post)

    if not os.path.exists('photos'):
        os.makedirs('photos')

    counter = 0
    for post in media:
        counter += 1
        file_name = f'photos/{original_post.id}_{counter}.jpg'
        await post.download_media(file=file_name)

    return len(media)


async def send_message_to_target_channel(client, source_username, sender_name, message_text, media_list):
    message = message_text
    if sender_name:
        message += f"\n\n**Для связи писать сюда:** {sender_name}"
    topic_id = await find_target_id_by_username(source_username)

    if media_list:
        await client.send_file(target_channel_url, media_list, caption=message, reply_to=topic_id)
    else:
        await client.send_message(target_channel_url, message, reply_to=topic_id)
    await asyncio.sleep(2)
