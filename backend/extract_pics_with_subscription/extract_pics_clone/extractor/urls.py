from django.urls import path
from . import views

urlpatterns = [
    # Web Interface Views
    path('', views.HomeView.as_view(), name='home'),
    path('extract/', views.ExtractView.as_view(), name='extract'),
    path('results/<int:extraction_id>/', views.ResultsView.as_view(), name='results'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]



    path("api/docs/", views.APIDocsView.as_view(), name="api_docs"),


    path("subscription/", views.SubscriptionView.as_view(), name="subscription"),

