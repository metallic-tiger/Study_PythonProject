from django.conf.urls import url
from goods import views

urlpatterns = [
    url('^$',views.index,name='index'),
    url('^index',views.index,name='index'),
]
