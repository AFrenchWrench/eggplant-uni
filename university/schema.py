import graphene
from graphene_django import DjangoObjectType
from django.shortcuts import get_object_or_404
from .models import (
    Course,
    SemesterCourse,
    StudentCourse,
    Semester,
    SemesterStudent,
    Faculty,
    Major,
)
from users.models import (
    Professor,
    Student,
)


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class SemesterCourseType(DjangoObjectType):
    class Meta:
        model = SemesterCourse


class StudentCourseType(DjangoObjectType):
    class Meta:
        model = StudentCourse


class SemesterType(DjangoObjectType):
    class Meta:
        model = Semester


class SemesterStudentType(DjangoObjectType):
    class Meta:
        model = SemesterStudent


class FacultyType(DjangoObjectType):
    class Meta:
        model = Faculty


class MajorType(DjangoObjectType):
    class Meta:
        model = Major


class CourseCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    faculty = graphene.ID(required=True)
    prerequisites = graphene.List(graphene.ID, required=False)
    corequisites = graphene.List(graphene.ID, required=False)
    units = graphene.Int(required=True)
    type = graphene.String(required=True)


class SemesterCourseCreateInput(graphene.InputObjectType):
    course = graphene.ID(required=True)
    semester = graphene.ID(required=True)
    day_and_time = graphene.String(required=True)
    exam_datetime = graphene.DateTime(required=True)
    exam_location = graphene.String(required=True)
    professor = graphene.ID(required=True)
    capacity = graphene.Int(required=True)


class StudentCourseCreateInput(graphene.InputObjectType):
    student = graphene.ID(required=True)
    course = graphene.ID(required=True)
    grade = graphene.Float(required=True)


class SemesterCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    course_selection_start_time = graphene.DateTime(required=True)
    course_selection_end_time = graphene.DateTime(required=True)
    class_start_time = graphene.DateTime(required=True)
    class_end_time = graphene.DateTime(required=True)
    course_addition_drop_start = graphene.DateTime(required=True)
    course_addition_drop_end = graphene.DateTime(required=True)
    last_day_for_emergency_withdrawal = graphene.DateTime(required=True)
    exam_start_time = graphene.DateTime(required=True)
    semester_end_date = graphene.Date(required=True)


class SemesterStudentCreateInput(graphene.InputObjectType):
    student = graphene.ID(required=True)
    semester = graphene.ID(required=True)
    is_active = graphene.Boolean(required=True)


class FacultyCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class MajorCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    department = graphene.String(required=True)
    faculty = graphene.ID(required=True)
    units = graphene.Int(required=True)
    degree_level = graphene.String(required=True)


class CourseCreate(graphene.Mutation):
    class Arguments:
        input = CourseCreateInput(required=True)

    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(self, info, input):
        course = input
        course['faculty'] = get_object_or_404(Faculty, id=course['faculty'])

        try:
            i = 0
            for prerequisite in course['prerequisites']:
                course['prerequisites'][i] = get_object_or_404(Course, id=prerequisite)
                i += 1
        except KeyError:
            course['prerequisites'] = None
        try:
            i = 0
            for corequisite in course['corequisites']:
                course['corequisites'][i] = get_object_or_404(Course, id=corequisite)
                i += 1
        except KeyError:
            course['corequisites'] = None

        course = Course.objects.create(**course)
        return CourseCreate(course=course)


class SemesterCourseCreate(graphene.Mutation):
    class Arguments:
        input = SemesterCourseCreateInput(required=True)

    semester_course = graphene.Field(SemesterCourseType)

    @staticmethod
    def mutate(self, info, input):
        semester_course = input
        semester_course['course'] = get_object_or_404(Course, id=semester_course['course'])
        semester_course['semester'] = get_object_or_404(Semester, id=semester_course['semester'])
        semester_course['professor'] = get_object_or_404(Professor, id=semester_course['professor'])
        semester_course = SemesterCourse.objects.create(**semester_course)
        return SemesterCourseCreate(semester_course=semester_course)


class StudentCourseCreate(graphene.Mutation):
    class Arguments:
        input = StudentCourseCreateInput(required=True)

    student_course = graphene.Field(StudentCourseType)

    @staticmethod
    def mutate(self, info, input):
        student_course = input
        student_course['student'] = get_object_or_404(Student, id=student_course['student'])
        student_course['course'] = get_object_or_404(SemesterCourse, id=student_course['course'])
        student_course = StudentCourse.objects.create(**student_course)
        return StudentCourseCreate(student_course=student_course)


class SemesterCreate(graphene.Mutation):
    class Arguments:
        input = SemesterCreateInput(required=True)

    semester = graphene.Field(SemesterType)

    @staticmethod
    def mutate(self, info, input):
        semester = input
        semester = Semester.objects.create(**semester)
        return SemesterCreate(semester=semester)


class SemesterStudentCreate(graphene.Mutation):
    class Arguments:
        input = SemesterStudentCreateInput(required=True)

    semester_student = graphene.Field(SemesterStudentType)

    @staticmethod
    def mutate(self, info, input):
        semester_student = input
        semester_student['student'] = get_object_or_404(Student, id=semester_student['student'])
        semester_student['semester'] = get_object_or_404(Semester, id=semester_student['semester'])
        semester_student = SemesterStudent.objects.create(**semester_student)
        return SemesterStudentCreate(semester_student=semester_student)


