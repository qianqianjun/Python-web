from django.urls import path
from . import views

#为URL名称设置命名空间，在html中设置{%url%}时写为“polls:detail”，避免有多个应用下有同名的url时,django不知道对应哪个url
app_name='polls'
urlpatterns=[
   # path('postKeyword',views.postKeyword),
    path('goods/<str:kw>',views.goods,name='goods'),
    path('',views.index,name='index'),
    path('<int:question_id>/',views.detail,name='detail'),
    path('<int:question_id>/results/',views.results,name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
]