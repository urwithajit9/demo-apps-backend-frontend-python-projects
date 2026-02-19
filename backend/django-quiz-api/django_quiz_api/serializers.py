from rest_framework import serializers
from django.utils import timezone
from .models import Question, Choice, Quiz, QuizQuestion, QuizResponse, QuestionResponse


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for the Choice model."""
    
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {
            'is_correct': {'write_only': True}  # Hide correct answer in list views
        }


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for the Question model with nested choices."""
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
    
    def validate_choices(self, choices):
        """Validate that at least 2 choices are provided and exactly one is correct."""
        if len(choices) < 2:
            raise serializers.ValidationError("At least 2 choices are required.")
        
        correct_choices = sum(1 for choice in choices if choice.get('is_correct', False))
        if correct_choices != 1:
            raise serializers.ValidationError("Exactly one choice must be marked as correct.")
        
        return choices
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        
        return question
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update choices if provided
        if choices_data is not None:
            # Delete existing choices
            instance.choices.all().delete()
            
            # Create new choices
            for choice_data in choices_data:
                Choice.objects.create(question=instance, **choice_data)
        
        return instance


class QuestionDetailSerializer(QuestionSerializer):
    """Detailed serializer for Question model, including approval information."""
    approved_by = serializers.ReadOnlyField(source='approved_by.username')
    
    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ['approved_by', 'approved_at']


class QuestionApprovalSerializer(serializers.ModelSerializer):
    """Serializer for approving or rejecting questions."""
    
    class Meta:
        model = Question
        fields = ['approval_status']
        
    def validate_approval_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("Status must be 'approved' or 'rejected'.")
        return value
    
    def update(self, instance, validated_data):
        instance.approval_status = validated_data.get('approval_status')
        instance.approved_by = self.context['request'].user
        instance.approved_at = timezone.now()
        instance.save()
        return instance


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Serializer for the QuizQuestion model."""
    question_text = serializers.ReadOnlyField(source='question.text')
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'question_text', 'order']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for the Quiz model."""
    created_by = serializers.ReadOnlyField(source='created_by.username')
    question_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'time_limit', 
            'created_by', 'is_active', 'pass_percentage',
            'question_count', 'created_at', 'updated_at'
        ]


class QuizDetailSerializer(QuizSerializer):
    """Detailed serializer for Quiz model, including questions."""
    questions = serializers.SerializerMethodField()
    
    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ['questions']
    
    def get_questions(self, obj):
        quiz_questions = obj.quiz_questions.all().order_by('order')
        return QuizQuestionSerializer(quiz_questions, many=True).data


class QuizQuestionAddSerializer(serializers.Serializer):
    """Serializer for adding questions to a quiz."""
    questions = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.filter(approval_status='approved'),
        many=True
    )
    
    def validate_questions(self, questions):
        if not questions:
            raise serializers.ValidationError("At least one question must be provided.")
        return questions


class QuizResponseSerializer(serializers.ModelSerializer):
    """Serializer for the QuizResponse model."""
    user = serializers.ReadOnlyField(source='user.username')
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    time_taken = serializers.ReadOnlyField()
    answered_questions_count = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizResponse
        fields = [
            'id', 'quiz', 'quiz_title', 'user', 'start_time', 'end_time',
            'score', 'status', 'time_taken', 'answered_questions_count',
            'is_passed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['start_time', 'end_time', 'score', 'status']


class QuestionResponseSerializer(serializers.ModelSerializer):
    """Serializer for the QuestionResponse model."""
    question_text = serializers.ReadOnlyField(source='question.text')
    
    class Meta:
        model = QuestionResponse
        fields = [
            'id', 'question', 'question_text', 'selected_choice',
            'is_correct', 'response_time'
        ]
        read_only_fields = ['is_correct']


class QuizQuestionResponseSerializer(serializers.Serializer):
    """Serializer for submitting an answer to a quiz question."""
    question_id = serializers.IntegerField()
    selected_choice_id = serializers.IntegerField()
    response_time = serializers.IntegerField(required=False)
    
    def validate(self, data):
        question_id = data.get('question_id')
        selected_choice_id = data.get('selected_choice_id')
        
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError({"question_id": "Question does not exist."})
        
        try:
            choice = Choice.objects.get(id=selected_choice_id, question=question)
        except Choice.DoesNotExist:
            raise serializers.ValidationError({"selected_choice_id": "Choice does not exist or does not belong to the specified question."})
        
        # Add validated objects to the data
        data['question'] = question
        data['selected_choice'] = choice
        
        return data


class QuizResultSerializer(serializers.ModelSerializer):
    """Serializer for quiz results."""
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    user = serializers.ReadOnlyField(source='user.username')
    question_responses = QuestionResponseSerializer(many=True, source='question_responses.all')
    pass_percentage = serializers.ReadOnlyField(source='quiz.pass_percentage')
    is_passed = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizResponse
        fields = [
            'id', 'quiz', 'quiz_title', 'user', 'start_time', 'end_time',
            'score', 'status', 'time_taken', 'pass_percentage', 'is_passed',
            'question_responses'
        ]
