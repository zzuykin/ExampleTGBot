from app.database.models import async_session
from app.database.models import User, Item, Order
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


async def is_reg(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return False
    return True


async def get_user(tg_id) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def get_catalog():
    async with async_session() as session:
        return await session.scalars(select(Item))


async def get_item(item_id: int) -> Item:
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_items_name() -> dict:
    items = await get_catalog()
    names = {}
    for item in items:
        names[item.id] = item.name
    return names


async def set_user(user: User):
    async with async_session() as session:
        session.add(user)
        await session.commit()


async def set_order(order: Order):
    async with async_session() as session:
        session.add(order)
        await session.commit()


async def get_order(id: int) -> Order:
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == id))
        return order


async def get_orders(tg_id):
    async with async_session() as session:
        result = await session.execute(
            select(User)
                .options(selectinload(User.orders))  # Загружаем связанные заказы
                .where(User.tg_id == tg_id)
        )
        user = result.scalar()
        return user.orders if user else []


async def del_order(order_id):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                await session.delete(order)
                await session.commit()


async def change_order(order_id, new_descr):
    try:
        async with async_session() as session:
            stmt = update(Order).where(Order.id == order_id).values(user_description=new_descr)
            await session.execute(stmt)
            await session.commit()
    except:
        print(f"Ошибка при обновлении пользователя")
