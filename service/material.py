from typing import TypeVar, Generic
from sqlalchemy.orm import Session
from generic_crud import BaseService
from models.fences import Material
from schema.material import MaterialSchema
from schema.generic import JsonRequest
from datetime import datetime


class MaterialService(BaseService):

    def insert_materials(material:MaterialSchema):
        new_material = Material()
        new_material.image = material.image
        new_material.name = material.name.title()
        new_material.description = new_material.description
        return new_material

    def add_material(self,db:Session,material:Material):
        if not material.name.replace("  ",""):
            return JsonRequest("no tiene nombre el material",None)
        return self.add(db,material)
    
    def remove_material(self,db:Session,id:int):
        material = db.query(Material).filter(Material.id == id)
        if material.count()>0:
            return JsonRequest("no existe el material a eliminar",None)
        material.delete()
        return JsonRequest("material eliminado",True)
    
    def update_material(self,db:Session,material:Material,id:int):
        exist = db.query(Material).filter(Material.id == id).count()
        if(exist):
            self.update(db,material,id)
            return JsonRequest("actualizado con exito",True)
        return JsonRequest("no existe el material a actualizar",None)


