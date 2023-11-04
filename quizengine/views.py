from rest_framework.response import Response
from rest_framework import status, generics
from .models import Exam, UserStatistics
from .serializers import ExamSerializer, ExamListSerializer, UserExamSerializer,UserRegistrationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer
    permission_classes = [IsAuthenticated]

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

class SubmitExamView(generics.CreateAPIView):
    serializer_class = UserExamSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            user_exam = serializer.save()
            return Response({
                "exam_id": user_exam.exam.id,
                "score": user_exam.score,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_statistics = UserStatistics.objects.get(user=request.user)
            return Response({
                "average_score": user_statistics.average_score,
                "quizzes_completed": user_statistics.quizzes_completed,
            })
        except UserStatistics.DoesNotExist:
            return Response({"error": "Statistics do not exist for this user."}, status=404)