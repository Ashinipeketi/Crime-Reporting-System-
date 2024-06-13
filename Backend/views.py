# crimeapp/views.py

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import MemberForm, CaseForm, PoliceRegistrationForm, PoliceLoginForm
from .models import Cases, Members
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        conform = request.POST.get('conform')
        age = request.POST.get('age')
        username = request.POST.get('username')
        myuser = User.objects.create_user(username, email, passwd)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.age = age
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return render(request, 'signin.html')
    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user1 = auth.authenticate(request, username=user, password=passwd)
        if user1 is not None:
            auth.login(request, user1)
            return render(request, "case_register.html")
        else:
            messages.error(request, "Password or email is incorrect")
            return render(request, "index.html")
    return render(request, "signin.html")

def report(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        typecrime = request.POST.get('typecrime')
        Description = request.POST.get('Description')
        if name and location and typecrime and Description:
            new_case = Cases(name=name, location=location, typecrime=typecrime, Description=Description)
            new_case.save()
            return render(request, 'index.html')
        else:
            return HttpResponse("All fields are required.")
    return render(request, 'case_register.html')

def fetch(request):
    all_cases = Cases.objects.all()
    return render(request, 'fetch.html', {'all': all_cases})

def delete(request, username):
    get_case = get_object_or_404(Cases, name=username)
    get_case.delete()
    return render(request, 'index.html')

def update(request, case_id):
    case = Cases.objects.get(pk=case_id)
    form = CaseForm(instance=case)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return render(request, "index.html")
    context = {'form': form}
    return render(request, 'update.html', context)

# Police Views
def police_register(request):
    if request.method == 'POST':
        form = PoliceRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('police_login')
    else:
        form = PoliceRegistrationForm()
    return render(request, 'police_register.html', {'form': form})

def police_login(request):
    if request.method == 'POST':
        form = PoliceLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = PoliceLoginForm()
    return render(request, 'police_login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

