from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email,username, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email = models.EmailField(verbose_name='Email Address',max_length=40,unique=True)
    username = models.CharField(verbose_name='username',max_length=20,unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    
    REQUIRED_FIELDS=['username']
    USERNAME_FIELD = 'email'
    objects = UserManager()
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        
        
        return True

    def has_module_perms(self, app_label):
        
        return True


