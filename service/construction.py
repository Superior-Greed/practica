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
        new_construction.name = construction.name.title()
        return new_construction
    
    def add_construction(self,db:Session,construction:Construction):
        if not construction.name.replace("  ",""):
            return JsonRequest("el nombre esta vacio",None)
        return self.add(db,construction)
    
    def delete_construction(self,db:Session,id:int):
        exist_construction = db.query(Construction).filter(Construction.id == id)
        if exist_construction.count()>0:
            construction_material = db.query(ConstructionMaterial).filter(ConstructionMaterial.costruction_id == id)
            if construction_material > 0:
                construction_material.delete()
            exist_construction.delete()
            return JsonRequest("construccion eliminada con exito",True)
        return JsonRequest("construccion no existe",True)
    
    def update_construction(self,db:Session,construction:Construction, id:int):
        exist_construction = db.query(Construction).filter(Construction.id == id).count()
        if exist_construction>0:
            self.update(db,construction,id)
            return JsonRequest("connstruccion actualizada con exito",True)
        return JsonRequest("no existe la construccion",None)

    def add_construction_material(self,db:Session,construction_id:int,material_id:int):
        exist_construction = db.query(ConstructionMaterial).filter(ConstructionMaterial.costruction_id == construction_id & ConstructionMaterial.material_id == material_id).count()>0
        if exist_construction:
            JsonRequest("ya existe",True)
        construction_material = ConstructionMaterial()
        construction_material.costruction_id = construction_id
        construction_material.material_id = material_id
        return JsonRequest("agregado con exito",  self.add(db,construction_material))
    
    def remove_construction_material(self,db:Session,construction_id:int,material_id:int):
        construction_material = db.query(ConstructionMaterial).filter(ConstructionMaterial.material_id == material_id & ConstructionMaterial.costruction_id == construction_id)
        if  construction_material.count()> 0:
            construction_material.delete()
            return JsonRequest("borrado con exito",True)
        return JsonRequest("no se encontro el material o la construction a borrar",None)
        
