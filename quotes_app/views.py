from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum

def index(request):
    if  'current_user' in request.session:
        return redirect("/quotes") 
    return render (request, 'index.html')

def login(request):
    if request.method == "POST":   
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        current_user = User.objects.get(email = request.POST['email'])
        request.session['current_user'] = current_user.id
        return redirect('/quotes')            
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    if request.method =="POST":
        errors = User.objects.user_validator(request.POST)        
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pwhash
        )
        request.session['current_user'] = new_user.id
        return redirect('/quotes')
    else:
        return redirect("/")

def quotes(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
            'quotes' : Quote.objects.all,                       
        }
    return render(request, 'quotes.html', context)

def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)        
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    user = User.objects.get(id = request.session['current_user'])
    quote = Quote.objects.create(
        author = request.POST['author'],
        quote = request.POST['quote'],
        uploaded_by = user,
    )
    return redirect('/quotes')

def delete_quote(request, id):
    quote = Quote.objects.get(id = id)
    quote.delete()
    return redirect("/quotes")

def like_quote(request, id):    
    user = User.objects.get(id = request.session['current_user'])
    quote = Quote.objects.get(id=id)
    if user.id in quote.liked_by.all():
        return False
    else:
        quote.liked_by.add(user)
        return redirect("/quotes")

def user(request, id):
    if  'current_user' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=id)
        quotes = user.uploader.all()
        current = User.objects.get(id= request.session['current_user'])        
        context = {
            'user' : user,
            'quotes' : quotes,  
            'current_user': current,                     
        }
    return render(request, 'user.html', context)

def edit(request, id):
    if request.method == "GET":
        context = {
            "user" : User.objects.get(id = request.session['current_user']),                             
        }
        return render (request, 'edit.html', context)
    else:
        errors = User.objects.edit_validator(request.POST)  
        user = User.objects.get(id=id)      
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{user.id}')
        user = User.objects.get(id=id)
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.save()  
        return redirect(f'/edit/{user.id}')
