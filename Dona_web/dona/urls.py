from django.contrib import admin
from django.urls import path,include
from dona import views
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import re_path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

app_name = 'dona'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('Pranking/', views.person_ranking, name='person_ranking'), 
    path('Rranking/', views.region_ranking, name='region_ranking'), 
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('message/', views.message, name='message'),
    path('message_make/<int:id>', views.message_make, name='message_make'),
    path('region_message_make/<int:id>', views.region_message_make, name='region_message_make'),
    path('message_delete/<int:msg_id>', views.message_delete, name='message_delete'),
    path('message_send/<int:msg_id>/', views.add_content_to_msg, name='add_content_to_msg'),
    path('help_clear/<int:msg_id>', views.help_clear, name='help_clear'),
    path('mypage/', views.mypage, name='mypage'),
    path('help/', views.HelpListView.as_view(), name='help_board_list'),
    path('help/delete/<int:id>/', views.delete, name='delete'),
    path('help/<int:id>', views.detail, name='detail'),
    path('region_board/', views.RegionListView.as_view(), name='region_board_list'),
    path('region_board/delete/<int:id>/', views.region_delete, name='region_delete'),
    path('region_board/<int:id>', views.region_detail, name='region_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^mypage/townsearch/$', views.townsearch, name="townsearch"),
    url(r'^mypage/townenroll/$', views.townenroll, name="townenroll"),
    path('summernote/', include('django_summernote.urls')),
    url(r'^posts/new/$', views.new_post, name='new_post'),
    url(r'^region_posts/new/$', views.region_new_post, name='new_post'),
    path('help/<int:help_board_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('region_posts/<int:region_board_id>/comment/', views.add_comment_to_region_post, name='add_comment_to_region_post'),


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT})
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)