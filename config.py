import os
from os import getenv

import dotenv
from telethon import TelegramClient

dotenv.load_dotenv()

# OpenAI Token for rewrite module
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# Target channel URL
target_channel_url = "https://t.me/Dubai_UAE_Hub"

# Database creds
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_DBNAME = os.getenv("POSTGRESQL_DBNAME")

# Source TG Channels / Chats
sources = {
    # TEST
    "testparsing12121": 12,
    "hdjdbjdjddjdjdj": 12,

    # НОВОСТИ
    "ND_DubaiNews": 2,
    "dubaiz": 2,
    "novosti_dubai": 2,
    "dubai_go_uae": 2,
    "live_emirates": 2,
    "dubai_zdorovo": 2,
    "Dubai_Russkie": 2,

    # ПРОДАЖА НЕДВИЖИМОСТИ
    "axcapital_cis": 3,
    "uae_forlife": 3,
    "billionacedubai": 3,

    # Аренда недвижимости
    # "RealtyDubay": 4,
    # "nedviga_dubai": 4,
    # "UAEDubai_Realty": 4,
    # "Dubai_dvizh": 4,

    # ОТЕЛИ, РЕСТОРАНЫ, РАЗВЛЕЧЕНИЯ, ЭКСКУРСИИ
    "hotel_avia_tours": 5,
    "Dubai_turist": 5,
    "Dubai_tgtop": 5,
    "dubaiadvise": 5,
    "wheregodubai": 5,
    "dubai_pro": 5,
    "Da_Dubai": 5,

    # БИЗНЕС, НАЛОГИ, ЮР И БУХ УСЛУГИ
    "legalblog_uae": 6,
    "bbdmcc": 6,
    "dubailaw": 6,

    # РАБОТА, ВАКАНСИИ И РЕЗЮМЕ
    "rabota_dubayz": 8,
    "dubai_vakansii": 8,
    # "vacancy_dxb": 8,

    # ОБМЕН ВАЛЮТЫ
    "dubaisk_obmen": 9,
    "moneyDUBAIchat": 9,
    "obmen_dubai_oae_24": 9,

    # АРЕНДА АВТО
    "prokat_oae": 10,
    "AutoinDubai": 10,
    "RentaCar_Dubai": 10,

    # БАРАХОЛКА
    # "DubaiSell": 11,
    # "dubay_chat": 11
}

keywords = ["куплю", "продам", "обменяю"]

blocked_username = ["@Pereka4alkin", "@dima_Amaz", "@None"]
blocked_keywords = []

main_account = TelegramClient('vadim_main', int(os.getenv("MAIN_ACCOUNT_API_ID")), os.getenv("MAIN_ACCOUNT_API_HASH"))
account_1 = TelegramClient('vadim_1', int(os.getenv("ACCOUNT_1_API_ID")), os.getenv("ACCOUNT_1_API_HASH"))
account_2 = TelegramClient('vadim_2', int(os.getenv("ACCOUNT_2_API_ID")), os.getenv("ACCOUNT_2_API_HASH"))
account_3 = TelegramClient('vadim_3', int(os.getenv("ACCOUNT_3_API_ID")), os.getenv("ACCOUNT_3_API_HASH"))
account_4 = TelegramClient('vadim_4', int(os.getenv("ACCOUNT_4_API_ID")), os.getenv("ACCOUNT_4_API_HASH"))
account_5 = TelegramClient('vadim_5', int(os.getenv("ACCOUNT_5_API_ID")), os.getenv("ACCOUNT_5_API_HASH"))
account_6 = TelegramClient('vadim_6', int(os.getenv("ACCOUNT_6_API_ID")), os.getenv("ACCOUNT_6_API_HASH"))
