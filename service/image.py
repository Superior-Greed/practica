from sqlalchemy.orm import Session
from service.generic_crud import BaseService
from models.fences import ImageConstruction
from schema.image import ImageConstructionSchema
from schema.generic import JsonRequest

class ImageConstructionService(BaseService):
    
    @staticmethod
    def insert_image_construction(images:list[ImageConstructionSchema]):
        new_images = list()
        for image in images:
            new_image = ImageConstruction()
            new_image.description = image.description
            new_image.image = image.image
            new_image.id_construction = image.id_construction
            new_images.append(new_image)
        return new_images
    
    @staticmethod
    def exist_image_construction(db:Session, model:ImageConstruction,id:int):
        image = db.query(model).filter(model.id == id)
        if image.count() > 0:
            return image.first()
        return False

    def add_all_image_construction(self,db:Session,images:list[ImageConstruction]):
        return JsonRequest(error="agregadas imagenes con exito",value=self.add_all(db,images))
    
    def remove_image_construction(self,db:Session,id:int):
        exist = self.exist_image_construction(db,ImageConstruction,id)
        if exist == False:
            return JsonRequest(error="no existe imagen",value=None)
        db.query(ImageConstruction).filter(ImageConstruction.id == id).delete()
        db.commit()
        return JsonRequest(error="borrado con exito",value=True)
