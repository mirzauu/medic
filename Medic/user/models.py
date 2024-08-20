from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class TestDetails(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='test_details')
    sample_collected_at = models.DateTimeField()
    age = models.PositiveIntegerField()
    doctor = models.CharField(max_length=255)

    def __str__(self):
        return f"Test for {self.user_profile.user.username} on {self.sample_collected_at}"    