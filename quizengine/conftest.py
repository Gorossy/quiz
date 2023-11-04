import pytest
from quizengine.models import Exam, Question, Choice

@pytest.fixture
def exam_fixture(db):
    exam = Exam.objects.create(title="Lorem Ipsum Exam", description="Sample description")
    question1 = Question.objects.create(exam=exam, text="Lorem ipsum dolor sit amet?", multiple_answers=False)
    Choice.objects.create(question=question1, text="Consectetur", is_correct=True)
    question2 = Question.objects.create(exam=exam, text="Sed do eiusmod tempor incididunt ut labore?", multiple_answers=True)
    Choice.objects.create(question=question2, text="Et dolore", is_correct=True)
    Choice.objects.create(question=question2, text="Et dolore magna", is_correct=False)
    return exam