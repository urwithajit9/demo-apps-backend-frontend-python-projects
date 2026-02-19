from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Question, Choice, Quiz, QuizQuestion, QuizResponse, QuestionResponse
from .serializers import (
    QuestionSerializer, QuestionDetailSerializer, QuestionApprovalSerializer,
    QuizSerializer, QuizDetailSerializer, QuizQuestionAddSerializer,
    QuizResponseSerializer, QuestionResponseSerializer, QuizQuestionResponseSerializer,
    QuizResultSerializer
)
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly, IsQuizOwnerOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing quiz questions.
    
    list:
    Return a list of all questions (filtered by approval status).
    
    create:
    Create a new question with choices.
    
    retrieve:
    Return the given question.
    
    update:
    Update the given question.
    
    partial_update:
    Partially update the given question.
    
    destroy:
    Delete the given question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'category']
    ordering_fields = ['created_at', 'difficulty', 'category']
    
    def get_queryset(self):
        """
        Filter questions based on user role and query parameters.
        """
        queryset = Question.objects.all()
        
        # Staff can see all questions
        if not self.request.user.is_staff:
            # Regular users can see approved questions and their own pending/rejected questions
            queryset = queryset.filter(
                Q(approval_status='approved') | 
                Q(created_by=self.request.user)
            )
        
        # Filter by approval status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(approval_status=status_param)
            
        # Filter by difficulty if provided
        difficulty_param = self.request.query_params.get('difficulty')
        if difficulty_param:
            queryset = queryset.filter(difficulty=difficulty_param)
            
        # Filter by category if provided
        category_param = self.request.query_params.get('category')
        if category_param:
            queryset = queryset.filter(category=category_param)
            
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        elif self.action in ['approve', 'reject']:
            return QuestionApprovalSerializer
        return QuestionSerializer
    
    def perform_create(self, serializer):
        """
        Set the creator when creating a question.
        """
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Approve a question.
        """
        question = self.get_object()
        serializer = self.get_serializer(question, data={'approval_status': 'approved'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'question approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Reject a question.
        """
        question = self.get_object()
        serializer = self.get_serializer(question, data={'approval_status': 'rejected'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'question rejected'})
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def pending(self, request):
        """
        List all pending questions.
        """
        pending_questions = Question.objects.filter(approval_status='pending')
        page = self.paginate_queryset(pending_questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(pending_questions, many=True)
        return Response(serializer.data)


class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing quizzes.
    
    list:
    Return a list of all quizzes.
    
    create:
    Create a new quiz.
    
    retrieve:
    Return the given quiz.
    
    update:
    Update the given quiz.
    
    partial_update:
    Partially update the given quiz.
    
    destroy:
    Delete the given quiz.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    
    def get_queryset(self):
        """
        Filter quizzes based on user role and query parameters.
        """
        queryset = Quiz.objects.all()
        
        # Regular users can see active quizzes and their own inactive quizzes
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(is_active=True) | 
                Q(created_by=self.request.user)
            )
            
        # Filter by active status if provided
        active_param = self.request.query_params.get('active')
        if active_param is not None:
            is_active = active_param.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'retrieve':
            return QuizDetailSerializer
        elif self.action == 'add_questions':
            return QuizQuestionAddSerializer
        return QuizSerializer
    
    def perform_create(self, serializer):
        """
        Set the creator when creating a quiz.
        """
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_questions(self, request, pk=None):
        """
        Add questions to a quiz.
        """
        quiz = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        questions = serializer.validated_data['questions']
        
        # Get the highest current order
        last_order = QuizQuestion.objects.filter(quiz=quiz).order_by('-order').first()
        next_order = 1 if last_order is None else last_order.order + 1
        
        # Add questions to the quiz
        for question in questions:
            # Skip if question already exists in this quiz
            if not QuizQuestion.objects.filter(quiz=quiz, question=question).exists():
                QuizQuestion.objects.create(
                    quiz=quiz,
                    question=question,
                    order=next_order
                )
                next_order += 1
        
        return Response({'status': 'questions added to quiz'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        Start a quiz and create a quiz response.
        """
        quiz = self.get_object()
        
        # Check if quiz is active
        if not quiz.is_active:
            return Response(
                {'error': 'This quiz is not active.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if quiz has questions
        if quiz.question_count == 0:
            return Response(
                {'error': 'This quiz has no questions.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new quiz response
        quiz_response = QuizResponse.objects.create(
            quiz=quiz,
            user=request.user,
            status='in_progress'
        )
        
        serializer = QuizResponseSerializer(quiz_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizResponseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing quiz responses.
    
    list:
    Return a list of all quiz responses for the current user.
    
    retrieve:
    Return the given quiz response.
    """
    serializer_class = QuizResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter quiz responses to only show the current user's responses.
        """
        return QuizResponse.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def next_question(self, request, pk=None):
        """
        Get the next unanswered question for this quiz response.
        """
        quiz_response = self.get_object()
        
        # Check if quiz is still in progress
        if quiz_response.status != 'in_progress':
            return Response(
                {'error': 'This quiz has already been completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all questions for this quiz
        quiz_questions = QuizQuestion.objects.filter(quiz=quiz_response.quiz).order_by('order')
        
        # Get IDs of already answered questions
        answered_question_ids = QuestionResponse.objects.filter(
            quiz_response=quiz_response
        ).values_list('question_id', flat=True)
        
        # Find the first unanswered question
        for quiz_question in quiz_questions:
            if quiz_question.question_id not in answered_question_ids:
                # Return the question with its choices
                question = quiz_question.question
                serializer = QuestionSerializer(question)
                return Response(serializer.data)
        
        # If all questions have been answered
        return Response(
            {'status': 'completed', 'message': 'All questions have been answered.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def answer(self, request, pk=None):
        """
        Submit an answer for a question in this quiz response.
        """
        quiz_response = self.get_object()
        
        # Check if quiz is still in progress
        if quiz_response.status != 'in_progress':
            return Response(
                {'error': 'This quiz has already been completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate the answer
        serializer = QuizQuestionResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = serializer.validated_data['question']
        selected_choice = serializer.validated_data['selected_choice']
        response_time = serializer.validated_data.get('response_time')
        
        # Check if question belongs to this quiz
        if not QuizQuestion.objects.filter(quiz=quiz_response.quiz, question=question).exists():
            return Response(
                {'error': 'This question does not belong to the current quiz.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if question has already been answered
        if QuestionResponse.objects.filter(quiz_response=quiz_response, question=question).exists():
            return Response(
                {'error': 'This question has already been answered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the question response
        question_response = QuestionResponse.objects.create(
            quiz_response=quiz_response,
            question=question,
            selected_choice=selected_choice,
            is_correct=selected_choice.is_correct,
            response_time=response_time
        )
        
        # Check if all questions have been answered
        quiz_question_count = QuizQuestion.objects.filter(quiz=quiz_response.quiz).count()
        answered_question_count = QuestionResponse.objects.filter(quiz_response=quiz_response).count()
        
        if answered_question_count >= quiz_question_count:
            # Calculate score
            correct_count = QuestionResponse.objects.filter(
                quiz_response=quiz_response, 
                is_correct=True
            ).count()
            
            score = (correct_count / quiz_question_count) * 100
            
            # Update quiz response
            quiz_response.status = 'completed'
            quiz_response.end_time = timezone.now()
            quiz_response.score = score
            quiz_response.save()
            
            return Response({
                'status': 'completed',
                'message': 'All questions have been answered.',
                'is_correct': question_response.is_correct,
                'score': score
            })
        
        return Response({
            'status': 'in_progress',
            'is_correct': question_response.is_correct,
            'questions_answered': answered_question_count,
            'total_questions': quiz_question_count
        })
    
    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        """
        Get the results of a completed quiz response.
        """
        quiz_response = self.get_object()
        
        # Check if quiz is completed
        if quiz_response.status != 'completed':
            return Response(
                {'error': 'This quiz has not been completed yet.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = QuizResultSerializer(quiz_response)
        return Response(serializer.data)
