from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    created and modified fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    """
    Model representing a quiz question.
    """
    DIFFICULTY_CHOICES = (
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    )
    
    APPROVAL_STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )
    
    text = models.TextField(_('Question Text'))
    difficulty = models.CharField(
        _('Difficulty Level'), 
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium'
    )
    category = models.CharField(_('Category'), max_length=100, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_questions',
        verbose_name=_('Created By')
    )
    approval_status = models.CharField(
        _('Approval Status'),
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='approved_questions',
        verbose_name=_('Approved By'),
        null=True,
        blank=True
    )
    approved_at = models.DateTimeField(_('Approved At'), null=True, blank=True)
    explanation = models.TextField(_('Explanation'), blank=True)
    
    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.text[:50]
    
    @property
    def is_approved(self):
        return self.approval_status == 'approved'
    
    @property
    def correct_choice(self):
        try:
            return self.choices.get(is_correct=True)
        except Choice.DoesNotExist:
            return None


class Choice(models.Model):
    """
    Model representing a choice for a question.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name=_('Question')
    )
    text = models.CharField(_('Choice Text'), max_length=255)
    is_correct = models.BooleanField(_('Is Correct Answer'), default=False)
    
    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')
        ordering = ['id']
        
    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        # If this choice is marked as correct, ensure no other choice for this question is correct
        if self.is_correct:
            Choice.objects.filter(question=self.question).exclude(pk=self.pk).update(is_correct=False)
        super().save(*args, **kwargs)


class Quiz(TimeStampedModel):
    """
    Model representing a quiz.
    """
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    time_limit = models.PositiveIntegerField(
        _('Time Limit (minutes)'), 
        null=True, 
        blank=True,
        help_text=_('Time limit for the quiz in minutes. Leave blank for no time limit.')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_quizzes',
        verbose_name=_('Created By')
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    pass_percentage = models.PositiveSmallIntegerField(
        _('Pass Percentage'),
        default=70,
        help_text=_('Percentage required to pass the quiz')
    )
    
    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def question_count(self):
        return self.quiz_questions.count()


class QuizQuestion(models.Model):
    """
    Model representing a question in a quiz.
    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='quiz_questions',
        verbose_name=_('Quiz')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='quiz_questions',
        verbose_name=_('Question')
    )
    order = models.PositiveIntegerField(_('Order'), default=0)
    
    class Meta:
        verbose_name = _('Quiz Question')
        verbose_name_plural = _('Quiz Questions')
        ordering = ['order']
        unique_together = ['quiz', 'question']
        
    def __str__(self):
        return f"{self.quiz.title} - {self.question.text[:30]}"


class QuizResponse(TimeStampedModel):
    """
    Model representing a user's response to a quiz.
    """
    STATUS_CHOICES = (
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('timed_out', _('Timed Out')),
    )
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Quiz')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_responses',
        verbose_name=_('User')
    )
    start_time = models.DateTimeField(_('Start Time'), auto_now_add=True)
    end_time = models.DateTimeField(_('End Time'), null=True, blank=True)
    score = models.DecimalField(
        _('Score'), 
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    
    class Meta:
        verbose_name = _('Quiz Response')
        verbose_name_plural = _('Quiz Responses')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def is_passed(self):
        if self.score is None:
            return False
        return self.score >= self.quiz.pass_percentage
    
    @property
    def time_taken(self):
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds() // 60
    
    @property
    def answered_questions_count(self):
        return self.question_responses.count()


class QuestionResponse(models.Model):
    """
    Model representing a user's response to a question in a quiz.
    """
    quiz_response = models.ForeignKey(
        QuizResponse,
        on_delete=models.CASCADE,
        related_name='question_responses',
        verbose_name=_('Quiz Response')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Question')
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('Selected Choice'),
        null=True,
        blank=True
    )
    is_correct = models.BooleanField(_('Is Correct'), default=False)
    response_time = models.PositiveIntegerField(
        _('Response Time (seconds)'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('Question Response')
        verbose_name_plural = _('Question Responses')
        unique_together = ['quiz_response', 'question']
        
    def __str__(self):
        return f"{self.quiz_response.user.username} - {self.question.text[:30]}"
    
    def save(self, *args, **kwargs):
        # Automatically determine if the response is correct
        if self.selected_choice:
            self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)
