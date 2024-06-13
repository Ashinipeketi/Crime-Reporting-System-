from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import MemberForm, CaseForm
from .models import Cases, Members
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .message import send_sms

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
        
        if passwd == conform:
            myuser = User.objects.create_user(username, email, passwd)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.age = age
            myuser.save()
            messages.success(request, "Your account has been successfully created")
            
            # Send welcome SMS
            send_sms(to=email, message="Welcome to the Crime Reporting System!")
            
            return render(request, 'signin.html')
        else:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

    return render(request, "signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user = auth.authenticate(request, username=username, password=passwd)
        if user is not None:
            auth.login(request, user)
            return render(request, "dashboard.html")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "signin.html")
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
            
            # Send SMS notification
            send_sms(to='76XXXXXXXX', message=f"New case reported: {typecrime} at {location}")

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
