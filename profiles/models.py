from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_jx8tyk'
    )

    class Meta:
        # -created_at betekent dat de profielen op aflopende volgorde 
        # van aanmaakdatum zullen worde gerangschikt
        ordering = ['-created_at']

    def __str__(self):
        # herinnering: dit is de dunder-string methode
        # Bij iedere profielaanaamk zal er een string
        # geretourneerd worden met de naam van de eigenaar
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    # indien een gebruiker gecreëerd is, dan wordt er
    # een Profile gecreëerd. Het Signaal vanuit de User
    # zal de functie create_profile triggeren en dus een Profiel aanmaken
    if created:
        Profile.objects.create(owner=instance)
# dit is het signaal. Iedere keer dat er een gebruiker wordt aangemaakt
# wil ik gelijk een "profiel" aanmaken. 
# sender=User betekent dat "User" hetgeen is, waar we het signaal 
# vandaag zullen krijgen.


post_save.connect(create_profile, sender=User)
