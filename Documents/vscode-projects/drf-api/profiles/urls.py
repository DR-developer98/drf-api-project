from django.urls import path
from profiles import views

# We hebben alleen één view, dus één urlpatroon
# Daar ProfileList een class-View is, moeten we as_view() gebruiken
urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
]
