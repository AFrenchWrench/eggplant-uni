# import graphene
# from graphene_django.types import DjangoObjectType
# from django.shortcuts import get_object_or_404
#
# from university.models import Course
# from users.models import Student
# from .models import (
#     CourseRegistrationRequest,
#     StudentCourseParticipant,
#     CourseCorrectionRequest,
#     ReconsiderationRequest,
#     EmergencyWithdrawalRequest,
#     SemesterWithdrawalRequest,
#     DefermentRequest,
# )
#
#
# class CourseRegistrationRequestType(DjangoObjectType):
#     class Meta:
#         model = CourseRegistrationRequest
#
#
# class StudentCourseParticipantType(DjangoObjectType):
#     class Meta:
#         model = StudentCourseParticipant
#
#
# class CourseCorrectionRequestType(DjangoObjectType):
#     class Meta:
#         model = CourseCorrectionRequest
#
#
# class ReconsiderationRequestType(DjangoObjectType):
#     class Meta:
#         model = ReconsiderationRequest
#
#
# class EmergencyWithdrawalRequestType(DjangoObjectType):
#     class Meta:
#         model = EmergencyWithdrawalRequest
#
#
# class SemesterWithdrawalRequestType(DjangoObjectType):
#     class Meta:
#         model = SemesterWithdrawalRequest
#
#
# class DefermentRequestType(DjangoObjectType):
#     class Meta:
#         model = DefermentRequest
#
#
# class CourseRegistrationRequestInput(graphene.InputObjectType):
#     student = graphene.ID(required=True)
#     courses = graphene.List(graphene.ID, required=True)
#
#
# class StudentCourseParticipantInput(graphene.InputObjectType):
#     student = graphene.ID(required=True)
#     semester_course = graphene.ID(required=True)
#     status = graphene.String()
#
#
# class CourseCorrectionRequestInput(graphene.InputObjectType):
#     dropped_courses = graphene.List(graphene.ID, required=True)
#     added_courses = graphene.List(graphene.ID, required=True)
#     status = graphene.String()
#
#
# class ReconsiderationRequestInput(graphene.InputObjectType):
#     course = graphene.ID(required=True)
#     text = graphene.String(required=True)
#     response = graphene.String()
#
#
# class EmergencyWithdrawalRequestInput(graphene.InputObjectType):
#     course = graphene.ID(required=True)
#     text = graphene.String(required=True)
#     response = graphene.String()
#
#
# class SemesterWithdrawalRequestInput(graphene.InputObjectType):
#     semester = graphene.ID(required=True)
#     text = graphene.String(required=True)
#     response = graphene.String()
#     count_semester = graphene.Boolean()
#     status = graphene.String()
#
#
# class DefermentRequestInput(graphene.InputObjectType):
#     student = graphene.ID(required=True)
#     file = graphene.String(required=True)
#     semester = graphene.ID(required=True)
#     faculty = graphene.ID(required=True)
#     status = graphene.String()
#
#
# class CreateCourseRegistrationRequest(graphene.Mutation):
#     class Arguments:
#         input = CourseRegistrationRequestInput(required=True)
#
#     course_registration_request = graphene.Field(CourseRegistrationRequestType)
#
#     @staticmethod
#     def mutate(self, info, input):
#         course_registration_request = input
#         course_registration_request['student'] = get_object_or_404(Student, id=course_registration_request['student'])
#         course_registration_request.courses.set(input['courses'])
#         i = 0
#         for course in course_registration_request['courses']:
#             course_registration_request['courses'][i] = get_object_or_404(Course, id=course)
#             i += 1
#         course_registration_request = CourseRegistrationRequest.objects.create(**course_registration_request)
#         return CreateCourseRegistrationRequest(course_registration_request=course_registration_request)
#
#
# class UpdateStudentCourseParticipant(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         input = StudentCourseParticipantInput(required=True)
#
#     student_course_participant = graphene.Field(StudentCourseParticipantType)
#
#     @staticmethod
#     def mutate(self, info, id, input):
#         student_course_participant = get_object_or_404(StudentCourseParticipant, pk=id)
#         student_course_participant.student_id = input['student']
#         student_course_participant.semester_course_id = input['semester_course']
#         student_course_participant.status = input['status']
#         student_course_participant.save()
#         return UpdateStudentCourseParticipant(student_course_participant=student_course_participant)
#
#
# class Query(graphene.ObjectType):
#     course_registration_requests = graphene.List(CourseRegistrationRequestType)
#     student_course_participants = graphene.List(StudentCourseParticipantType)
#     course_correction_requests = graphene.List(CourseCorrectionRequestType)
#     reconsideration_requests = graphene.List(ReconsiderationRequestType)
#     emergency_withdrawal_requests = graphene.List(EmergencyWithdrawalRequestType)
#     semester_withdrawal_requests = graphene.List(SemesterWithdrawalRequestType)
#     deferment_requests = graphene.List(DefermentRequestType)
#
#     def resolve_course_registration_requests(self, info):
#         return CourseRegistrationRequest.objects.all()
#
#     def resolve_student_course_participants(self, info):
#         return StudentCourseParticipant.objects.all()
#
#     def resolve_course_correction_requests(self, info):
#         return CourseCorrectionRequest.objects.all()
#
#     def resolve_reconsideration_requests(self, info):
#         return ReconsiderationRequest.objects.all()
#
#     def resolve_emergency_withdrawal_requests(self, info):
#         return EmergencyWithdrawalRequest.objects.all()
#
#     def resolve_semester_withdrawal_requests(self, info):
#         return SemesterWithdrawalRequest.objects.all()
#
#     def resolve_deferment_requests(self, info):
#         return DefermentRequest.objects.all()
#
#
# class Mutation(graphene.ObjectType):
#     create_course_registration_request = CreateCourseRegistrationRequest.Field()
#     update_student_course_participant = UpdateStudentCourseParticipant.Field()
