from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Peep, Profile
from .forms import PeepForm

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
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        peeps = Peep.objects.filter(user_id=pk)

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