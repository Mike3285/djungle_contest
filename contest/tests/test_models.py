from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from contest.models import Contest, Prize


class PrizeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        # Setup run before every test method.
        Prize.objects.create(name="sconto del 5%",
                             code="codice-sconto",
                             perday=24,
                             won_today=0,
                             contest_field= Contest.objects.create(start_date="2020-02-01",
                                                                   stop_date="2020-02-29",
                                                                   code="C0001")
                             )


