from django.urls import path
from likes import views

urlspatterns = [
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
]
