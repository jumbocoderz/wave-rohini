
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your models here.
class homeGallery(models.Model):
    image_id = models.AutoField
    image_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="main/images")
    desc = models.CharField(max_length=300, default="")
    
    def __str__(self):
        return self.image_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default="")
    phn = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=5000, default="")
    
    def __str__(self):
        return self.name

class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "http://localhost:8000/main/activate/%s" %(self.activation_key)
        context = {
            "activation_key" : self.activation_key,
            "activation_url" : activation_url,
            "user" : self.user.username,
        } 
        message = render_to_string("main/activation_message.txt",context)
        subject = "Activate your email"
        # print(message)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)