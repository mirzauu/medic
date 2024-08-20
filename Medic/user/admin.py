from django.contrib import admin
from .models import UserProfile,TestDetails,Doctor,Tests


admin.site.register(UserProfile)  
admin.site.register(TestDetails)  
admin.site.register(Doctor)  
admin.site.register(Tests)  
