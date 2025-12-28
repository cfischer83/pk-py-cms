from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User
from .forms import LoginForm, RegisterForm, ProfileForm


class LoginView(View):
    """Handle user login."""
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_display_name()}!')
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Handle user logout."""
    
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('core:home')
    
    def post(self, request):
        return self.get(request)


class RegisterView(View):
    """Handle user registration."""
    template_name = 'users/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = User.Role.CONTRIBUTOR
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('core:home')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display user profile."""
    template_name = 'users/profile.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile."""
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)
