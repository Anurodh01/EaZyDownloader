from . import views
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('youtube/',views.youtube,name='youtube'),
    path('instagram/',views.instagram,name='instagram'),
    path('download/',views.download,name='download'),
    path('profile_pic/',views.profile_pic,name='profile_pic'),
    path('post_download/',views.post_download,name='post_download'),
    path('story_download/',views.story_download,name='story_download'),
    path('profile_download/',views.profile_download,name='profile_download')
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    