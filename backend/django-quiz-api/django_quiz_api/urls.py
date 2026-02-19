from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'django_quiz_api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'quiz-responses', views.QuizResponseViewSet, basename='quiz-response')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
