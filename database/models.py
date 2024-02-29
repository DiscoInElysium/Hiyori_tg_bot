from __future__ import annotations

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from config import SQL_URL
from typing import List


engine = create_async_engine(SQL_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User_OngoingList_association(Base):
    __tablename__ = "association_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    left_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)
    right_id: Mapped[int] = mapped_column(
        ForeignKey("ongoing_list.id"), primary_key=True, nullable=False)
    ongoing_list: Mapped["OngoingList"] = relationship(back_populates="users")
    users: Mapped["User"] = relationship(back_populates="ongoing_list")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    # new
    ongoing_list: Mapped[List["User_OngoingList_association"]] = relationship(back_populates="users")


class OngoingList(Base):
    __tablename__ = 'ongoing_list'

    id: Mapped[int] = mapped_column(primary_key=True)
    anime_title: Mapped[str] = mapped_column(unique=True)
    anime_description = mapped_column(Text)
    link: Mapped[str] = mapped_column(unique=True)
    release_day: Mapped[str] = mapped_column()
    release_date: Mapped[str] = mapped_column()
    users: Mapped[List["User_OngoingList_association"]] = relationship(back_populates="ongoing_list")
    # new


async def async_main():
    # async with db_helper.session.factory() as session
    #   #await main_relations(session)
    #   await demo_m2m(session)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
