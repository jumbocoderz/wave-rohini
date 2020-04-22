from django.contrib import admin

# Register your models here.
from . models import homeGallery, Contact, EmailConfirmed

admin.site.register(homeGallery)
admin.site.register(Contact)
admin.site.register(EmailConfirmed)

