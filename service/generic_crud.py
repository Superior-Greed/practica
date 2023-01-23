from typing import TypeVar, Generic
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseService():

    @staticmethod
    def all(db:Session,model:Generic[T]):
        return db.query(model).all()
    
    @staticmethod
    def filter(db:Session, model:Generic[T],id:int):
        return db.query(model).filter(model.id ==id).first()
    
    @staticmethod
    def add(db:Session,model:Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def remove(db:Session,model:Generic[T]):
        db.delete(model)
        db.commit()

    @staticmethod
    def add_all(db:Session,models:list[Generic[T]]):
        db.add_all(models)
        db.commit()
    
    @staticmethod
    def update(db:Session, model:Generic[T],id:int):
        db.query(model).filter(model.id == id).first().update(model,synchronize_session=False)

    # @staticmethod
    # def update(db:Session,model:Generic[T],id: int):
    #     up = db.query(model).filter(model.id ==id).one()
    #     up = model
    #     db.commit()

