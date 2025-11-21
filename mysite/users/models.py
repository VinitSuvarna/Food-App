from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# -----------------------------------------------------------------------------------

class ProfileModel(models.Model):
    profile_username = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pic.jpg', upload_to='profile_pictures')
    location = models.CharField(max_length=100)
    USER_TYPES_CHOICES = (
        ("SELECT", "SELECT"),
        ("RESTAURANT", "RESTAURANT"),
        ("CUSTOMER", "CUSTOMER"),
        ("ADMIN", "ADMIN"),
    )
    user_type = models.CharField(choices=USER_TYPES_CHOICES, default="SELECT")
    def __str__(self):
        return self.profile_username.username
    