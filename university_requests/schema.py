import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from university.models import (
    SemesterCourse,
    Semester,
    Faculty,
)
from users.models import Student, Professor
from utils.schema_utils import (
    resolve_model_with_filters,
    login_required, staff_or_assistant,
)
from .models import (
    CourseRegistrationRequest,
    StudentCourseParticipant,
    CourseCorrectionRequest,
    ReconsiderationRequest,
    EmergencyWithdrawalRequest,
    SemesterWithdrawalRequest,
    DefermentRequest,
)


class CourseRegistrationRequestType(DjangoObjectType):
    class Meta:
        model = CourseRegistrationRequest


class StudentCourseParticipantType(DjangoObjectType):
    class Meta:
        model = StudentCourseParticipant


class CourseCorrectionRequestType(DjangoObjectType):
    class Meta:
        model = CourseCorrectionRequest


class ReconsiderationRequestType(DjangoObjectType):
    class Meta:
        model = ReconsiderationRequest


class EmergencyWithdrawalRequestType(DjangoObjectType):
    class Meta:
        model = EmergencyWithdrawalRequest


class SemesterWithdrawalRequestType(DjangoObjectType):
    class Meta:
        model = SemesterWithdrawalRequest


class DefermentRequestType(DjangoObjectType):
    class Meta:
        model = DefermentRequest


class CreateCourseRegistrationRequestInput(graphene.InputObjectType):
    courses = graphene.List(graphene.ID, required=True)


class CreateStudentCourseParticipantInput(graphene.InputObjectType):
    course = graphene.ID(required=True)


class CreateCourseCorrectionRequestInput(graphene.InputObjectType):
    dropped_courses = graphene.List(graphene.ID, required=True)
    added_courses = graphene.List(graphene.ID, required=True)


class CreateReconsiderationRequestInput(graphene.InputObjectType):
    course = graphene.ID(required=True)
    text = graphene.String(required=True)


class CreateEmergencyWithdrawalRequestInput(graphene.InputObjectType):
    course = graphene.ID(required=True)
    text = graphene.String(required=True)


class CreateSemesterWithdrawalRequestInput(graphene.InputObjectType):
    semester = graphene.ID(required=True)
    text = graphene.String(required=True)


class CreateDefermentRequestInput(graphene.InputObjectType):
    file = Upload(required=True)
    semester = graphene.ID(required=True)
    faculty = graphene.ID(required=True)


