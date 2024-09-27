from django.db import models
from django.contrib.auth.models import User
# Create your models here.
User.add_to_class('action_verify', models.BooleanField(null=False,default=False))
User.add_to_class('verify', models.BooleanField(null=False,default=False))

User.add_to_class('tocken',models.TextField(null=True,blank=True))
