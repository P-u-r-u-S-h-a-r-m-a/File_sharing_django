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
    groups = models.ManyToManyField('auth.Group',related_name='customuser_groups',blank=True,
    )
    user_permissions = models.ManyToManyField('auth.Permission',related_name='customuser_user_permissions',  blank=True,)




