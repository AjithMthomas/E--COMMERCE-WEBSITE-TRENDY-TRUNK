from django.db.models. signals import post_save
from.models import Account,UserProfile
from django.dispatch import receiver

# functions
# to create userprofile for each time a user is created
@receiver(post_save,sender=Account)
def createProfile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

#to save profile when when each user object is created
@receiver(post_save,sender=Account)
def saveUserProfile(sender,instance,**kwargs):
    instance.userprofile.save()