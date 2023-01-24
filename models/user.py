from sqlalchemy import Table,Column, Integer,String,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base
class UserRoles(Base):
    __tablename__ = "userRoles"
    
    user_id = Column(Integer,ForeignKey("users.id"),ondelete="CASCADE",primary_key=True)
    roles_id = Column(Integer,ForeignKey("roles.id"),primary_key=True)

    roles = relationship("Role", back_populates="users")
    users = relationship("User", back_populates="roles")

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

    roles = relationship("UserRoles",back_populates="users")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer,primary_key = True,index= True)
    name = Column(String(250),unique=True)
    description = Column(Text, nullable = True)

    users = relationship("UserRoles", back_populates="roles")

