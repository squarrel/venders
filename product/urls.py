from django.urls import path
from product import views


urlpatterns = [
    path('', views.ProductRecordView.as_view()),
    path('<int:pk>/', views.ProductRecordView.as_view()),
]

