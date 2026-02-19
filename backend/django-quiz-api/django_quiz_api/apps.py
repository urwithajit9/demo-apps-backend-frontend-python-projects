from django.apps import AppConfig


class DjangoQuizApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_quiz_api'
    verbose_name = 'Django Quiz API'
    
    def ready(self):
        # Import signals
        import django_quiz_api.signals
