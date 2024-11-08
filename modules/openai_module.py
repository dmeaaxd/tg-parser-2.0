from openai import OpenAI

from config import OPENAI_TOKEN


async def rewrite_message(message_text):
    client = OpenAI(api_key=OPENAI_TOKEN)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": f"Сделай художественный рерайт текста без потери смысла и стиля! Не нужно писать поэмы\n"
                        f"НИКОГДА не пиши в начале: конечно вот художественный рерайт текста или похожее, ПИШИ ТОЛЬКО САМ ПЕРЕПИСАННЫЙ ТЕКСТ, ничего лишнего!"},
            {"role": "user", "content": f"Текст для рерайта:\n{message_text}"},

        ],
        max_tokens=5000
    )
    return completion.choices[0].message.content
