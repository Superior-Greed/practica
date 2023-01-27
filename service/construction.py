from sqlalchemy.orm import Session
from generic_crud import BaseService
from models.fences import Construction,ConstructionMaterial
from schema.construction import ConstructionSchema
from schema.generic import JsonRequest

class ConstructionService(BaseService):
    
    def insert_construction(construction:ConstructionSchema):
        new_construction = Construction()
        new_construction.id_type_construction = construction.id_type_construction
        new_construction.final_date  = construction.final_date
        new_construction.init_date = construction.init_date
        new_construction.price = construction.price
        new_construction.name = construction.name
        return new_construction
    
    def add_construction(self, db:Session,construction:Construction):
        return