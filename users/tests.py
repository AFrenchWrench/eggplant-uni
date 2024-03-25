from django.test import TestCase
from django.utils import timezone

from student_dash.models import StudentCourse
from university.models import Faculty, Major, ApprovedCourse
from users.models import User, Student, Professor


class UserTests(TestCase):
    def test_create_user(self):
        self.user1 = User.objects.create(username='user1', email='soads@asdas.ads', phone_number='sds',
                                         national_id='asdasda', gender='M', birth_date=timezone.now())
        self.assertEqual(User.objects.get(username='user1'), self.user1)


class StudentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='student', user_code='asdasdasd', password='<PASSWORD>',
                                        email='email@email.email',
                                        phone_number='1234', national_id='31321658',
                                        first_name='first', last_name='last', gender='male')
        self.user1 = User.objects.create(username='professor', user_code='asdasdasdss', password='<PASSWORD>',
                                         email='email1@email.email',
                                         phone_number='15234', national_id='3132221658',
                                         first_name='first', last_name='last', gender='male')
        self.faculty = Faculty.objects.create(faculty_name='Faculty', faculty_code='12345')
        self.major = Major.objects.create(major_code='12345', major_name='Major', department='Department',
                                          faculty=self.faculty, number_of_credits=4, degree_level='asasda')
        self.professor = Professor.objects.create(user=self.user1, major=self.major, rank='I')
        self.student = Student.objects.create(user=self.user,
                                              admission_year=1403,
                                              admission_semester='spring 403', major=self.major,
                                              advisor=self.professor, military_status=True)
        self.course = ApprovedCourse.objects.create(course_code='adsdasd', course_name='sadad',
                                                    offering_faculty=self.faculty,
                                                    number_of_credits=4, course_type='General')
        self.course1 = ApprovedCourse.objects.create(course_code='adsdaasdassd', course_name='sadsdadasdad',
                                                     offering_faculty=self.faculty,
                                                     number_of_credits=4, course_type='General')
        self.stucourse1 = StudentCourse.objects.create(student=self.student, course=self.course, course_status='sdasd',
                                                       grade=16, semester='spring 403')
        self.stucourse2 = StudentCourse.objects.create(student=self.student, course=self.course1, course_status='sdasd',
                                                       grade=12, semester='spring 403')

    def test_get_gpa_method(self):
        self.assertEqual(self.student.get_gpa(), 14.0)