class CreateCourseRegistrationRequest(graphene.Mutation):
    class Arguments:
        input = CreateCourseRegistrationRequestInput(required=True)

    course_registration_request = graphene.Field(CourseRegistrationRequestType)

    @staticmethod
    @login_required
    def mutate(self, info, input):
        semester = [semester for semester in Semester.objects.all() if semester.is_active()][0]
        if semester.course_selection_end_time < timezone.now():
            raise GraphQLError("The Course Selection Time is Over")
        elif semester.course_selection_start_time > timezone.now():
            raise GraphQLError("The Course Selection hasn't been Started")
        try:
            user = info.context.user
            student = user.student
            semester_courses = [get_object_or_404(SemesterCourse, pk=course_id) for course_id in input['courses']]
            # TODO : create a form to validate the selected courses based on document
            # درس ͖یشنیاز حتما باید در وضعیت قبول باشد -- Done
            # درس تکراری یا پاس شده نمیتوان برداشت -- Done
            # درس تکمیل را نمیتوان اخذ کرد -- Done
            # درس همنیاز را نمیتوان زودتر از درسی که همنیاز آن شده حذف کرد -- HELP!!
            # در صورت معدل ترم ͖یش بالای  ۱۷دانشجو حق دارد  ۲۴واحد اخذ کند و در غیر این صورت  ۲۰واحد در یک -- Done
            # انتخاب واحد می تواند اخذ کند -- Done
            # تداخل زمانی در امتحان و کلاس نباید وجود داشته باشد
            # دانشجو در صورت داشتن سنوات میتواند انتخاب واحد کند
            # تنها دروس مرتبط به رشته را میتوان برداشت
            # و هر خطایی که بنظر شما منطقی میباشد باید ͖یادهسازی شود

            # Prerequisites Check
            # if not all(map(student.check_course_passed_or_failed,
            #                [prerequisite for semester_course in
            #                 semester_courses for prerequisite in semester_course.course.get_all_prerequisites()])):
            #     raise GraphQLError("At Least One of the Prerequisites Not Passed")

            pp = [p.check_all_prerequisites() for p in semester_courses]

            # Duplicate Semester Course Check
            #     if len(semester_courses) != len(set(semester_courses)):
            #         raise GraphQLError("Duplicate Course Found!")
            #
            #     # Passed Course Check
            #     for semester_course in semester_courses:
            #         if semester_course in student.get_passed_courses:
            #             raise GraphQLError("You Passed At Least One of the Course")
            #
            #     # Semester Course Capacity Check (Without Redis)
            #     if not all([semester_course.get_capacity_count() for semester_course in semester_courses]):
            #         raise GraphQLError("At Least Capacity of One of the Courses is Zero ")
            #
            #     # Units Count Check
            #     if sum([semester_course.course_units() for semester_course in
            #             semester_courses]) >= student.get_max_courses_unit():
            #         raise GraphQLError("Courses Units Count is Bigger than Max Allowed Units")
            #
            #     #
            #     course_registration_request = CourseRegistrationRequest.objects.create(student=student,
            #                                                                            courses=semester_courses)
            #
            return CreateCourseRegistrationRequest(course_registration_request=course_registration_request)
        except Student.DoesNotExist:
            raise GraphQLError("You have to be a Student to create this request")


class CreateStudentCourseParticipant(graphene.Mutation):
    class Arguments:
        input = CreateStudentCourseParticipantInput(required=True)

    student_course_participant = graphene.Field(StudentCourseParticipantType)

    @staticmethod
    def mutate(self, info, input):
        student = get_object_or_404(Student, pk=input['student'])
        course = get_object_or_404(SemesterCourse, pk=input['course'])

        student_course_participant = StudentCourseParticipant.objects.create(student=student,
                                                                             course=course)

        return CreateStudentCourseParticipant(student_course_participant=student_course_participant)


class CreateCourseCorrectionRequest(graphene.Mutation):
    class Arguments:
        input = CreateCourseCorrectionRequestInput(required=True)

    course_correction_request = graphene.Field(CourseCorrectionRequestType)

    @staticmethod
    @login_required
    def mutate(self, info, input):
        semester = [semester for semester in Semester.objects.all() if semester.is_active()][0]
        if semester.course_addition_drop_end < timezone.now():
            raise GraphQLError("The Course addition/drop Time is Over")
        try:
            user = info.context.user
            student = user.student
            dropped_courses = [get_object_or_404(SemesterCourse, pk=course_id) for course_id in
                               input['dropped_courses']]
            added_courses = [get_object_or_404(SemesterCourse, pk=course_id) for course_id in input['added_courses']]

            # TODO: add same logic as course registration here

            course_correction_request = CourseCorrectionRequest.objects.create(student=student)
            course_correction_request.dropped_courses.set(dropped_courses)
            course_correction_request.added_courses.set(added_courses)

            return CreateCourseCorrectionRequest(course_correction_request=course_correction_request)
        except Student.DoesNotExist:
            raise GraphQLError("You have to be a Student to create this request")


class CreateReconsiderationRequest(graphene.Mutation):
    class Arguments:
        input = CreateReconsiderationRequestInput(required=True)

    reconsideration_request = graphene.Field(ReconsiderationRequestType)

    @staticmethod
    def mutate(self, info, input):
        student = get_object_or_404(Student, pk=input['student'])
        course = get_object_or_404(SemesterCourse, pk=input['course'])

        reconsideration_request = ReconsiderationRequest.objects.create(student=student, course=course,
                                                                        text=input['text'])

        return CreateReconsiderationRequest(reconsideration_request=reconsideration_request)


