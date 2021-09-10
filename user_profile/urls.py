from django.urls import path
from user_profile import views


urlpatterns = [
    path('', views.UserProfileRecordView.as_view()),
    path('deposit/<int:pk>/<int:amount>/', views.deposit),
]
