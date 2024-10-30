from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from datetime import datetime


class Passport(models.Model):
    GENDER_TYPE = (('M', 'Male'), ('F', 'Female'))
    passport_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(default='M', choices=GENDER_TYPE, max_length=6)
    judicial = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.passport_id} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        today = datetime.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def formatted_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    
    
    

class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        user = CustomUser(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with `is_staff=True`, `is_superuser=True`, and `is_active=True` by default.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", 1)
        extra_fields.setdefault("last_name", "System")
        extra_fields.setdefault("first_name", "Administrator")

        assert extra_fields["is_staff"], "Superuser must have is_staff=True."
        assert extra_fields["is_superuser"], "Superuser must have is_superuser=True."
        return self._create_user(username, password, **extra_fields)



class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Voter"))
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=2, choices=USER_TYPE, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + " " + self.first_name
    
    def get_full_name(self):
        return self.last_name + " " + self.first_name
    
    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def formatted_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def save(self, *args, **kwargs):
        try:
            passport = Passport.objects.get(passport_id=self.username)
            self.first_name = passport.first_name
            self.last_name = passport.last_name
        except Passport.DoesNotExist:
            raise ValidationError(f"Username '{self.username}' does not exist in the Passport model.")
        
        super().save(*args, **kwargs)
        
