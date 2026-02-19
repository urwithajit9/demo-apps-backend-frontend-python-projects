# Django Quiz API

A reusable Django app that provides REST API endpoints for creating and managing quizzes with multiple-choice questions.

## Features

- Create and manage multiple-choice questions
- Question approval workflow
- Create quizzes from approved questions
- Take quizzes and track responses
- Automatic scoring and result calculation
- Comprehensive REST API with Django REST Framework

## Installation

```bash
pip install django-quiz-api
```

## Quick Start

1. Add "django_quiz_api" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_quiz_api',
]
```

2. Include the django_quiz_api URLconf in your project urls.py:

```python
urlpatterns = [
    ...
    path('api/quiz/', include('django_quiz_api.urls')),
]
```

3. Run migrations to create the models:

```bash
python manage.py migrate
```

4. Start using the API endpoints!

## API Endpoints

### Question Management

- `GET /api/quiz/questions/` - List all questions
- `POST /api/quiz/questions/` - Create a new question with choices
- `GET /api/quiz/questions/{id}/` - Retrieve a specific question
- `PUT /api/quiz/questions/{id}/` - Update a question
- `DELETE /api/quiz/questions/{id}/` - Delete a question
- `POST /api/quiz/questions/{id}/approve/` - Approve a question (staff only)
- `POST /api/quiz/questions/{id}/reject/` - Reject a question (staff only)
- `GET /api/quiz/questions/pending/` - List pending questions (staff only)

### Quiz Management

- `GET /api/quiz/quizzes/` - List all quizzes
- `POST /api/quiz/quizzes/` - Create a new quiz
- `GET /api/quiz/quizzes/{id}/` - Retrieve a specific quiz
- `PUT /api/quiz/quizzes/{id}/` - Update a quiz
- `DELETE /api/quiz/quizzes/{id}/` - Delete a quiz
- `POST /api/quiz/quizzes/{id}/add-questions/` - Add questions to a quiz
- `POST /api/quiz/quizzes/{id}/start/` - Start a quiz (creates a QuizResponse)

### Quiz Taking

- `GET /api/quiz/quiz-responses/` - List all quiz responses for the current user
- `GET /api/quiz/quiz-responses/{id}/` - Retrieve a specific quiz response
- `GET /api/quiz/quiz-responses/{id}/next-question/` - Get the next question
- `POST /api/quiz/quiz-responses/{id}/answer/` - Submit an answer
- `GET /api/quiz/quiz-responses/{id}/result/` - Get quiz results

## Django REST Framework Refresher

If you're new to Django REST Framework or need a refresher, here are some key concepts used in this package:

### Serializers

Serializers convert complex data types (like Django models) to Python primitives that can be rendered into JSON. They also handle deserialization, validating incoming data.

```python
# Example serializer from django_quiz_api
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'difficulty', 'category', 'created_by',
            'approval_status', 'explanation', 'choices',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['approval_status', 'approved_by', 'approved_at']
```

### ViewSets

ViewSets combine the logic for multiple related views into a single class. They provide actions like `list`, `create`, `retrieve`, `update`, and `destroy`.

```python
# Example viewset from django_quiz_api
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    # Custom action example
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        question = self.get_object()
        serializer = self.get_serializer(question, data={'approval_status': 'approved'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'question approved'})
```

### Routers

Routers automatically generate URL patterns for ViewSets, making it easy to set up API endpoints.

```python
# Example router from django_quiz_api
router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
```

### Permissions

Permissions determine whether a request should be granted or denied access. DRF provides several built-in permissions, and you can create custom ones.

```python
# Example custom permission from django_quiz_api
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
```

## Example Usage

### Creating a Question with Choices

```python
# POST to /api/quiz/questions/
{
    "text": "What is the capital of France?",
    "difficulty": "easy",
    "category": "Geography",
    "explanation": "Paris is the capital and most populous city of France.",
    "choices": [
        {
            "text": "Paris",
            "is_correct": true
        },
        {
            "text": "London",
            "is_correct": false
        },
        {
            "text": "Berlin",
            "is_correct": false
        },
        {
            "text": "Madrid",
            "is_correct": false
        }
    ]
}
```

### Creating a Quiz

```python
# POST to /api/quiz/quizzes/
{
    "title": "Geography Quiz",
    "description": "Test your knowledge of world capitals",
    "time_limit": 10,
    "pass_percentage": 70
}
```

### Adding Questions to a Quiz

```python
# POST to /api/quiz/quizzes/{quiz_id}/add-questions/
{
    "questions": [1, 2, 3, 4, 5]  # Question IDs
}
```

### Starting a Quiz

```python
# POST to /api/quiz/quizzes/{quiz_id}/start/
# No request body needed
```

### Answering a Question

```python
# POST to /api/quiz/quiz-responses/{response_id}/answer/
{
    "question_id": 1,
    "selected_choice_id": 3,
    "response_time": 15  # seconds (optional)
}
```

## Customization

### Settings

You can customize the behavior of django-quiz-api by adding these settings to your project's settings.py:

```python
# Default settings (you can override these)
QUIZ_API_SETTINGS = {
    'DEFAULT_PASS_PERCENTAGE': 70,  # Default passing score percentage
    'ALLOW_ANONYMOUS_QUIZ_CREATION': False,  # Whether anonymous users can create quizzes
    'REQUIRE_QUESTION_APPROVAL': True,  # Whether questions require approval before use
    'MAX_CHOICES_PER_QUESTION': 6,  # Maximum number of choices per question
}
```

### Extending Models

You can extend the models by subclassing them in your own app:

```python
from django_quiz_api.models import Question, Quiz

class CustomQuestion(Question):
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    
class CustomQuiz(Quiz):
    background_color = models.CharField(max_length=7, default='#FFFFFF')
```

## License

MIT License