class FacultyCreate(graphene.Mutation):
    class Arguments:
        input = FacultyCreateInput(required=True)

    faculty = graphene.Field(FacultyType)

    @staticmethod
    def mutate(self, info, input):
        faculty = input
        faculty = Faculty.objects.create(**faculty)
        return FacultyCreate(faculty=faculty)


class MajorCreate(graphene.Mutation):
    class Arguments:
        input = MajorCreateInput(required=True)

    major = graphene.Field(MajorType)

    @staticmethod
    def mutate(self, info, input):
        major = input
        major['faculty'] = get_object_or_404(FacultyType, id=major['faculty'])
        major = Major.objects.create(**major)
        return MajorCreate(major=major)


class CourseUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    faculty = graphene.ID()
    prerequisites = graphene.List(graphene.ID)
    corequisites = graphene.List(graphene.ID)
    units = graphene.Int()
    type = graphene.String()


class SemesterCourseUpdateInput(graphene.InputObjectType):
    course = graphene.ID()
    semester = graphene.ID()
    day_and_time = graphene.String()
    exam_datetime = graphene.DateTime()
    exam_location = graphene.String()
    professor = graphene.ID()
    capacity = graphene.Int()


class StudentCourseUpdateInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    grade = graphene.Float()


class SemesterUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    course_selection_start_time = graphene.DateTime()
    course_selection_end_time = graphene.DateTime()
    class_start_time = graphene.DateTime()
    class_end_time = graphene.DateTime()
    course_addition_drop_start = graphene.DateTime()
    course_addition_drop_end = graphene.DateTime()
    last_day_for_emergency_withdrawal = graphene.DateTime()
    exam_start_time = graphene.DateTime()
    semester_end_date = graphene.Date()


class SemesterStudentUpdateInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    is_active = graphene.Boolean()


class FacultyUpdateInput(graphene.InputObjectType):
    name = graphene.String()


class MajorUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    department = graphene.String()
    faculty = graphene.ID()
    units = graphene.Int()
    degree_level = graphene.String()


class CourseUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = CourseUpdateInput(required=True)

    course = graphene.Field(CourseType)

    @staticmethod
    def mutate(self, info, pk, input):
        course = get_object_or_404(Course, pk=pk)
        for field, value in input.items():
            if field == 'faculty':
                value = get_object_or_404(Faculty, id=value)
            elif field == 'prerequisites' and value is not None:
                i = 0
                for prerequisite in value:
                    value[i] = get_object_or_404(Course, id=prerequisite)
                    i += 1
            elif field == 'corequisites' and value is not None:
                i = 0
                for corequisite in value:
                    value[i] = get_object_or_404(Course, id=corequisite)
                    i += 1
            setattr(course, field, value)
        course.save()
        return CourseUpdate(course=course)


class SemesterCourseUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = SemesterCourseUpdateInput(required=True)

    semester_course = graphene.Field(SemesterCourseType)

    @staticmethod
    def mutate(self, info, pk, input):
        semester_course = get_object_or_404(SemesterCourse, pk=pk)
        for field, value in input.items():
            if field == 'course':
                value = get_object_or_404(Course, pk=value)
            elif field == 'semester':
                value = get_object_or_404(Semester, pk=value)
            elif field == 'professor':
                value = get_object_or_404(Professor, pk=value)
            setattr(semester_course, field, value)
        semester_course.save()
        return SemesterCourseUpdate(semester_course=semester_course)


class StudentCourseUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = StudentCourseUpdateInput(required=True)

    student_course = graphene.Field(StudentCourseType)

    @staticmethod
    def mutate(self, info, pk, input):
        student_course = get_object_or_404(StudentCourse, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'course':
                value = get_object_or_404(SemesterCourse, pk=value)
            setattr(student_course, field, value)
        student_course.save()
        return StudentCourseUpdate(student_course=student_course)


class SemesterUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = SemesterUpdateInput(required=True)

    semester = graphene.Field(SemesterType)

    @staticmethod
    def mutate(self, info, pk, input):
        semester = get_object_or_404(Semester, pk=pk)
        for field, value in input.items():
            setattr(semester, field, value)
        semester.save()
        return SemesterUpdate(semester=semester)


class SemesterStudentUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = SemesterStudentUpdateInput(required=True)

    semester_student = graphene.Field(SemesterStudentType)

    @staticmethod
    def mutate(self, info, pk, input):
        semester_student = get_object_or_404(SemesterStudent, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'semester':
                value = get_object_or_404(Semester, pk=value)
            setattr(semester_student, field, value)
        semester_student.save()
        return SemesterStudentUpdate(semester_student=semester_student)


class FacultyUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = FacultyUpdateInput(required=True)

    faculty = graphene.Field(FacultyType)

    @staticmethod
    def mutate(self, info, pk, input):
        faculty = get_object_or_404(Faculty, pk=pk)
        for field, value in input.items():
            setattr(faculty, field, value)
        faculty.save()
        return FacultyUpdate(faculty=faculty)


class MajorUpdate(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = MajorUpdateInput(required=True)

    major = graphene.Field(MajorType)

    @staticmethod
    def mutate(self, info, pk, input):
        major = get_object_or_404(Major, pk=pk)
        for field, value in input.items():
            if field == 'faculty':
                value = get_object_or_404(Faculty, pk=value)
            setattr(major, field, value)
        major.save()
        return MajorUpdate(major=major)

