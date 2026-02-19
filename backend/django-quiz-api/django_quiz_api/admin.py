from django.contrib import admin
from .models import Question, Choice, Quiz, QuizQuestion, QuizResponse, QuestionResponse

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    min_num = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'category', 'created_by', 'approval_status', 'created_at')
    list_filter = ('difficulty', 'approval_status', 'category', 'created_at')
    search_fields = ('text', 'category')
    readonly_fields = ('created_by', 'approved_by', 'approved_at', 'created_at', 'updated_at')
    inlines = [ChoiceInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_active', 'question_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    inlines = [QuizQuestionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'is_correct', 'response_time')
    can_delete = False

@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'status', 'score', 'start_time', 'end_time')
    list_filter = ('status', 'start_time')
    search_fields = ('quiz__title', 'user__username')
    readonly_fields = ('quiz', 'user', 'start_time', 'end_time', 'score', 'status', 'created_at', 'updated_at')
    inlines = [QuestionResponseInline]
    
    def has_add_permission(self, request):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
