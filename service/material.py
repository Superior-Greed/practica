from typing import TypeVar, Generic
from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.fences import Material,ConstructionMaterial
from schema.material import MaterialSchema
from schema.generic import JsonRequest
from datetime import datetime


class MaterialService(BaseService):

    def insert_materials(material:MaterialSchema):
        new_material = Material()
        new_material.image = material.image
        new_material.name = material.name.title()
        new_material.description = material.description
        return new_material
    
    def insert_materials_schema(material:Material):
        new_material = MaterialSchema(
        id=material.id,
        image = material.image,
        name = material.name,
        description = material.description
        )
        return new_material
    
    def add_material(self,db:Session,material:Material):
        if not material.name.replace("  ",""):
            return JsonRequest(error="no tiene nombre el material",value=None)
        return  JsonRequest(error="actualizado con exito",value=self.insert_materials_schema(self.add(db,material)))
    
    def remove_material(self,db:Session,id:int):
        material = db.query(Material).filter(Material.id == id)
        if material.count()==0:
            return JsonRequest(error="no existe el material a eliminar",value=None)
        construction_material = db.query(ConstructionMaterial).filter(ConstructionMaterial.material_id == id)
        if construction_material > 0:
            construction_material.delete()
            db.commit()
        material.delete()
        db.commit()
        return JsonRequest(error="material eliminado",value=True)
    
    def update_material(self,db:Session,material:Material,id:int):
        exist = db.query(Material).filter(Material.id == id).count()
        if(exist):
            db.query(Material).filter(Material.id == id).update({
                Material.image: material.image,
                Material.description: material.description,
                Material.name: material.name
            },synchronize_session=False)
            db.commit()
            return JsonRequest(error="actualizado con exito",value=self.insert_materials_schema(material))
        return JsonRequest(error="no existe el material a actualizar",value=None)


