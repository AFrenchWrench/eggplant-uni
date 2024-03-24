from django.test import TestCase

from university.models import Faculty


class FacultyTests(TestCase):
    pass
    # def test_create_faculty(self):
    #     self.faculty = list()
    #     for num in range(10000):
    #         self.faculty.append(Faculty.objects.create(faculty_name=f'fuc-k{num}'))
    #     self.assertEqual(len(self.faculty), 10000)
