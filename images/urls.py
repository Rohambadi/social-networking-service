from django.urls import path
from . import views


app_name = 'images'


urlpatterns = [
    path('post/', views.image_post, name='post'),
    path('image_detail/<int:id>/<slug:slug>/', views.image_detail, name='detail')
]
