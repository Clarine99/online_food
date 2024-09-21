from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_name
    
    def save (self, *args, **kwargs):
        if self.pk is not None:
            print(f'inside Vendor model: {self.pk}')
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/account_verification_email.html'
                context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                if self.is_approved == True:
                    mail_subject = 'Congratulations! Your restaurant has been approved'
                    
                    send_notification(mail_subject, mail_template, context)
                    
                else:
                    mail_subject = 'We are sorry! you are not eligible'
                    
                user = User.objects.get(pk=self.user.id)
                user.is_approved = self.is_approved
                user.save()
            self.is_approved = True
        super(Vendor, self).save(*args, **kwargs)
