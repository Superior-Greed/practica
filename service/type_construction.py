from sqlalchemy.orm import Session
from generic_crud import BaseService
from models.fences import TypeConstruction
from schema.type_construction import TypeConstructionSchema
from schema.generic import JsonRequest

class TypeConstructioService(BaseService):
    
    def insert_type_costruction(type_construction:TypeConstructionSchema):

        new_type_construction = TypeConstruction()
        new_type_construction.name = type_construction.name.title()
        new_type_construction.description = type_construction.description
        return new_type_construction
    
    def add_type_construction(self,db:Session,type_construction:TypeConstruction):
        if not type_construction.name.replace("  ",""):
            return JsonRequest("no hay nombre",None)
        return JsonRequest("creado con exito",self.add(db,type_construction))
    
    def delete_type_costruction(self,db:Session,id:int):
        type_costruction = db.query(TypeConstruction).filter(TypeConstruction.id == id)
        if type_costruction.count()>0:
            return JsonRequest("no esta registrado se tipo de construccion",None)
        type_costruction.delete()
        return JsonRequest("se a eliminado con exito",True)
    
    def update_type_construction(self,db:Session,type_construction:TypeConstruction,id:int):
        exist = db.query(TypeConstruction).filter(TypeConstruction.id == id).count()
        if(exist):
            self.update(db,type_construction,id)
            return JsonRequest("actualizado con exito",True)
        return JsonRequest("no existe el typo de constructionn a actualizar",None)


