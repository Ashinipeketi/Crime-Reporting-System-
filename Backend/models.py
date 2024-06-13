# crimeapp/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PoliceManager(BaseUserManager):
        def create_user(self, police_id, email, password=None):
        if not email:
        raise ValueError("Users must have an email address")
            if not police_id:
            raise ValueError("Users must have a police ID")

                user = self.model(
                           email=self.normalize_email(email),
                           police_id=police_id,
                       )
                       user.set_password(password)
                       user.save(using=self._db)
                       return user

                              def create_superuser(self, police_id, email, password=None):
                              user = self.create_user(
                                         email=email,
                                         police_id=police_id,
                                         password=password,
                                     )
                                     user.is_admin = True
                                                     user.save(using=self._db)
                                                     return user

                                                             class Police(AbstractBaseUser):
                                                                 police_id = models.CharField(max_length=10, unique=True)
                                                                         email = models.EmailField(max_length=255, unique=True)
                                                                                 is_active = models.BooleanField(default=True)
                                                                                         is_admin = models.BooleanField(default=False)

                                                                                                 objects = PoliceManager()

                                                                                                         USERNAME_FIELD = 'email'
                                                                                                                 REQUIRED_FIELDS = ['police_id']

                                                                                                                         def __str__(self):
                                                                                                                         return self.email

                                                                                                                                 def has_perm(self, perm, obj=None):
                                                                                                                                 return True

                                                                                                                                         def has_module_perms(self, app_label):
                                                                                                                                         return True

                                                                                                                                                 @property
                                                                                                                                                 def is_staff(self):
                                                                                                                                                 return self.is_admin

# Existing models
                                                                                                                                                         class Members(models.Model):
                                                                                                                                                             fname = models.CharField(max_length=50)
                                                                                                                                                                     lname = models.CharField(max_length=100)
                                                                                                                                                                             email = models.EmailField(max_length=200)
                                                                                                                                                                                     passwd = models.CharField(max_length=50)
                                                                                                                                                                                             conform = models.CharField(max_length=50)
                                                                                                                                                                                                     age = models.IntegerField()

                                                                                                                                                                                                             def __str__(self):
                                                                                                                                                                                                             return self.email + ' ' + self.passwd

                                                                                                                                                                                                                     crimes = [('theft', 'Theft'), ('fraud', 'Fraud'), ('robbery', 'Robbery'), ('harrsing', 'Harrsing')]

                                                                                                                                                                                                                             class Cases(models.Model):
                                                                                                                                                                                                                                 name = models.CharField(max_length=50)
                                                                                                                                                                                                                                         location = models.CharField(max_length=200)
                                                                                                                                                                                                                                                 typecrime = models.CharField(max_length=10, choices=crimes)
                                                                                                                                                                                                                                                         Description = models.TextField()

                                                                                                                                                                                                                                                                 def __str__(self):
                                                                                                                                                                                                                                                                 return self.name + '' + self.location + self.typecrime + self.Description
