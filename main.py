import asyncio
import db.session
import db.schema
import db.ops


async def init_db():
    """ Init the database (create the tables) """

    async with db.session.engine.begin() as conn:
        await conn.run_sync(db.schema.Base.metadata.drop_all)
        await conn.run_sync(db.schema.Base.metadata.create_all)

# Hardcoded titles for books to be inserted into the database
book_titles = [
    'The Great Gatsby',
    'Atlas Shrugged',
    'Three Comrades',
    '1984',
    'Anne of Avonlea',
    'For Whom The Bell Tolls',
    'Moby Dick',
    'Anne of Green Gables',
    'Middlemarch',
    'The Voyage Out'
]

# Hardcoded names for authors to be inserted into the database
author_names = [
    'Ernest Hemingway',
    'L M Montgomery',
    'F Scott Fitzgerald',
    'Virginia Woolf',
    'George Orwell',
    'George Eliot',
]


async def fill_db():
    """ Create some books and authors in the db """

    async with db.session.SessionMaker() as session:

        print(f'\nCreating {len(book_titles)} books in the database:')
        for title in book_titles:
            book = await db.ops.create_book(session, title)
            print(book)

        print(f'\nCreating {len(author_names)} authors in the database:')
        for name in author_names:
            author = await db.ops.create_author(session, name)
            print(author)


def calc_page_number(offset: int, limit: int):
    """ Calculate the current page number based on the offset and the limit """
    return (offset // limit) + 1

async def print_page_by_page(class_name: str, order_by_column_name: str,
                             limit: int):
    print(f'\nPaginated {class_name}s ordered by {order_by_column_name} '
          f'({limit=}):')

    async with db.session.SessionMaker() as session:

        has_next_page = True
        offset = 0
        # Print all the pages from beginning to end.
        while has_next_page:

            # Get the next page.
            # Get one extra item to check if there is a next page.
            page = await db.ops.get_page(
                session, class_name, order_by_column_name,
                limit + 1, offset)
            has_next_page = len(page) == limit + 1

            if len(page) == 0:
                # no more books
                break

            # Erase the extra book, if there was one.
            if has_next_page:
                page = page[:-1]

            # Print the page.
            print(f'\nPAGE {calc_page_number(offset, limit)} ({offset=}, {limit=}):')
            for item in page:
                print(item)

            # Move the offset forward.
            offset += limit


async def cleanup():
    await db.session.engine.dispose()

PAGE_SIZE = 3


async def main():
    await init_db()
    await fill_db()
    await print_page_by_page('Book', 'id', PAGE_SIZE)
    await print_page_by_page('Book', 'title', PAGE_SIZE)
    await print_page_by_page('Author', 'id', PAGE_SIZE)
    await print_page_by_page('Author', 'name', PAGE_SIZE)
    await cleanup()


if __name__ == '__main__':
    asyncio.run(main())
