from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import RegisterForm, UpdateProfileForm, UpdateUserForm
from .models import Role
from django.contrib.auth.models import User

import os


select_role = {
    'client': 'Client',
    'employee': 'Team'
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
    ctx = {}
    if os.environ.get('DJANGO_ENV'):
        ctx['django_env'] = os.environ.get('DJANGO_ENV')
    ctx['django_env'] = 'literally nothing found, fool'
    return render(request, 'users/start.html', context=ctx)


@login_required
def confirm_login(request):
    role = request.user.profile.role

    if role.name == 'Team':     # User has no team
        # messages.info(request, 'Du har ikke noget hold. Du bedes derfor oprette et, før du kan tilgå resten af siden.Du kan også få en af dine kollegaer til at tilmelde dig et eksisterende hold.')
        return redirect('team-new-user')
    elif role.name == 'Team Member' or role.name == 'Team Leader':  # User is either Team Leader or Team Member
        team = request.user.profile.team
        return redirect(reverse('team-detail', kwargs={
            'pk': team.id,
            'slug': team.slug
        }))
    # User is Client.
    return redirect('client-projects')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = kwargs.get('object')
        ctx['projects'] = user.profile.project_set.all()
        ctx['owns_projects'] = user.owner.all()
        ctx['leads_projects'] = user.leader.all()
        ctx['no_projects_msg'] = 'Der blev ikke fundet nogen projekter under denne kategori.'
        if kwargs.get('object').pk is self.request.user.pk:
            ctx['is_current_user'] = True
        return ctx


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)
        ctx = {
            "u_form":u_form,
            "p_form":p_form
        }
        return render(request, 'users/user_update.html', context=ctx)

    def post(self, request, **kwargs):
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Din profil er blevet opdateret!")
        return redirect(reverse('user-profile', kwargs={"pk":request.user.pk}))
