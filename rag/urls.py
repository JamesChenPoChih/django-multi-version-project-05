from django.urls import path

from . import views


app_name = 'rag'

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('api/', views.chatbot_api, name='chatbot_api'),
]
