from django.conf.urls import url
from user.views import Register,Login,on_live

urlpatterns = [
    # url('^register$',views.Register,name= 'Register'),
    # url('^register_headle',views.Register,name= 'register_headle'),
    url('^register$',Register.as_view(),name= 'Register'),
    url('^login$',Login.as_view(),name= 'Login'),
    url('^on_live/(?P<Token>.*)$',on_live.as_view(),name='on_live')
]
