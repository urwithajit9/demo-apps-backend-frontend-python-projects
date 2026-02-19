from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Question, QuizResponse, QuestionResponse

@receiver(post_save, sender=Question)
def handle_question_approval(sender, instance, created, **kwargs):
    """
    Signal handler for when a question is saved.
    Updates the approved_at timestamp when a question is approved.
    """
    if not created and instance.approval_status == 'approved' and not instance.approved_at:
        # If the question was just approved, set the approved_at timestamp
        instance.approved_at = timezone.now()
        # Use update to avoid triggering this signal again
        Question.objects.filter(pk=instance.pk).update(approved_at=timezone.now())

@receiver(post_save, sender=QuestionResponse)
def update_quiz_response_on_completion(sender, instance, created, **kwargs):
    """
    Signal handler for when a question response is saved.
    Updates the quiz response status and score when all questions are answered.
    """
    if created:
        quiz_response = instance.quiz_response
        quiz = quiz_response.quiz
        
        # Count total questions in the quiz
        total_questions = quiz.quiz_questions.count()
        
        # Count answered questions
        answered_questions = QuestionResponse.objects.filter(quiz_response=quiz_response).count()
        
        # If all questions are answered, complete the quiz
        if answered_questions >= total_questions and quiz_response.status == 'in_progress':
            # Calculate score
            correct_answers = QuestionResponse.objects.filter(
                quiz_response=quiz_response,
                is_correct=True
            ).count()
            
            score = (correct_answers / total_questions) * 100
            
            # Update quiz response
            quiz_response.status = 'completed'
            quiz_response.end_time = timezone.now()
            quiz_response.score = score
            quiz_response.save()
