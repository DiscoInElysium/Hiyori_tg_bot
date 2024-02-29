# CREATE
# READ
# UPDATE
# DELETE


from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from anime_parser.anime_storage import ongoing_to_storage
from database.models import OngoingList, User, User_OngoingList_association


async def get_ongoings(session: async_sessionmaker[AsyncSession]) -> list[OngoingList]:
    async with session() as session:
        stmt = select(OngoingList)
        result = await session.execute(stmt)
        ongoings = result.scalars()

    return list(ongoings)


async def insert_users(telega_id, session: async_sessionmaker[AsyncSession]) -> None:
    stmt = (
        insert(User).
        values(telegram_id=telega_id)
    )
    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def get_users(session: async_sessionmaker[AsyncSession]) -> list[User]:
    async with session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars()

    return list(users)


async def insert_ongoings(session: async_sessionmaker[AsyncSession]) -> None:

    rows = ongoing_to_storage()

    stmt = insert(OngoingList).values(
        [{
            'anime_title': anime_title,
            'anime_description': anime_description,
            'link': link,
            'release_day': release_day,
            'release_date': release_date
        } for anime_title, anime_description, link, release_day, release_date in rows
        ])
    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def delete_ongoing(ongoing, session: async_sessionmaker[AsyncSession]) -> None:

    stmt = delete(OngoingList).where(OngoingList.anime_title == ongoing)

    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def delete_association(ongoing_id, session: async_sessionmaker[AsyncSession]) -> None:

    stmt = delete(User_OngoingList_association).where(User_OngoingList_association.right_id == ongoing_id)

    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def update_ongoing(ongoing, new_release_date, session: async_sessionmaker[AsyncSession]) -> None:

    stmt = (
        update(OngoingList).
        where(OngoingList.anime_title == ongoing).
        values(release_date=new_release_date)
    )

    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def create_remainder(telegram_id, ongoing_id, session: async_sessionmaker[AsyncSession]) -> None:
    stmt = insert(User_OngoingList_association).values(left_id=telegram_id, right_id=ongoing_id)
    async with session() as session:
        async with session.begin():
            await session.execute(stmt)


async def get_remainder(session: async_sessionmaker[AsyncSession]) -> list[User_OngoingList_association]:
    async with session() as session:
        stmt = select(User_OngoingList_association)
        result = await session.execute(stmt)
        ongoings = result.scalars()

    return list(ongoings)
