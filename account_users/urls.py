
from django.urls import path
from account_users.views import login,signup,log_out

urlpatterns = [
    path('login',login,name='login'),
    path('signup',signup,name='signup'),
    path('logout',log_out,name='logout')
]
