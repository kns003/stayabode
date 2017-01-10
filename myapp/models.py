from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

USER_ROLES = (
    ('House Owner', 'HOUSE OWNER'),
    ('Propery Owner', 'PROPERTY OWNER'),
    ('Community Manager', 'COMMUNITY MANAGER'),
)
    
class BroadCast(models.Model):
    message = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    broadcasts = models.ForeignKey(BroadCast, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=200, choices=USER_ROLES)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    
    def as_json(self):
        return dict(
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            phone_number=self.phone_number,
            role=self.role
        )