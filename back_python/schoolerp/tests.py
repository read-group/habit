from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from .models import School


class QuestionMethodTests(TestCase):

    def test_q(self):
        """
        query count test
        """
        for item in School.objects.all():
            print(item)
        #self.assertIs(School.objects.count()==1, True)
