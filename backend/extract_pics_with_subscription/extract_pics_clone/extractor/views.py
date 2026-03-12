from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from .models import Extraction, Image
from .utils import extract_images_from_url
import threading


class HomeView(View):
    def get(self, request):
        context = {}
        
        # If user is authenticated, show recent extractions
        if request.user.is_authenticated:
            recent_extractions = Extraction.objects.filter(
                user=request.user
            ).order_by('-timestamp')[:3]
            context['recent_extractions'] = recent_extractions
        
        return render(request, 'extractor/home.html', context)


class ExtractView(View):
    def post(self, request):
        url = request.POST.get('url')
        if not url:
            messages.error(request, 'Please provide a valid URL.')
            return redirect('home')
        
        # Create extraction object
        extraction = Extraction.objects.create(
            user=request.user if request.user.is_authenticated else None,
            url=url,
            status='pending'
        )
        
        # Start image extraction in background thread
        def extract_in_background():
            try:
                extract_images_from_url(url, extraction)
            except Exception as e:
                print(f"Background extraction failed: {str(e)}")
        
        thread = threading.Thread(target=extract_in_background)
        thread.daemon = True
        thread.start()
        
        messages.success(request, 'Image extraction started! You will be redirected to the results page.')
        return redirect('results', extraction_id=extraction.id)


class ResultsView(View):
    def get(self, request, extraction_id):
        extraction = get_object_or_404(Extraction, id=extraction_id)
        
        # Check if user owns this extraction (if they're logged in)
        if request.user.is_authenticated and extraction.user and extraction.user != request.user:
            messages.error(request, 'You do not have permission to view this extraction.')
            return redirect('home')
        
        images = extraction.images.all().order_by('name')
        
        context = {
            'extraction': extraction,
            'images': images,
        }
        
        return render(request, 'extractor/results.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = AuthenticationForm()
        return render(request, 'extractor/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next page if specified
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        
        return render(request, 'extractor/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = UserCreationForm()
        return render(request, 'extractor/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            # Set email if provided
            email = request.POST.get('email')
            if email:
                user.email = email
                user.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('dashboard')
        
        return render(request, 'extractor/register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        # Get user's extractions
        extractions = Extraction.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
        
        # Calculate stats
        total_extractions = Extraction.objects.filter(user=request.user).count()
        completed_extractions = Extraction.objects.filter(
            user=request.user, 
            status='completed'
        ).count()
        total_images = Image.objects.filter(
            extraction__user=request.user
        ).count()
        
        stats = {
            'total_extractions': total_extractions,
            'completed_extractions': completed_extractions,
            'total_images': total_images,
        }
        
        context = {
            'extractions': extractions,
            'stats': stats,
        }
        
        return render(request, 'extractor/dashboard.html', context)




class APIDocsView(TemplateView):
    template_name = 'extractor/api_docs.html'




class SubscriptionView(TemplateView):
    template_name = 'extractor/subscription.html'

