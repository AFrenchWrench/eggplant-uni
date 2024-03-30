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


class CreateCourseInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    faculty = graphene.ID(required=True)
    prerequisites = graphene.List(graphene.ID, required=False)
    corequisites = graphene.List(graphene.ID, required=False)
    units = graphene.Int(required=True)
    type = graphene.String(required=True)


class CreateSemesterCourseInput(graphene.InputObjectType):
    course = graphene.ID(required=True)
    semester = graphene.ID(required=True)
    day_and_time = graphene.String(required=True)
    exam_datetime = graphene.DateTime(required=True)
    exam_location = graphene.String(required=True)
    professor = graphene.ID(required=True)
    capacity = graphene.Int(required=True)


class CreateStudentCourseInput(graphene.InputObjectType):
    student = graphene.ID(required=True)
    course = graphene.ID(required=True)
    grade = graphene.Float(required=True)


class CreateSemesterInput(graphene.InputObjectType):
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


class CreateSemesterStudentInput(graphene.InputObjectType):
    student = graphene.ID(required=True)
    semester = graphene.ID(required=True)
    is_active = graphene.Boolean(required=True)


class CreateFacultyInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateMajorInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    department = graphene.String(required=True)
    faculty = graphene.ID(required=True)
    units = graphene.Int(required=True)
    degree_level = graphene.String(required=True)


class CreateCourse(graphene.Mutation):
    class Arguments:
        input = CreateCourseInput(required=True)

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
        return CreateCourse(course=course)


class CreateSemesterCourse(graphene.Mutation):
    class Arguments:
        input = CreateSemesterCourseInput(required=True)

    semester_course = graphene.Field(SemesterCourseType)

    @staticmethod
    def mutate(self, info, input):
        semester_course = input
        semester_course['course'] = get_object_or_404(Course, id=semester_course['course'])
        semester_course['semester'] = get_object_or_404(Semester, id=semester_course['semester'])
        semester_course['professor'] = get_object_or_404(Professor, id=semester_course['professor'])
        semester_course = SemesterCourse.objects.create(**semester_course)
        return CreateSemesterCourse(semester_course=semester_course)


class CreateStudentCourse(graphene.Mutation):
    class Arguments:
        input = CreateStudentCourseInput(required=True)

    student_course = graphene.Field(StudentCourseType)

    @staticmethod
    def mutate(self, info, input):
        student_course = input
        student_course['student'] = get_object_or_404(Student, id=student_course['student'])
        student_course['course'] = get_object_or_404(SemesterCourse, id=student_course['course'])
        student_course = StudentCourse.objects.create(**student_course)
        return CreateStudentCourse(student_course=student_course)


class CreateSemester(graphene.Mutation):
    class Arguments:
        input = CreateSemesterInput(required=True)

    semester = graphene.Field(SemesterType)

    @staticmethod
    def mutate(self, info, input):
        semester = input
        semester = Semester.objects.create(**semester)
        return CreateSemester(semester=semester)


class CreateSemesterStudent(graphene.Mutation):
    class Arguments:
        input = CreateSemesterStudentInput(required=True)

    semester_student = graphene.Field(SemesterStudentType)

    @staticmethod
    def mutate(self, info, input):
        semester_student = input
        semester_student['student'] = get_object_or_404(Student, id=semester_student['student'])
        semester_student['semester'] = get_object_or_404(Semester, id=semester_student['semester'])
        semester_student = SemesterStudent.objects.create(**semester_student)
        return CreateSemesterStudent(semester_student=semester_student)


class CreateFaculty(graphene.Mutation):
    class Arguments:
        input = CreateFacultyInput(required=True)

    faculty = graphene.Field(FacultyType)

    @staticmethod
    def mutate(self, info, input):
        faculty = input
        faculty = Faculty.objects.create(**faculty)
        return CreateFaculty(faculty=faculty)


