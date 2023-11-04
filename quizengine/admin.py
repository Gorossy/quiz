from django.contrib import admin
from .models import Exam, Question, Choice

class AnswerInline(admin.TabularInline):
    model = Choice
    extra = 3  

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text', 'exam', 'multiple_answers']}),
    ]
    inlines = [AnswerInline]
    list_display = ('text', 'exam', 'multiple_answers')
    list_filter = ['exam']
    search_fields = ['text']

class ExamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'description']}),
    ]
    list_display = ('title', 'description')
    search_fields = ['title', 'description']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam, ExamAdmin)
