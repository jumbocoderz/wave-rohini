import hashlib
import random
import re

from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import homeGallery,Contact,EmailConfirmed
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    allImages = homeGallery.objects.all()
    count = homeGallery.objects.count()
    n = len(allImages)

    params = { 'allImages' : allImages , 'count' : range(1,count)}
    return render(request, 'main/index.html', params)

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phn=phone, desc=desc)
        contact.save()
    return render(request, 'main/contact.html')

def handleSignup(request):
    if request.method=="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        '''  checking of data for signup '''
        if len(username)>30:
            messages.error(request, "Username must be under 30 characters")
            return redirect('home')
        
        user_exist = User.objects.filter(username=username)
        if len(user_exist)>0:
            messages.error(request, "Username exist already")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must only contain letters and numbers")
            return redirect('home')

        email_exist = User.objects.filter(email=email)
        if len(email_exist)>0:
            messages.error(request, "Email used before")
            return redirect('home')

        if pass1!=pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your account has been created successfully, Please check your email and confirm your account")
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=myuser)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            base,domain = str(myuser.email).split("@")
            activation_key = hashlib.sha1((short_hash+base).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email() 
        return redirect('home')

    else:
        return HttpResponse("404 ...... NOT FOUND")


def handleLogin(request):
    if request.method=="POST":
        username = request.POST['loginUser']
        password = request.POST['loginPass']
        user = authenticate(username=username, password=password)

        if user is not None:
            checking_confirmed = EmailConfirmed.objects.filter(user=user)
            if len(checking_confirmed)>0 and checking_confirmed[0].confirmed==True:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('home')
            else:
                messages.error(request, "Please confirm your account by clicking the activation link. Activation link sent to your email")
                return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

    else:
        return HttpResponse("404 ...... NOT FOUND")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.error(request, "You are using wrong activation link")
            return redirect('home')

        if instance is not None and not instance.confirmed:
            messages.success(request,"Confirmation Succesful! Welcome.")
            instance.confirmed = True
            instance.save()
        elif instance is not None and instance.confirmed:
            messages.success(request, "Your account confirmed already")
        else:
            page_message=""

        return redirect('home')
    else:
        raise Http404
    