from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Peep, Profile
from .forms import MyUserChangeForm, PeepForm, SignUpForm, ChangePasswordForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


def home(request):
    if request.user.is_authenticated:
        form = PeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                peep = form.save(commit=False)
                peep.user = request.user
                peep.save()
                messages.success(request, ('Your Peep Has Been Posted..'))
                return redirect('home')


        peeps = Peep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'peeps':peeps, 'form':form})
    else:
        peeps = Peep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'peeps':peeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page..'))
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()
        # Return Message
        messages.success(request, (f'You have unfollowed {profile.user.username}!'))
        return redirect('profile', pk=request.user.pk)
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Follow the user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()
        # Return Message
        messages.success(request, (f'You have followed {profile.user.username}!'))
        return redirect('profile', pk=request.user.pk)
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        peeps = Peep.objects.filter(user_id=pk).order_by("-created_at")

        #Post Form Logic
        if request.method == 'POST':
            #Get current user ID
            current_user_profile = request.user.profile
            #Get form data
            action = request.POST['follow']
            #Decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            #Save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {'profile':profile, 'peeps':peeps})
    else:
        messages.success(request, ('You Must Be Logged In To View This Page..'))
        return redirect('home')    

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles":profiles})
        else:
            messages.success(request, ("That's not your profile page!"))
            return redirect('home')
            
    else:
        messages.success(request, ('You Must Be Logged In To View This Page..'))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles":profiles})
        else:
            messages.success(request, ("That's not your profile page!"))
            return redirect('home')
            
    else:
        messages.success(request, ('You Must Be Logged In To View This Page..'))
        return redirect('home')

def my_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', pk=request.user.pk)
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You Have Been Logged In! Get PEEPING!'))
            return redirect('home')
        else:
            messages.success(request, ('Loggin failed. Please try again..'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You Have Been Logged Out!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']
            #Login User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registered! Welcome!'))
            return redirect('home')
            
    return render(request, "register.html", {'form':form})

def update_user(request):
     if request.user.is_authenticated:
         profile_user = Profile.objects.get(user__id=request.user.id)

         if request.method == 'POST':
             user_form = MyUserChangeForm(request.POST, instance=request.user)
             profile_form = ProfileForm(request.POST, request.FILES, instance=profile_user)
             if user_form.is_valid() and profile_form.is_valid():
                 user_form.save()
                 profile_form.save()
                 messages.success(request, ('Profile Updated'))
                 return redirect('update_user')
         else:
             user_form = MyUserChangeForm(instance=request.user)
             profile_form = ProfileForm(instance=request.user.profile)
             return render(request, 'update_user.html', {"user_form":user_form, "profile_form":profile_form})
     else:
         messages.success(request, ('You are not Logged In!'))
         return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('Password Updated'))
                login(request, request.user)
                return redirect('profile', pk=request.user.pk)
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(request.user)
            return render(request, 'update_password.html', {"form":form})
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('login')
    
def peep_like(request, pk):
    if request.user.is_authenticated:
        peep = get_object_or_404(Peep, id=pk)
        if peep.likes.filter(id=request.user.id):
            peep.likes.remove(request.user)
        else:
            peep.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('home')
    
def peep_show(request, pk):
    peep = get_object_or_404(Peep, id=pk)
    if peep:
        return render(request, 'show_peep.html', {"peep":peep})
    else:
        messages.success(request, ('That Peep Does Not Exist!'))
        return redirect('home')
    
def delete_peep(request, pk):
    if request.user.is_authenticated:
        peep = get_object_or_404(Peep, id=pk)
        # Check to see if you own the peep
        if request.user.username == peep.user.username:
            # Delete the peep
            peep.delete()
            messages.success(request, ('Peep Deleted!'))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ('Denied!'))
            return redirect('home')
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect(request.META.get("HTTP_REFERER"))
    
def edit_peep(request, pk):
    if request.user.is_authenticated:
        peep = get_object_or_404(Peep, id=pk)
        # Check to see if you own the peep
        if request.user.username == peep.user.username:
            form = PeepForm(request.POST or None, instance=peep)
            if request.method == "POST":
                if form.is_valid():
                    peep = form.save(commit=False)
                    peep.user = request.user
                    peep.save()
                    messages.success(request, ('Your Peep Has Been Updated..'))
                    return redirect('home')
            else:
                return render(request, 'edit_peep.html', {"form":form, "peep":peep})
        else:
            messages.success(request, ('Denied!'))
            return redirect('home')
    else:
        messages.success(request, ('You are not Logged In!'))
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = Peep.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search.html', {})
    
def search_user(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search':search, 'searched':searched})
    else:
        return render(request, 'search_user.html', {})