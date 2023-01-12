import typing
import sqlalchemy
import db.schema


async def create_book(session, title):
    rec = db.schema.Book(title=title)
    session.add(rec)
    await session.commit()
    return rec


async def create_author(session, name):
    rec = db.schema.Author(name=name)
    session.add(rec)
    await session.commit()
    return rec


# generic reusable code for any object type to get a page of items
# using limit and offset
async def get_page(session, class_name: str, order_by_column_name: str,
                   limit: int, offset: int):

    db_schema_class = getattr(db.schema, class_name)
    order_by_column = getattr(db_schema_class, order_by_column_name)

    sql = sqlalchemy.select(db_schema_class).\
        limit(limit).offset(offset).\
        order_by(order_by_column)
    return (await session.execute(sql)).scalars().all()
