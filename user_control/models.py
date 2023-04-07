from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from message_control.models import GenericFileUpload
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS=["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        ordering = ("created_at",)
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,related_name='user_profile', on_delete= models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    caption = models.CharField(max_length=250)
    about = models.TextField()
    profile_picture = models.ForeignKey(
        GenericFileUpload, related_name="user_image", on_delete=models.SET_NULL, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("created_at",)
        
        
class Favorite(models.Model):
    user = models.OneToOneField(CustomUser, related_name="user_favorite", on_delete=models.CASCADE)
    favorite = models.ManyToManyField(CustomUser, related_name="user_favoured")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} + {self.favorite.username}"
    
    class Meta:
        ordering = ("created_at",)    
    
