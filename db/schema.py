import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

# This is a simplistic DB schema containing two tables without any
# relationship between them, to keep this demo code short. We define
# two tables in order to demonstrate how to implement pagination
# only once, such that it can be reused for any type of object
# (decoupling).


class Book(Base):
    __tablename__ = "books"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.id}: '{self.title}'"


class Author(Base):
    __tablename__ = "authors"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.id}: '{self.name}'"
