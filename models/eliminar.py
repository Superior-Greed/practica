from sqlalchemy import Table,Column, Integer,String,DateTime,Text
from sqlalchemy.orm import relationship

from config.db import Base

association_user_roles = Table(
    "userRoles",
    Base.metadata,
    Column("user_id",ForeignKey=("users.id"),primary_key=True),
    Column("roles_id",ForeignKey=("roles.id"),primary_key=True)
)

class User_Roles(Base):
    __tablename__ = "userRoles"

    user_id = Column(ForeignKey=("users.id"),primary_key=True),
    roles_id = Column(ForeignKey=("roles.id"),primary_key=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True,index = True)
    user_name = Column(String(250),unique=True)
    name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250),unique=True)
    password = Column(String(250))
    image = Column(Text,nullable=True)
    session_init = Column(DateTime,nullable=True)

    roles = relationship("Role",secundary="userRoles",back_populates="users")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer,primary_key = True,index= True)
    name = Column(String(250),unique=True)
    description = Column(Text, nullable = True)

    users = relationship("User",secundary=association_user_roles,back_populates="roles")

