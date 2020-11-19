from django.contrib import admin
from django.urls import path,include
from dona import views
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import re_path
from django.conf import settings
from django.conf.urls import url

app_name = 'dona'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('monthly_ranking/', views.monthly_ranking, name='monthly_ranking'), 
    path('yearly_ranking/', views.yearly_ranking, name='yearly_ranking'), 
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('message/', views.message, name='message'),
    path('mypage/', views.mypage, name='mypage'),
    path('help/', views.HelpListView.as_view(), name='help_board_list'),
    path('help/<int:id>', views.detail, name='detail'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^mypage/townsearch/$', views.townsearch, name="townsearch"),
    url(r'^mypage/townenroll/$', views.townenroll, name="townenroll"),
    path('summernote/', include('django_summernote.urls')),
    url(r'^posts/new/$', views.new_post, name='new_post'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT})
]