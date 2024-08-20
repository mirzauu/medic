from django.urls import path
from .views import LoginView,UserDetailsView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user/details/', UserDetailsView.as_view(), name='user_details'),
]