class CreateEmergencyWithdrawalRequest(graphene.Mutation):
    class Arguments:
        input = CreateEmergencyWithdrawalRequestInput(required=True)

    emergency_withdrawal_request = graphene.Field(EmergencyWithdrawalRequestType)

    @staticmethod
    def mutate(self, info, input):
        student = get_object_or_404(Student, pk=input['student'])
        course = get_object_or_404(SemesterCourse, pk=input['course'])

        emergency_withdrawal_request = EmergencyWithdrawalRequest.objects.create(student=student, course=course,
                                                                                 text=input['text'])

        return CreateEmergencyWithdrawalRequest(emergency_withdrawal_request=emergency_withdrawal_request)


class CreateSemesterWithdrawalRequest(graphene.Mutation):
    class Arguments:
        input = CreateSemesterWithdrawalRequestInput(required=True)

    semester_withdrawal_request = graphene.Field(SemesterWithdrawalRequestType)

    @staticmethod
    def mutate(self, info, input):
        student = get_object_or_404(Student, pk=input['student'])
        semester = get_object_or_404(Semester, pk=input['semester'])

        semester_withdrawal_request = SemesterWithdrawalRequest.objects.create(student=student, semester=semester,
                                                                               text=input['text'])

        return CreateSemesterWithdrawalRequest(semester_withdrawal_request=semester_withdrawal_request)


class CreateDefermentRequest(graphene.Mutation):
    class Arguments:
        input = CreateDefermentRequestInput(required=True)

    deferment_request = graphene.Field(DefermentRequestType)

    @staticmethod
    def mutate(self, info, input):
        student = get_object_or_404(Student, pk=input['student'])
        semester = get_object_or_404(Semester, pk=input['semester'])
        faculty = get_object_or_404(Faculty, pk=input['faculty'])

        deferment_request = DefermentRequest.objects.create(student=student, semester=semester, faculty=faculty,
                                                            file=input['file'])

        return CreateDefermentRequest(deferment_request=deferment_request)


class UpdateCourseRegistrationRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    courses = graphene.List(graphene.ID)
    status = graphene.String()


class UpdateStudentCourseParticipantInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    status = graphene.String()


class UpdateCourseCorrectionRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    dropped_courses = graphene.List(graphene.ID)
    added_courses = graphene.List(graphene.ID)
    status = graphene.String()


class UpdateReconsiderationRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    text = graphene.String()
    response = graphene.String()
    status = graphene.String()


class UpdateEmergencyWithdrawalRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    text = graphene.String()
    response = graphene.String()
    status = graphene.String()


class UpdateSemesterWithdrawalRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    text = graphene.String()
    response = graphene.String()
    status = graphene.String()


class UpdateDefermentRequestInput(graphene.InputObjectType):
    student = graphene.ID()
    file = Upload()
    semester = graphene.ID()
    faculty = graphene.ID()
    status = graphene.String()


class UpdateCourseRegistrationRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateCourseRegistrationRequestInput(required=True)

    course_registration_request = graphene.Field(CourseRegistrationRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        course_registration_request = get_object_or_404(CourseRegistrationRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'courses':
                value = [get_object_or_404(SemesterCourse, pk=pk) for pk in value]
            setattr(course_registration_request, field, value)
        course_registration_request.save()
        return UpdateCourseRegistrationRequest(course_registration_request=course_registration_request)


class UpdateStudentCourseParticipant(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateStudentCourseParticipantInput(required=True)

    student_course_participant = graphene.Field(StudentCourseParticipantType)

    @staticmethod
    def mutate(root, info, pk, input):
        student_course_participant = get_object_or_404(StudentCourseParticipant, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'course':
                value = get_object_or_404(SemesterCourse, pk=value)
            setattr(student_course_participant, field, value)
        student_course_participant.save()
        return UpdateStudentCourseParticipant(student_course_participant=student_course_participant)


class UpdateCourseCorrectionRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateCourseCorrectionRequestInput(required=True)

    course_correction_request = graphene.Field(CourseCorrectionRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        course_correction_request = get_object_or_404(CourseCorrectionRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field in ['dropped_courses', 'added_courses']:
                value = [get_object_or_404(SemesterCourse, pk=pk) for pk in value]
            setattr(course_correction_request, field, value)
        course_correction_request.save()
        return UpdateCourseCorrectionRequest(course_correction_request=course_correction_request)


class UpdateReconsiderationRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateReconsiderationRequestInput(required=True)

    reconsideration_request = graphene.Field(ReconsiderationRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        reconsideration_request = get_object_or_404(ReconsiderationRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'course':
                value = get_object_or_404(SemesterCourse, pk=value)
            setattr(reconsideration_request, field, value)
        reconsideration_request.save()
        return UpdateReconsiderationRequest(reconsideration_request=reconsideration_request)


class UpdateEmergencyWithdrawalRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateEmergencyWithdrawalRequestInput(required=True)

    emergency_withdrawal_request = graphene.Field(EmergencyWithdrawalRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        emergency_withdrawal_request = get_object_or_404(EmergencyWithdrawalRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'course':
                value = get_object_or_404(SemesterCourse, pk=value)
            setattr(emergency_withdrawal_request, field, value)
        emergency_withdrawal_request.save()
        return UpdateEmergencyWithdrawalRequest(emergency_withdrawal_request=emergency_withdrawal_request)


class UpdateSemesterWithdrawalRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateSemesterWithdrawalRequestInput(required=True)

    semester_withdrawal_request = graphene.Field(SemesterWithdrawalRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        semester_withdrawal_request = get_object_or_404(SemesterWithdrawalRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'semester':
                value = get_object_or_404(Semester, pk=value)
            setattr(semester_withdrawal_request, field, value)
        semester_withdrawal_request.save()
        return UpdateSemesterWithdrawalRequest(semester_withdrawal_request=semester_withdrawal_request)


class UpdateDefermentRequest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        input = UpdateDefermentRequestInput(required=True)

    deferment_request = graphene.Field(DefermentRequestType)

    @staticmethod
    def mutate(root, info, pk, input):
        deferment_request = get_object_or_404(DefermentRequest, pk=pk)
        for field, value in input.items():
            if field == 'student':
                value = get_object_or_404(Student, pk=value)
            elif field == 'file':
                # Handle file upload if needed
                pass
            elif field in ['semester', 'faculty']:
                value = get_object_or_404(Faculty, pk=value)
            setattr(deferment_request, field, value)
        deferment_request.save()
        return UpdateDefermentRequest(deferment_request=deferment_request)


class DeleteCourseRegistrationRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        course_registration_request = get_object_or_404(CourseRegistrationRequest, pk=id)
        course_registration_request.delete()
        return DeleteCourseRegistrationRequest(success=True)


class DeleteStudentCourseParticipant(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        student_course_participant = get_object_or_404(StudentCourseParticipant, pk=id)
        student_course_participant.delete()
        return DeleteStudentCourseParticipant(success=True)


class DeleteCourseCorrectionRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        course_correction_request = get_object_or_404(CourseCorrectionRequest, pk=id)
        course_correction_request.delete()
        return DeleteCourseCorrectionRequest(success=True)


class DeleteReconsiderationRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        reconsideration_request = get_object_or_404(ReconsiderationRequest, pk=id)
        reconsideration_request.delete()
        return DeleteReconsiderationRequest(success=True)


class DeleteEmergencyWithdrawalRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        emergency_withdrawal_request = get_object_or_404(EmergencyWithdrawalRequest, pk=id)
        emergency_withdrawal_request.delete()
        return DeleteEmergencyWithdrawalRequest(success=True)


class DeleteSemesterWithdrawalRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        semester_withdrawal_request = get_object_or_404(SemesterWithdrawalRequest, pk=id)
        semester_withdrawal_request.delete()
        return DeleteSemesterWithdrawalRequest(success=True)


class DeleteDefermentRequest(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        deferment_request = get_object_or_404(DefermentRequest, pk=id)
        deferment_request.delete()
        return DeleteDefermentRequest(success=True)


class Mutation(graphene.ObjectType):
    create_course_registration_request = CreateCourseRegistrationRequest.Field()
    create_student_course_participant = CreateStudentCourseParticipant.Field()
    create_course_correction_request = CreateCourseCorrectionRequest.Field()
    create_reconsideration_request = CreateReconsiderationRequest.Field()
    create_emergency_withdrawal_request = CreateEmergencyWithdrawalRequest.Field()
    create_semester_withdrawal_request = CreateSemesterWithdrawalRequest.Field()
    create_deferment_request = CreateDefermentRequest.Field()

    update_course_registration_request = UpdateCourseRegistrationRequest.Field()
    update_student_course_participant = UpdateStudentCourseParticipant.Field()
    update_course_correction_request = UpdateCourseCorrectionRequest.Field()
    update_reconsideration_request = UpdateReconsiderationRequest.Field()
    update_emergency_withdrawal_request = UpdateEmergencyWithdrawalRequest.Field()
    update_semester_withdrawal_request = UpdateSemesterWithdrawalRequest.Field()
    update_deferment_request = UpdateDefermentRequest.Field()

    delete_course_registration_request = DeleteCourseRegistrationRequest.Field()
    delete_student_course_participant = DeleteStudentCourseParticipant.Field()
    delete_course_correction_request = DeleteCourseCorrectionRequest.Field()
    delete_reconsideration_request = DeleteReconsiderationRequest.Field()
    delete_emergency_withdrawal_request = DeleteEmergencyWithdrawalRequest.Field()
    delete_semester_withdrawal_request = DeleteSemesterWithdrawalRequest.Field()
    delete_deferment_request = DeleteDefermentRequest.Field()


class CourseRegistrationRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    courses = graphene.List(graphene.ID)
    status = graphene.String()


class StudentCourseParticipantFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    status = graphene.String()


class CourseCorrectionRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    dropped_courses = graphene.List(graphene.ID)
    added_courses = graphene.List(graphene.ID)
    status = graphene.String()


class ReconsiderationRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    status = graphene.String()


class EmergencyWithdrawalRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    course = graphene.ID()
    status = graphene.String()


class SemesterWithdrawalRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    count_semester = graphene.Boolean()
    status = graphene.String()


class DefermentRequestFilterInput(graphene.InputObjectType):
    student = graphene.ID()
    semester = graphene.ID()
    faculty = graphene.ID()
    status = graphene.String()


class Query(graphene.ObjectType):
    course_registration_requests = graphene.List(CourseRegistrationRequestType,
                                                 filters=CourseRegistrationRequestFilterInput())
    student_course_participants = graphene.List(StudentCourseParticipantType,
                                                filters=StudentCourseParticipantFilterInput())
    course_correction_requests = graphene.List(CourseCorrectionRequestType,
                                               filters=CourseCorrectionRequestFilterInput())
    reconsideration_requests = graphene.List(ReconsiderationRequestType,
                                             filters=ReconsiderationRequestFilterInput())
    emergency_withdrawal_requests = graphene.List(EmergencyWithdrawalRequestType,
                                                  filters=EmergencyWithdrawalRequestFilterInput())
    semester_withdrawal_requests = graphene.List(SemesterWithdrawalRequestType,
                                                 filters=SemesterWithdrawalRequestFilterInput())
    deferment_requests = graphene.List(DefermentRequestType,
                                       filters=DefermentRequestFilterInput())

    course_registration_request = graphene.Field(CourseRegistrationRequestType, pk=graphene.ID(required=True))
    student_course_participant = graphene.Field(StudentCourseParticipantType, pk=graphene.ID(required=True))
    course_correction_request = graphene.Field(CourseCorrectionRequestType, pk=graphene.ID(required=True))
    reconsideration_request = graphene.Field(ReconsiderationRequestType, pk=graphene.ID(required=True))
    emergency_withdrawal_request = graphene.Field(EmergencyWithdrawalRequestType, pk=graphene.ID(required=True))
    semester_withdrawal_request = graphene.Field(SemesterWithdrawalRequestType, pk=graphene.ID(required=True))
    deferment_request = graphene.Field(DefermentRequestType, pk=graphene.ID(required=True))

    # TODO : if you were in the mood manage the access levels of these queries and mutations
    #  if you weren't I'll do it in the morning

    @login_required
    def resolve_course_registration_requests(self, info, filters=None):
        user = info.context.user
        try:
            student = user.student
        except Student.DoesNotExist:
            student = None
        try:
            professor = user.professor
        except Professor.DoesNotExist:
            professor = None

        filters = filters or {}
        if student is not None:
            filters['student'] = student.id
        elif professor is not None:
            filters['student'] = professor
        return resolve_model_with_filters(CourseRegistrationRequest, filters)

    @login_required
    def resolve_student_course_participants(self, info, filters=None):
        return resolve_model_with_filters(StudentCourseParticipant, filters)

    @login_required
    def resolve_course_correction_requests(self, info, filters=None):
        return resolve_model_with_filters(CourseCorrectionRequest, filters)

    @login_required
    def resolve_reconsideration_requests(self, info, filters=None):
        return resolve_model_with_filters(ReconsiderationRequest, filters)

    @login_required
    def resolve_emergency_withdrawal_requests(self, info, filters=None):
        return resolve_model_with_filters(EmergencyWithdrawalRequest, filters)

    @login_required
    def resolve_semester_withdrawal_requests(self, info, filters=None):
        return resolve_model_with_filters(SemesterWithdrawalRequest, filters)

    @login_required
    def resolve_deferment_requests(self, info, filters=None):
        return resolve_model_with_filters(DefermentRequest, filters)

    @staticmethod
    def resolve_course_registration_request(self, info, pk):
        return get_object_or_404(CourseRegistrationRequest, pk=pk)

    @staticmethod
    def resolve_student_course_participant(self, info, pk):
        return get_object_or_404(StudentCourseParticipant, pk=pk)

    @staticmethod
    def resolve_course_correction_request(self, info, pk):
        return get_object_or_404(CourseCorrectionRequest, pk=pk)

    @staticmethod
    def resolve_reconsideration_request(self, info, pk):
        return get_object_or_404(ReconsiderationRequest, pk=pk)

    @staticmethod
    @login_required
    def resolve_emergency_withdrawal_request(self, info, pk):
        user = info.context.user
        request = get_object_or_404(EmergencyWithdrawalRequest, pk=pk)
        if staff_or_assistant(user):
            try:
                faculty = request.student.major.faculty
                assistant = user.assistant
                if faculty == assistant.faculty:
                    return request
                else:
                    raise GraphQLError("You can only access the requests from your own faculty")
            except ObjectDoesNotExist:
                return request
        else:
            try:
                student = user.student
            except ObjectDoesNotExist:
                raise GraphQLError("You are not a Student")

            if request.student == student:
                return request
            else:
                raise GraphQLError("This request is not yours")

    @staticmethod
    def resolve_semester_withdrawal_request(self, info, pk):
        return get_object_or_404(SemesterWithdrawalRequest, pk=pk)

    @staticmethod
    def resolve_deferment_request(self, info, pk):
        return get_object_or_404(DefermentRequest, pk=pk)


schema = graphene.Schema(query=Query, mutation=Mutation)
