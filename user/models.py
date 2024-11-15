from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class BaseModel(models.Model):
    created_at=models.DateTimeField(editable=False)
    updated_at=models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.created_at=timezone.now()
        self.updated_at=timezone.now()
        return super(BaseModel,self).save(*args,**kwargs)
    class Meta:
        abstract=True



class CustomUser(AbstractUser,BaseModel):
    user_type_choices=(
        ('OP','Operation user'),
        ('CL','Client user')
    )
    user_type=models.CharField(max_length=2,choices=user_type_choices)


class FileUpload(BaseModel):
    file=models.FileField(upload_to='uploads/')
    uploaded_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#    uploded_time=models.DateTimeField()

    def save(self,*args,**kwargs):
        if not self.id:
            self.created_at=timezone.now()
        self.updated_at = timezone.now()
        super(FileUpload, self).save(*args, **kwargs)