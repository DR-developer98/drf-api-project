from django.urls import path
from profiles import views

# 2 views = 2 urlpatronen
# Daar ProfileList een class-View is, moeten we as_view() gebruiken
# /profiles/<int:pk> ===> de profielen worden gekenmekert door een id (primary key)
# die primary key zal weergegeven worden als integer (int)
urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>', views.ProfileDetail.as_view()),
]
