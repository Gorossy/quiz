import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def user_and_token(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    refresh = RefreshToken.for_user(user)
    # Devolvemos directamente el token de acceso como un string
    return user, str(refresh.access_token)

@pytest.mark.django_db
def test_submit_exam_success(exam_fixture, user_and_token):
    user, token = user_and_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # Obtén las preguntas y respuestas correctas de la fixture de examen
    question1 = exam_fixture.questions.get(text="Lorem ipsum dolor sit amet?")
    choice1 = question1.choices.get(text="Consectetur")
    question2 = exam_fixture.questions.get(text="Sed do eiusmod tempor incididunt ut labore?")
    choice2_1, _ = question2.choices.all()

    # Asegúrate de que el payload incluye respuestas para todas las preguntas
    data = {
        "exam": exam_fixture.id,
        "user_answers": [
            {
                "question": question1.id,
                "selected_choices": [choice1.id]
            },
            {
                "question": question2.id,
                "selected_choices": [choice2_1.id]  # Asume que solo esta es correcta y es una respuesta múltiple
            }
        ]
    }

    url = reverse('submit-exam')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    # Asegúrate de que la puntuación esperada aquí sea la correcta según tu lógica de puntuación
    assert response.data['score'] == 100  # Reemplaza 'tu_puntuación_esperada' con la puntuación correcta según tu lógica de puntuación

@pytest.mark.django_db
def test_submit_exam_failure(exam_fixture, user_and_token):
    user, token = user_and_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    question2 = exam_fixture.questions.get(text="Sed do eiusmod tempor incididunt ut labore?")
    choice2_1, choice2_2 = question2.choices.all()

    data = {
        "exam": exam_fixture.id,
        "user_answers": [
        ]
    }

    url = reverse('submit-exam')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
