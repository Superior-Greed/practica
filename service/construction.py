from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.fences import Construction,ConstructionMaterial,TypeConstruction,ImageConstruction,Material
from schema.construction import ConstructionSchema
from schema.generic import JsonRequest
from sqlalchemy import or_,and_

class ConstructionService(BaseService):
    
    @staticmethod
    def insert_construction(construction:ConstructionSchema):
        new_construction = Construction()
        new_construction.id_type_construction = construction.id_type_construction
        new_construction.final_date  = construction.final_date
        new_construction.init_date = construction.init_date
        new_construction.price = construction.price
        new_construction.name = construction.name.title()
        return new_construction
    
    def add_construction(self,db:Session,construction:Construction):
        if not construction.name.replace(" ",""):
            return JsonRequest(error="el nombre esta vacio", value=None)
        type_construction = False
        if construction.id_type_construction > 0:
            type_construction = db.query(TypeConstruction).filter(TypeConstruction.id == construction.id_type_construction).count() > 0
        if type_construction == False:
            return JsonRequest(error="no existe el tipo construccion", value=None)
        return JsonRequest(error="construccion agregada con exito",value=self.add(db,construction))
    
    def delete_construction(self,db:Session,id:int):
        exist_construction = db.query(Construction).filter(Construction.id == id)
        if exist_construction.count()>0:
            construction_material = db.query(ConstructionMaterial).filter(ConstructionMaterial.costruction_id == id)
            if construction_material.count() > 0:
                construction_material.delete()
            db.query(ImageConstruction).filter(ImageConstruction.id_construction == id).delete()
            exist_construction.delete()
            db.commit()
            return JsonRequest(error="construccion eliminada con exito",value=True)
        return JsonRequest(error="construccion no existe",value=True)
    
    def update_construction(self,db:Session,construction:Construction, id:int):
        exist_construction = db.query(Construction).filter(Construction.id == id)
        if exist_construction.count()>0:
            if construction.id_type_construction > 0:
                type_construction = db.query(TypeConstruction).filter(TypeConstruction.id == construction.id_type_construction).count() > 0
                if type_construction == False:
                    return JsonRequest(error="no agregaste el tipo de construccion o no existe",value=True)
            exist_construction.update({
                Construction.id_type_construction: construction.id_type_construction,
                Construction.final_date: construction.final_date,
                Construction.init_date: construction.init_date,
                Construction.name : construction.name,
                Construction.price:construction.price
            },synchronize_session=False)
            db.commit()
            return JsonRequest(error="connstruccion actualizada con exito",value=True)
        return JsonRequest(error="no existe la construccion",value=None)

    def add_construction_material(self,db:Session,construction_id:int,material_id:int):
        exist_construction = db.query(ConstructionMaterial).filter(and_(ConstructionMaterial.costruction_id == construction_id , ConstructionMaterial.material_id == material_id)).count()>0
        if exist_construction:
            JsonRequest(error="ya existe",value=True)
        construction_material = ConstructionMaterial()
        construction_material.costruction_id = construction_id
        construction_material.material_id = material_id
        return JsonRequest(error="agregado con exito", value= self.add(db,construction_material))
    
    def delete_construction_material(self,db:Session,construction_id:int,material_id:int):
        construction_material = db.query(ConstructionMaterial).filter(and_(ConstructionMaterial.material_id == material_id , ConstructionMaterial.costruction_id == construction_id))
        if  construction_material.count()> 0:
            construction_material.delete()
            db.commit()
            return JsonRequest(error="borrado con exito",value=True)
        return JsonRequest(error="no se encontro el material o la construction a borrar",value=None)
        
    def all_construction(self,db:Session):
        return db.query(Construction,TypeConstruction,ImageConstruction,Material).join(Construction.materials).join(Construction.type_construction).join(Construction.images).all()
    
    def filter_construction(self,db:Session,id:int):
        return db.query(Construction,TypeConstruction,ImageConstruction,Material).join(Construction.materials).join(Construction.type_construction).join(Construction.images).filter(Construction.id == id).first()
    
    def filter_construction_material(self,db:Session,id:int):
        return db.query(ConstructionMaterial).filter(ConstructionMaterial.costruction_id == id).all()