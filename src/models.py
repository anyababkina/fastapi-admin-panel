import sqlalchemy


from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )


class Admin(Base):
    __tablename__ = 'admin'

    username = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True
    )

    password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False
    )


class User(Base):
    __tablename__ = 'user'

    username = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True
    )

    password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False
    )

    items = relationship(
        'Item',
        back_populates='user',
        uselist=True,
        lazy='joined'
    )


class Item(Base):
    __tablename__ = 'item'

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id')
    )

    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )

    description = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=True
    )

    user = relationship(
        'User',
        back_populates='items',
        uselist=False,
        lazy='joined'
    )
