from datetime import date

from sqlalchemy import Column, Integer, String, DateTime, func, select
from tenacity import retry, stop_after_attempt, wait_fixed

from database.connection import Base, engine, async_session


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)

    date_added = Column(DateTime, default=func.now())


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), retry_error_callback=lambda x: print("Не удалось подключиться к базе данных"))
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Асинхронная функция для добавления сообщения в базу данных
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
async def add_message(text: str):
    async with async_session() as session:
        async with session.begin():
            message = Message(text=text)
            session.add(message)
            await session.commit()

# Асинхронная функция для проверки наличия сообщения с указанным текстом за сегодня
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
async def is_message_exist_today(text: str) -> bool:
    async with async_session() as session:
        today = date.today()
        query = select(Message).where(
            Message.text == text,
            func.date(Message.date_added) == today
        )
        result = await session.execute(query)
        return result.scalar() is None


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
async def add_message_if_not_exists(text: str) -> bool:
    """Добавляет сообщение, если его еще нет в базе данных. Возвращает True, если сообщение добавлено, иначе False."""
    async with async_session() as session:
        async with session.begin():
            today = date.today()
            query = select(Message).where(
                Message.text == text,
                func.date(Message.date_added) == today
            ).with_for_update()  # блокируем строку, если она существует

            result = await session.execute(query)
            existing_message = result.scalar()

            if existing_message is None:
                # Добавляем сообщение только если его нет
                message = Message(text=text)
                session.add(message)
                await session.commit()
                return True  # Сообщение добавлено
            else:
                return False  # Сообщение уже существует
