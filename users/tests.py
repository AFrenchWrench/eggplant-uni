from django.test import TestCase
from django.utils import timezone

from student_dash.models import StudentCourse
from university.models import Faculty, Major, Course, Semester
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
        self.faculty = Faculty.objects.create(name='Faculty')
        self.major = Major.objects.create(name='Major', department='Department',
                                          faculty=self.faculty, units=4, degree_level='AD')
        self.professor = Professor.objects.create(user=self.user1, major=self.major, rank='I')
        self.semester = Semester.objects.create(name='Spring 1403', course_selection_start_time=timezone.now(),
                                                course_selection_end_time=timezone.now(),
                                                class_start_time=timezone.now(),
                                                class_end_time=timezone.now(),
                                                course_addition_drop_start=timezone.now(),
                                                course_addition_drop_end=timezone.now(),
                                                last_day_for_emergency_withdrawal=timezone.now(),
                                                exam_start_time=timezone.now(),
                                                semester_end_date=timezone.now())
        self.student = Student.objects.create(user=self.user,
                                              admission_year=1403,
                                              admission_semester=self.semester, major=self.major,
                                              advisor=self.professor, military_status=True)
        self.course = Course.objects.create(name='sadad',
                                            faculty=self.faculty,
                                            units=4, type='G')
        self.course1 = Course.objects.create(name='sadsdadasdad',
                                             faculty=self.faculty,
                                             units=4, type='G')
        self.stu_course1 = StudentCourse.objects.create(student=self.student, course=self.course,
                                                        grade=16, semester=self.semester)
        self.stu_course2 = StudentCourse.objects.create(student=self.student, course=self.course1,
                                                        grade=12, semester=self.semester)

    def test_get_gpa_method(self):
        self.assertEqual(self.student.get_gpa(), 14.0)
