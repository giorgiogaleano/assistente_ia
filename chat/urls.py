from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'chat'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='chat:new_chat')),
    path('new_chat', views.new_chat, name = 'new_chat'),
]
