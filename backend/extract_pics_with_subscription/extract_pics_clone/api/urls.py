from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # API Documentation root endpoint
    path('', views.APIRootView.as_view(), name='api_root'),
    
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Image extraction endpoints
    path('extract/', views.ExtractImagesView.as_view(), name='extract_images'),
    path('extractions/', views.ExtractionsListView.as_view(), name='extractions_list'),
    path('extractions/<int:pk>/images/', views.ExtractionImagesView.as_view(), name='extraction_images'),
    path('images/<int:pk>/download/', views.ImageDownloadView.as_view(), name='image_download'),
    path('images/bulk_download/', views.BulkDownloadView.as_view(), name='bulk_download'),
    
    # API Key management endpoints
    path('keys/', views.APIKeyListView.as_view(), name='api_keys_list'),
    path('keys/generate/', views.APIKeyCreateView.as_view(), name='api_key_create'),
    path('keys/<int:pk>/revoke/', views.APIKeyRevokeView.as_view(), name='api_key_revoke'),
]

