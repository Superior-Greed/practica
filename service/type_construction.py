from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.fences import TypeConstruction,ConstructionMaterial,Construction
from schema.type_construction import TypeConstructionSchema
from schema.generic import JsonRequest
from sqlalchemy import or_,and_

class TypeConstructioService(BaseService):
    
    @staticmethod
    def insert_type_costruction(type_construction:TypeConstructionSchema):
        new_type_construction = TypeConstruction()
        new_type_construction.name = type_construction.name.title()
        new_type_construction.description = type_construction.description
        return new_type_construction
    
    @staticmethod
    def insert_type_costruction_schema(type_construction:TypeConstruction):
        new_type_construction = TypeConstructionSchema(
        name = type_construction.name,
        description = type_construction.description,
        id=type_construction.id
        )
        return new_type_construction
    
    def add_type_construction(self,db:Session,type_construction:TypeConstruction):
        if not type_construction.name.replace(" ",""):
            return JsonRequest(error="no hay nombre",value=None)
        return JsonRequest(error="creado con exito",value=self.insert_type_costruction_schema(self.add(db,type_construction)))
    
    def delete_type_costruction(self,db:Session,id:int):
        db.execute("""delete cm
                    from typeConstructions ty 
                    inner join constructions c on c.id_type_construction = ty.id 
                    inner join constructionMaterials cm  on c.id = cm.costruction_id 
                    where cm.costruction_id  = c.id and ty.id = {0}
                    """.format(id))
        db.execute("""delete i
                    from typeConstructions ty 
                    inner join constructions c on c.id_type_construction = ty.id 
                    inner join images i  on c.id = i.id_construction 
                    where ty.id = {0}""".format(id))
        db.execute("""delete c from typeConstructions ty 
                    inner join constructions c on c.id_type_construction = ty.id 
                    where ty.id = {0}
                    """.format(id))
        type_costruction = db.query(TypeConstruction).filter(TypeConstruction.id == id)
        if type_costruction.count()==0:
            return JsonRequest(error="no esta registrado se tipo de construccion",value=None)      
        type_costruction.delete()
        db.commit()
        return JsonRequest(error="se a eliminado con exito",value=True)
    
    def update_type_construction(self,db:Session,type_construction:TypeConstruction,id:int):
        exist = db.query(TypeConstruction).filter(TypeConstruction.id == id).count() > 0
        if(exist):
            db.query(TypeConstruction).filter(TypeConstruction.id == id).update({
                TypeConstruction.description: type_construction.description,
                TypeConstruction.name: type_construction.name
            },synchronize_session=False)
            db.commit()
            return JsonRequest(error="actualizado con exito",value=self.insert_type_costruction_schema(type_construction))
        return JsonRequest(error="no existe el typo de constructionn a actualizar",value=None)


