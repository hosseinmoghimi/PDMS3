from io import BytesIO

from PIL import Image
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.settings import MEDIA_ROOT
from resizeimage import resizeimage
import os
def ResizeImage(image_origin,pk,save_path,*args, **kwargs):
    height=200
    width=200
    file_name="img1"
    
    if 'height' in kwargs:
        height=kwargs['height']
    if 'width' in kwargs:
        width=kwargs['width']
    if 'file_name' in kwargs:
        file_name=kwargs['file_name']
    if image_origin and image_origin is not None:
        # THUMBNAIL_Wkwargs['THUMBNAIL_HEIGHT']
        #Opening the uploaded image
        image = Image.open(image_origin)
    
        output = BytesIO()
        
        #Resize/modify the image
        image = image.resize( (width,height),Image.ANTIALIAS )
        
        #after modifications, save it to the output
        image.save(output, format='JPEG', quality=95)
        
        output.seek(0)
        #change the imagefield value to be the newley modifed image value
        resized_image = InMemoryUploadedFile(output,'ImageField', f"{pk}.jpg", save_path, sys.getsizeof(output), None)
        return resized_image

# class ResizeImage2:
#     def __init__(self,image_path,user=None):
#         image_path=os.path.join(MEDIA_ROOT,str(image_path))
#         self.image_path=image_path
#     def save(self,width,height,save_path):
#         with open(self.image_path, 'r+b') as f:
#             with Image.open(f) as image:
#                 save_path=os.path.join(MEDIA_ROOT,str(save_path))
#                 cover = resizeimage.resize_cover(image, [width, height])
#                 cover.save(save_path, image.format)
#                 return save_path