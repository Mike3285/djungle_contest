from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from contest.models import Contest

class  ContestTestCase(TestCase):
    def setUp(self):
        Contest.objects.create(name="lion")
        Contest.objects.create(name="cat")

    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')