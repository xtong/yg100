from django.test import TestCase

# Create your tests here.
from .models import StudyClass

class StudyClassModelTests(TestCase):

    def test_create_class(self):

        study_class = StudyClass()