from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserProfile, User
import qrcode
@receiver(post_save,sender=User)   
def created_profile_receiver (sender, instance, created, **kwargs):
    if created:
        
        UserProfile.objects.create(user=instance)
        
    else:
        try:
            print(created, "instance:",instance)
            user_profile = UserProfile.objects.get(user=instance)
            print("user is updated",user_profile)
            user_profile.save()
        except:
            print('jsdkfj')
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, 'this user is being saved')