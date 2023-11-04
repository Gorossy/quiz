from rest_framework import serializers
from .models import Exam, Question, Choice, UserAnswer, UserExam, UserStatistics
from django.contrib.auth.models import User

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'multiple_answers', 'choices')

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ('id', 'title', 'description', 'questions')

class ExamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'title', 'description')

class UserAnswerSerializer(serializers.ModelSerializer):
    selected_choices = serializers.PrimaryKeyRelatedField(many=True, queryset=Choice.objects.all())

    class Meta:
        model = UserAnswer
        fields = ('question', 'selected_choices')

class UserExamSerializer(serializers.ModelSerializer):
    user_answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserExam
        fields = ('exam', 'user_answers')
    
    def validate(self, attrs):
        questions = Question.objects.filter(exam=attrs['exam'])
        question_ids = [q.id for q in questions]
        for user_answer in attrs['user_answers']:
            if user_answer['question'].id not in question_ids:
                raise serializers.ValidationError("One or more questions do not belong to the provided exam.")
        return attrs
    def validate_user_answers(self, value):
        if not value:
            raise serializers.ValidationError("At least one answer must be provided.")
        return value
    def create(self, validated_data):
        user_answers_data = validated_data.pop('user_answers')
        user = self.context['user']
        exam = validated_data['exam']

        user_exam = UserExam.objects.create(user=user, exam=exam)

        total_score = 0
        for user_answer_data in user_answers_data:
            question = user_answer_data['question']
            selected_choices_instances = user_answer_data['selected_choices'] 
            user_answer = UserAnswer.objects.create(user_exam=user_exam, question=question)
            user_answer.selected_choices.set(selected_choices_instances)
            
            correct_choices = question.choices.filter(is_correct=True)
            if question.multiple_answers:
                
                if set(user_answer.selected_choices.all()) == set(correct_choices) and user_answer.selected_choices.count() == correct_choices.count():
                    total_score += 1
            else:
                if user_answer.selected_choices.count() == 1 and user_answer.selected_choices.first().is_correct:
                    total_score += 1

            user_answer.save()

        user_exam.score = total_score / question.exam.questions.count() * 100 
        user_exam.save()

        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_statistics.update_statistics()

        return user_exam
class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user