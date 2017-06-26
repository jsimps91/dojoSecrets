from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Secret
from django.db.models import Count
import re
import datetime
from django.core.exceptions import ObjectDoesNotExist
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    isValid = True
    if(len(request.POST['first_name']) < 2):
        messages.add_message(request, messages.ERROR, "Name must be at least 2 characters!")
        isValid = False
    if(request.POST['first_name'].isalpha() == False): 
        messages.add_message(request, messages.ERROR, "Name must contain letters only!")
        isValid = False
    if(len(request.POST['last_name']) < 2):
        messages.add_message(request, messages.ERROR, "Name must be at least 2 characters!")
        isValid = False
    if(request.POST['last_name'].isalpha() == False): 
        messages.add_message(request, messages.ERROR, "Name must contain letters only!")
        isValid = False       
    if(not EMAIL_REGEX.match(request.POST['email'])):
        messages.add_message(request, messages.ERROR, "Please enter a valid email address")
        isValid = False   
    if(len(request.POST['password']) < 8):
        messages.add_message(request, messages.ERROR, "Password must be at least 8 characters!")
        isValid = False
    if(len(request.POST['password']) > 14):
        messages.add_message(request, messages.ERROR, "Password cannot be longer than 14 characters!")
        isValid = False    
    if(request.POST['password'] != request.POST['password_conf']):
        messages.add_message(request, messages.ERROR, "Passwords must match!") 
        isValid= False         
    if not isValid:
        return redirect ('/')    

    User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'], email = request.POST['email'], password = request.POST['password'])
    request.session['current_user'] = User.objects.get(email= request.POST['email']).id
    return redirect ("/success")

def success(request):
    context = {}
    if "current_user" in request.session.keys():
        context = {
            "user" : User.objects.get(pk=request.session['current_user']),
            "posts" : Secret.objects.all().annotate(num_likes=Count('likes')).order_by('-created_at'),
            "you" : Secret.objects.filter(user_id=(User.objects.get(pk=request.session['current_user']))),
         }
    print Secret.objects.all()
    return render(request, 'first_app/secrets.html', context)     
def login(request):
    try:
        users = User.objects.get(email=request.POST['email'], password=request.POST['password'])
    except ObjectDoesNotExist:
        messages.add_message(request, messages.INFO, "Invalid username or password!")
        return redirect('/')    
    else:
        context = {}
        request.session['current_user'] = User.objects.get(email=request.POST['email'], password=request.POST['password']).id
        if "current_user" in request.session.keys():
            return redirect('/success') 
def postSecret(request):
    Secret.objects.create(message=request.POST['secret'], user_id=(User.objects.get(pk=request.session['current_user'])))
    return redirect ('/success')

def logout(request):
    request.session.clear() 
    messages.add_message(request, messages.INFO, "Successfully logged out")
    return redirect ('/')

def like(request, like_id, user_id):
    secret = Secret.objects.get(id=like_id)
    user = User.objects.get(id=user_id)
    if user not in secret.likes.all():
        secret.likes.add(user)
    return redirect ('/success')

def delete(request, id):
    Secret.objects.get(id=id).delete()
    return redirect ('/success') 

def unlike(request, like_id, user_id):
    secret = Secret.objects.get(id=like_id)
    user = User.objects.get(id=user_id)
    if user in secret.likes.all():
        secret.likes.remove(user)
    return redirect ('/success')


def mostPopular(request):
    context = {
        "user" : User.objects.get(pk=request.session['current_user']),
        "posts" : Secret.objects.all().annotate(num_likes=Count('likes')).order_by('- num_likes'),
        "you" : Secret.objects.filter(user_id=(User.objects.get(pk=request.session['current_user']))),
    }
    return render (request, 'first_app/popular.html', context)

