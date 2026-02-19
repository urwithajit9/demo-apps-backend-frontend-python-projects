# Django Quiz API Package Structure

This document outlines the structure of the Django Quiz API package, a reusable Django app that provides REST API endpoints for creating and managing quizzes.

## Package Structure

```
django_quiz_api/
├── django_quiz_api/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── validators.py
│   ├── signals.py
│   ├── admin.py
│   ├── migrations/
│   │   └── __init__.py
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── README.md
├── LICENSE
└── requirements.txt
```

## Core Components

### Models

1. **Question**
   - Text field for the question
   - Difficulty level (Easy, Medium, Hard)
   - Category/Tag for organization
   - Created by (User reference)
   - Approval status (Pending, Approved, Rejected)
   - Created/Updated timestamps

2. **Choice**
   - Text field for the choice
   - Reference to Question
   - Boolean field indicating if it's the correct answer

3. **Quiz**
   - Title
   - Description
   - Number of questions
   - Time limit (optional)
   - Created by (User reference)
   - Active status
   - Created/Updated timestamps

4. **QuizQuestion**
   - Reference to Quiz
   - Reference to Question
   - Order/Position in the quiz

5. **QuizResponse**
   - Reference to Quiz
   - Reference to User
   - Start time
   - End time
   - Score
   - Completion status

6. **QuestionResponse**
   - Reference to QuizResponse
   - Reference to Question
   - Reference to selected Choice
   - Correct/Incorrect status
   - Response time

### API Endpoints

1. **Question Management**
   - `POST /api/questions/` - Create a new question with choices
   - `GET /api/questions/` - List all questions (with filtering)
   - `GET /api/questions/{id}/` - Retrieve a specific question
   - `PUT /api/questions/{id}/` - Update a question
   - `DELETE /api/questions/{id}/` - Delete a question

2. **Question Approval**
   - `POST /api/questions/{id}/approve/` - Approve a question
   - `POST /api/questions/{id}/reject/` - Reject a question
   - `GET /api/questions/pending/` - List pending questions

3. **Quiz Management**
   - `POST /api/quizzes/` - Create a new quiz
   - `GET /api/quizzes/` - List all quizzes
   - `GET /api/quizzes/{id}/` - Retrieve a specific quiz
   - `PUT /api/quizzes/{id}/` - Update a quiz
   - `DELETE /api/quizzes/{id}/` - Delete a quiz
   - `POST /api/quizzes/{id}/add-questions/` - Add questions to a quiz

4. **Quiz Taking**
   - `POST /api/quizzes/{id}/start/` - Start a quiz (creates a QuizResponse)
   - `GET /api/quiz-responses/{id}/next-question/` - Get the next question
   - `POST /api/quiz-responses/{id}/answer/` - Submit an answer
   - `GET /api/quiz-responses/{id}/result/` - Get quiz results

### Permissions

1. **QuestionPermission**
   - Anyone can create questions
   - Only staff/admins can approve/reject questions
   - Question creators can edit their own questions

2. **QuizPermission**
   - Anyone can view active quizzes
   - Only authenticated users can create quizzes
   - Quiz creators can edit their own quizzes

3. **ResponsePermission**
   - Users can only view their own responses
   - Users can only submit answers to their own quiz attempts

## Integration Points

The package will be designed to be easily integrated into existing Django projects:

1. **App Configuration**
   - Simple installation via pip
   - Add to INSTALLED_APPS
   - Include URLs in project's urls.py

2. **Customization**
   - Settings for controlling behavior
   - Extension points for custom logic
   - Template overrides

3. **Authentication**
   - Compatible with Django's authentication system
   - Support for token authentication
   - Support for JWT authentication

## Dependencies

- Django (>=3.2)
- Django REST Framework (>=3.12)
- djangorestframework-simplejwt (optional, for JWT authentication)
