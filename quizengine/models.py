from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    multiple_answers = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'exam', 'completed_at'] 

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - Score: {self.score}"

class UserAnswer(models.Model):
    user_exam = models.ForeignKey(UserExam, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"{self.user_exam.user.username} - {self.question.text} - {self.selected_choices.all()}"
    
class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    average_score = models.FloatField(default=0.0)
    quizzes_completed = models.IntegerField(default=0)

    def update_statistics(self):
        exams = UserExam.objects.filter(user=self.user)
        self.average_score = exams.aggregate(Avg('score'))['score__avg'] or 0.0
        self.quizzes_completed = exams.count()
        self.save()

    def __str__(self):
        return f"{self.user.username} - Avg Score: {self.average_score}, Quizzes Completed: {self.quizzes_completed}"