class CreateMajor(graphene.Mutation):
    class Arguments:
        input = CreateMajorInput(required=True)

    major = graphene.Field(MajorType)

    @staticmethod
    def mutate(self, info, input):
        major = input
        major['faculty'] = get_object_or_404(FacultyType, id=major['faculty'])
        major = Major.objects.create(**major)
        return CreateMajor(major=major)


class UpdateCourseInput(graphene.InputObjectType):
    name = graphene.String()
    faculty = graphene.ID()
    prerequisites = graphene.List(graphene.ID)
    corequisites = graphene.List(graphene.ID)
    units = graphene.Int()
    type = graphene.String()


class UpdateSemesterCourseInput(graphene.InputObjectType):
    course = graphene.ID()
    semester = graphene.ID()
    day_and_time = graphene.String()
    exam_datetime = graphene.DateTime()
    exam_location = graphene.String()
    professor = graphene.ID()
    capacity = graphene.Int()


class UpdateStudentCourseInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    grade = graphene.Float()


class UpdateSemesterInput(graphene.InputObjectType):
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


class UpdateSemesterStudentInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    is_active = graphene.Boolean()


class UpdateFacultyInput(graphene.InputObjectType):
    name = graphene.String()


class UpdateMajorInput(graphene.InputObjectType):
    name = graphene.String()
    department = graphene.String()
    faculty = graphene.ID()
    units = graphene.Int()
    degree_level = graphene.String()


class UpdateCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateCourseInput(required=True)

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
        return UpdateCourse(course=course)


class UpdateSemesterCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateSemesterCourseInput(required=True)

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
        return UpdateSemesterCourse(semester_course=semester_course)


class UpdateStudentCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateStudentCourseInput(required=True)

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
        return UpdateStudentCourse(student_course=student_course)


