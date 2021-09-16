from django.urls import path
from user_profile import views


urlpatterns = [
    path('', views.UserProfileView.as_view()),
    path('<int:pk>/', views.UserProfileView.as_view()),
    path('deposit/<int:pk>/<int:amount>/', views.deposit),
    path('buy/<int:pk>/<int:amount>/', views.buy),
]
