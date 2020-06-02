from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages

from .forms import RegisterForm

from .models import Role


select_role = {
    'client': 'Client',
    'user': 'Team Leader'
}


def register(request, usertype:str):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role_name = select_role.get(usertype)
            role = Role.objects.get(name=role_name)
            user.profile.role = role
            user.profile.save()

            messages.success(request, 'Din bruger er blevet oprettet! Du kan nu logge ind.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {"form":form})


def start(request):
    return render(request, 'users/start.html')


def confirm_login(request):
    if request.user.profile.role.name == 'Team Leader':
        return redirect('team-index')
    return redirect('client-index')



def profile_view(request):
    return render(request, 'users/profile.html')
