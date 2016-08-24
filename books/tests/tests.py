from django.test import TestCase

# Create your tests here.
class DemoTest(TestCase):
    def test_addition(self):
        self.assertEquals(1+1,2)

    def test_addition2(self):
        self.assertEquals(2+2,4)
