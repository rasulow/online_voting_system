from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voterDashboard"))

    
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("adminDashboard"))
            else:
                return redirect(reverse("voterDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }

    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            try:
                user = userForm.save(commit=False)
                voter = voterForm.save(commit=False)
                
                voter.admin = user  # Assign voter to user (admin)

                user.save()  # Save user to the database
                voter.save()  # Save voter to the database
                
                messages.success(request, "Account created. You can login now!")
                return redirect(reverse('account_login'))
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            messages.error(request, "Provided data failed validation")

    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
