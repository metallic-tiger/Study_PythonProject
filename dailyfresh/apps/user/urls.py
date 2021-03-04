from django.conf.urls import url
from user.views import Register,Login

urlpatterns = [
    # url('^register$',views.Register,name= 'Register'),
    # url('^register_headle',views.Register,name= 'register_headle'),
    url('^register$',Register.as_view(),name= 'Register'),
    url('^login$',Login.as_view(),name= 'Login'),
]
