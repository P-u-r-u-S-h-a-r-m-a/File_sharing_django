from django.db import models
from user.models import BaseModel,CustomUser
from .validators import validate_file_type
from django.utils import timezone


class FileUpload(BaseModel):
    file_name=models.CharField(max_length=25,unique=True)
    file = models.FileField(upload_to='uploads/', validators=[validate_file_type])
    uploaded_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        if not self.id:
            self.created_at=timezone.now()
        self.updated_at = timezone.now()
        super(FileUpload, self).save(*args, **kwargs)