from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#为URL名称设置命名空间，在html中设置{%url%}时写为“polls:detail”，避免有多个应用下有同名的url时,django不知道对应哪个url
app_name='polls'
urlpatterns=[
    path('postKeyword',views.postKeyword),
    path('goods/<str:kw>',views.goods,name='goods'),
    path('',views.index,name='index'),
    path('barrage',views.barrage,name='barrage'),
]
urlpatterns += staticfiles_urlpatterns()
