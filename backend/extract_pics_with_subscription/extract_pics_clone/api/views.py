from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from rest_framework_simplejwt.tokens import RefreshToken
from extractor.models import Extraction, Image
from extractor.utils import extract_images_from_url
from .serializers import (
    UserRegistrationSerializer, 
    ExtractionSerializer, 
    ExtractionCreateSerializer,
    ImageSerializer
)
import threading
import zipfile
import io
import requests


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class ExtractImagesView(generics.CreateAPIView):
    serializer_class = ExtractionCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create extraction object
        extraction = Extraction.objects.create(
            user=request.user,
            url=serializer.validated_data['url'],
            status='pending'
        )
        
        # Start image extraction in background thread
        def extract_in_background():
            try:
                extract_images_from_url(extraction.url, extraction)
            except Exception as e:
                print(f"Background extraction failed: {str(e)}")
        
        thread = threading.Thread(target=extract_in_background)
        thread.daemon = True
        thread.start()
        
        return Response({
            'extraction_id': extraction.id,
            'status': extraction.status,
            'message': 'Image extraction started'
        }, status=status.HTTP_201_CREATED)


class ExtractionsListView(generics.ListAPIView):
    serializer_class = ExtractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Extraction.objects.filter(user=self.request.user)


class ExtractionImagesView(generics.RetrieveAPIView):
    serializer_class = ExtractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Extraction.objects.filter(user=self.request.user)


class ImageDownloadView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, *args, **kwargs):
        try:
            image = Image.objects.get(
                pk=pk, 
                extraction__user=request.user
            )
            
            # Redirect to the actual image URL
            return HttpResponse(
                status=302,
                headers={'Location': image.url}
            )
            
        except Image.DoesNotExist:
            raise Http404("Image not found")


class BulkDownloadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        image_ids = request.data.get('image_ids', [])
        
        if not image_ids:
            return Response(
                {'error': 'No image IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get images belonging to the user
        images = Image.objects.filter(
            id__in=image_ids,
            extraction__user=request.user
        )
        
        if not images.exists():
            return Response(
                {'error': 'No valid images found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, image in enumerate(images):
                try:
                    # Download image content
                    response = requests.get(image.url, timeout=30)
                    if response.status_code == 200:
                        # Generate filename
                        filename = image.name or f'image_{i+1}'
                        if image.file_type:
                            filename = f"{filename}.{image.file_type}"
                        
                        # Add to ZIP
                        zip_file.writestr(filename, response.content)
                        
                except Exception as e:
                    print(f"Error downloading image {image.url}: {str(e)}")
                    continue
        
        zip_buffer.seek(0)
        
        # Return ZIP file
        response = HttpResponse(
            zip_buffer.getvalue(),
            content_type='application/zip'
        )
        response['Content-Disposition'] = 'attachment; filename="images.zip"'
        
        return response



# API Key Management Views
from rest_framework.views import APIView
from users.models import APIKey
from .serializers import (
    APIKeySerializer,
    APIKeyCreateSerializer,
    APIKeyResponseSerializer
)
from .authentication import APIKeyAuthentication


class APIKeyListView(generics.ListAPIView):
    """List all API keys for the authenticated user"""
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)


class APIKeyCreateView(APIView):
    """Generate a new API key for the authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = APIKeyCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            name = serializer.validated_data['name']
            
            # Generate the API key
            api_key, raw_key = APIKey.generate_key(request.user, name)
            
            # Return the response with the raw key (only shown once)
            response_data = {
                'id': api_key.id,
                'name': api_key.name,
                'key': raw_key,
                'prefix': api_key.prefix,
                'created_at': api_key.created_at
            }
            
            response_serializer = APIKeyResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIKeyRevokeView(APIView):
    """Revoke (deactivate) an API key"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            api_key = APIKey.objects.get(pk=pk, user=request.user)
            api_key.revoke()
            return Response({'message': 'API key revoked successfully'}, status=status.HTTP_200_OK)
        except APIKey.DoesNotExist:
            return Response({'error': 'API key not found'}, status=status.HTTP_404_NOT_FOUND)


# Update existing views to support API key authentication
# We need to modify the authentication_classes for existing views
ExtractImagesView.authentication_classes = [APIKeyAuthentication]
ExtractionsListView.authentication_classes = [APIKeyAuthentication]
ExtractionImagesView.authentication_classes = [APIKeyAuthentication]
ImageDownloadView.authentication_classes = [APIKeyAuthentication]
BulkDownloadView.authentication_classes = [APIKeyAuthentication]




class APIRootView(APIView):
    """
    API Root endpoint that provides documentation and overview of available endpoints.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Return API documentation and available endpoints.
        """
        return Response({
            'message': 'Welcome to Extract.pics API',
            'version': '1.0',
            'documentation': request.build_absolute_uri('/api/docs/'),
            'endpoints': {
                'authentication': {
                    'register': request.build_absolute_uri('/api/register/'),
                    'token': request.build_absolute_uri('/api/token/'),
                    'token_refresh': request.build_absolute_uri('/api/token/refresh/'),
                },
                'image_extraction': {
                    'extract': request.build_absolute_uri('/api/extract/'),
                    'extractions': request.build_absolute_uri('/api/extractions/'),
                    'extraction_images': request.build_absolute_uri('/api/extractions/{id}/images/'),
                    'image_download': request.build_absolute_uri('/api/images/{id}/download/'),
                    'bulk_download': request.build_absolute_uri('/api/images/bulk_download/'),
                },
                'api_keys': {
                    'list': request.build_absolute_uri('/api/keys/'),
                    'generate': request.build_absolute_uri('/api/keys/generate/'),
                    'revoke': request.build_absolute_uri('/api/keys/{id}/revoke/'),
                }
            },
            'usage': {
                'authentication': 'Use JWT tokens or API keys for authentication',
                'rate_limits': 'Standard rate limits apply',
                'support': 'Contact support for assistance'
            }
        })

