from django.urls import path
from .views import RegisterAPIView  #,UserLoginView,UserListView

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('get-all-users/', UserListView.as_view(), name='get-all-users'),
]