class UpdateSemester(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateSemesterInput(required=True)

    semester = graphene.Field(SemesterType)

    @staticmethod
    def mutate(self, info, pk, input):
        semester = get_object_or_404(Semester, pk=pk)
        for field, value in input.items():
            setattr(semester, field, value)
        semester.save()
        return UpdateSemester(semester=semester)


class UpdateSemesterStudent(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateSemesterStudentInput(required=True)

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
        return UpdateSemesterStudent(semester_student=semester_student)


class UpdateFaculty(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateFacultyInput(required=True)

    faculty = graphene.Field(FacultyType)

    @staticmethod
    def mutate(self, info, pk, input):
        faculty = get_object_or_404(Faculty, pk=pk)
        for field, value in input.items():
            setattr(faculty, field, value)
        faculty.save()
        return UpdateFaculty(faculty=faculty)


class UpdateMajor(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateMajorInput(required=True)

    major = graphene.Field(MajorType)

    @staticmethod
    def mutate(self, info, pk, input):
        major = get_object_or_404(Major, pk=pk)
        for field, value in input.items():
            if field == 'faculty':
                value = get_object_or_404(Faculty, pk=value)
            setattr(major, field, value)
        major.save()
        return UpdateMajor(major=major)


class DeleteCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return DeleteCourse(success=True)


class DeleteSemesterCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        semester_course = get_object_or_404(SemesterCourse, pk=pk)
        semester_course.delete()
        return DeleteSemesterCourse(success=True)


class DeleteStudentCourse(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        student_course = get_object_or_404(StudentCourse, pk=pk)
        student_course.delete()
        return DeleteStudentCourse(success=True)


class DeleteSemester(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        semester = get_object_or_404(Semester, pk=pk)
        semester.delete()
        return DeleteSemester(success=True)


class DeleteSemesterStudent(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        semester_student = get_object_or_404(SemesterStudent, pk=pk)
        semester_student.delete()
        return DeleteSemesterStudent(success=True)


class DeleteFaculty(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        faculty = get_object_or_404(Faculty, pk=pk)
        faculty.delete()
        return DeleteFaculty(success=True)


class DeleteMajor(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, pk):
        major = get_object_or_404(Major, pk=pk)
        major.delete()
        return DeleteMajor(success=True)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_semester_course = CreateSemesterCourse.Field()
    create_student_course = CreateStudentCourse.Field()
    create_semester = CreateSemester.Field()
    create_semester_student = CreateSemesterStudent.Field()
    create_faculty = CreateFaculty.Field()
    create_major = CreateMajor.Field()
    update_course = UpdateCourse.Field()
    update_semester_course = UpdateSemesterCourse.Field()
    update_student_course = UpdateStudentCourse.Field()
    update_semester = UpdateSemester.Field()
    update_semester_student = UpdateSemesterStudent.Field()
    update_faculty = UpdateFaculty.Field()
    update_major = UpdateMajor.Field()
    delete_course = DeleteCourse.Field()
    delete_semester_course = DeleteSemesterCourse.Field()
    delete_student_course = DeleteStudentCourse.Field()
    delete_semester = DeleteSemester.Field()
    delete_semester_student = DeleteSemesterStudent.Field()
    delete_faculty = DeleteFaculty.Field()
    delete_major = DeleteMajor.Field()


class CourseFilterInput(graphene.InputObjectType):
    name = graphene.String()
    faculty = graphene.ID()
    type = graphene.String()


class SemesterCourseFilterInput(graphene.InputObjectType):
    course = graphene.ID()
    semester = graphene.ID()


class StudentCourseFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()


class SemesterFilterInput(graphene.InputObjectType):
    name = graphene.String()


class SemesterStudentFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    is_active = graphene.Boolean()


class FacultyFilterInput(graphene.InputObjectType):
    name = graphene.String()


class MajorFilterInput(graphene.InputObjectType):
    name = graphene.String()
    department = graphene.String()
    faculty = graphene.ID()


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, filters=CourseFilterInput())
    semester_courses = graphene.List(SemesterCourseType, filters=SemesterCourseFilterInput())
    student_courses = graphene.List(StudentCourseType, filters=StudentCourseFilterInput())
    semesters = graphene.List(SemesterType, filters=SemesterFilterInput())
    semester_students = graphene.List(SemesterStudentType, filters=SemesterStudentFilterInput())
    faculties = graphene.List(FacultyType, filters=FacultyFilterInput())
    majors = graphene.List(MajorType, filters=MajorFilterInput())

    # Generic resolver to get all instances of a model with filters
    def resolve_model_with_filters(self, info, model_class, filter_input=None):
        queryset = model_class.objects.all()
        if filter_input:
            queryset = queryset.filter(**filter_input)
        return queryset

    # Resolver for retrieving a single instance of a model by its ID
    def resolve_model_by_id(self, info, model_class, id):
        return get_object_or_404(model_class, id=id)

    # Resolver for courses
    def resolve_courses(self, info, filters=None):
        return self.resolve_model_with_filters(info, Course, filters)

    # Resolver for semester courses
    def resolve_semester_courses(self, info, filters=None):
        return self.resolve_model_with_filters(info, SemesterCourse, filters)

    # Resolver for student courses
    def resolve_student_courses(self, info, filters=None):
        return self.resolve_model_with_filters(info, StudentCourse, filters)

    # Resolver for semesters
    def resolve_semesters(self, info, filters=None):
        return self.resolve_model_with_filters(info, Semester, filters)

    # Resolver for semester students
    def resolve_semester_students(self, info, filters=None):
        return self.resolve_model_with_filters(info, SemesterStudent, filters)

    # Resolver for faculties
    def resolve_faculties(self, info, filters=None):
        return self.resolve_model_with_filters(info, Faculty, filters)

    # Resolver for majors
    def resolve_majors(self, info, filters=None):
        return self.resolve_model_with_filters(info, Major, filters)


schema = graphene.Schema(query=Query, mutation=Mutation)
