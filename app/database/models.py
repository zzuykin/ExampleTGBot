from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os


load_dotenv()
engine = create_async_engine(url = os.getenv("SQLALCHEMY_URL"))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(25))
    user_name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(25))
    phone_num: Mapped[str] = mapped_column(String(25))

    # Связь с заказами, указываем foreign_keys=[Order.user_id] для явного указания внешнего ключа
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    photo_url : Mapped[str] = mapped_column(String(120))

    # Связь с заказами, указываем foreign_keys=[Order.item_id] для явного указания внешнего ключа
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="item")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Связь с пользователем через внешний ключ
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")

    # Связь с товаром через внешний ключ
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    item: Mapped["Item"] = relationship("Item", back_populates="orders")

    user_description: Mapped[str] = mapped_column(String(120))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
