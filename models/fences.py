from sqlalchemy import Column,ForeignKey,Integer,String,Text,Numeric,DateTime,Table
from sqlalchemy.orm import relationship

from config.db import Base

association_construction_image = Table(
    "constructionImages",
    Base.metadata,
    Column("construction_id",ForeignKey=("constructions.id"),primary_key=True),
    Column("image_id",ForeignKey=("images.id"),primary_key=True)
)

association_construction_material = Table(
    "constructionMaterials",
    Base.metadata,
    Column("construction_id",ForeignKey=("constructions.id"),primary_key=True),
    Column("material_id",ForeignKey=("material.id"),primary_key=True)
)

class Construction(Base):
    __tablename__ = "constructions"
    
    id = Column(Integer,primary_key=True,index=True)
    name= Column(String(50))
    price= Column(Numeric(10,2),nullable=True)
    init_date = Column(DateTime,nullable=True)
    final_date = Column(DateTime,nullable=True)
    id_type_construction = Column(Integer,ForeignKey("typeConstruction.id"))

    type_construction = relationship("Type_Construction",back_populates="constructions")
    images = relationship("Image_Construction",secundary=association_construction_image,back_populates="construction")
    materials = relationship("Material",secundary=association_construction_material,back_populates="construction")


class Type_Construction(Base):
    __tablename__ = "typeConstructions"
    
    id = Column(Integer,primary_key=True,index=True)
    name= Column(String(250))
    description = Column(Text,nullable=True)

    constructions = relationship("Construction",back_populates="type_construction")

class Image_Construction(Base):
    __tablename__= "images"
    
    id = Column(Integer,primary_key=True,index=True)
    description = Column(Text,nullable=True)
    image = Column(Text,nullable=False)

    construction = relationship("Construction",secundary=association_construction_image,back_populates="images")

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer,primary_key=True,index=True)
    name= Column(String(250))
    description = Column(String(250),nullable=True)
    # purchase_price =Column(Numeric(10,2),nullable = True)
    # sell_price = Column(Numeric(10,2),nullable = True)
    image = Column(Text,nullable = True)

    construction = relationship("Image_Construction",secundary=association_construction_material,back_populates="materials")
