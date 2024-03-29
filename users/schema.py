import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model, logout, login, authenticate
from graphql import GraphQLError

from users.models import (
    Student,
    Professor,
    Assistant,
)

from university.models import (
    Semester,
    Faculty,
    Major,
)

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User


class StudentType(DjangoObjectType):
    class Meta:
        model = Student


class ProfessorType(DjangoObjectType):
    class Meta:
        model = Professor


class AssistantType(DjangoObjectType):
    class Meta:
        model = Assistant


class MajorType(DjangoObjectType):
    class Meta:
        model = Major


class SemesterType(DjangoObjectType):
    class Meta:
        model = Semester


class FacultyType(DjangoObjectType):
    class Meta:
        model = Faculty


class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    national_id = graphene.String(required=True)
    gender = graphene.String(required=True)
    birth_date = graphene.Date(required=True)
    user_code = graphene.String(required=True)


class CreateStudentInput(graphene.InputObjectType):
    admission_year = graphene.Int(required=True)
    admission_semester = graphene.Int(required=True)
    major = graphene.Int(required=True)
    advisor = graphene.Int(required=False)
    military_status = graphene.Boolean(required=True)


class CreateProfessorInput(graphene.InputObjectType):
    major = graphene.Int(required=True)
    specialization = graphene.String(required=True)
    rank = graphene.String(required=True)


class CreateAssistantInput(graphene.InputObjectType):
    faculty = graphene.Int(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        base_user_input = CreateUserInput(required=True)
        student_input = CreateStudentInput()
        professor_input = CreateProfessorInput()
        assistant_input = CreateAssistantInput()

    user = graphene.Field(UserType)
    student = graphene.Field(StudentType)
    professor = graphene.Field(ProfessorType)
    assistant = graphene.Field(AssistantType)

    @staticmethod
    def mutate(root, info, base_user_input, student_input=None, professor_input=None, assistant_input=None):

        # Create the associated models if provided
        if student_input:
            student = CreateUser._create_student(base_user_input, student_input)
            return CreateUser(student=student)
        elif professor_input:
            professor = CreateUser._create_professor(base_user_input, professor_input)
            return CreateUser(professor=professor)
        elif assistant_input:
            assistant = CreateUser._create_assistant(base_user_input, assistant_input)
            return CreateUser(assistant=assistant)

        # Create the user
        user = User.objects.create_user(**base_user_input)

        # Return the created objects
        return CreateUser(user=user)

    @staticmethod
    def _create_student(base_user_input, student_input):
        student_input['admission_semester'] = get_object_or_404(Semester, id=student_input['admission_semester'])
        student_input['major'] = get_object_or_404(Major, id=student_input['major'])
        try:
            if student_input['advisor']:
                student_input['advisor'] = get_object_or_404(Professor, id=student_input.get('advisor'))
        except KeyError:
            student_input['advisor'] = None
        user = User.objects.create_user(**base_user_input)

        return Student.objects.create(user=user, **student_input)

    @staticmethod
    def _create_professor(base_user_input, professor_input):
        professor_input['major'] = get_object_or_404(Major, id=professor_input['major'])
        user = User.objects.create_user(**base_user_input)

        return Professor.objects.create(user=user, **professor_input)

    @staticmethod
    def _create_assistant(base_user_input, assistant_input):
        assistant_input['faculty'] = get_object_or_404(Faculty, id=assistant_input['faculty'])
        user = User.objects.create_user(**base_user_input)

        return Assistant.objects.create(user=user, **assistant_input)


class UpdateUserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    national_id = graphene.String()
    gender = graphene.String()
    birth_date = graphene.Date()
    user_code = graphene.String()


class UpdateStudentInput(graphene.InputObjectType):
    admission_year = graphene.Int()
    admission_semester = graphene.Int()
    major = graphene.Int()
    advisor = graphene.Int()
    military_status = graphene.Boolean()


class UpdateProfessorInput(graphene.InputObjectType):
    major = graphene.Int()
    specialization = graphene.String()
    rank = graphene.String()


class UpdateAssistantInput(graphene.InputObjectType):
    faculty = graphene.Int()


class UpdateUser(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        base_user_input = UpdateUserInput(required=True)
        student_input = UpdateStudentInput()
        professor_input = UpdateProfessorInput()
        assistant_input = UpdateAssistantInput()

    user = graphene.Field(UserType)
    student = graphene.Field(StudentType)
    professor = graphene.Field(ProfessorType)
    assistant = graphene.Field(AssistantType)

    @staticmethod
    def mutate(root, info, pk, base_user_input, student_input=None, professor_input=None, assistant_input=None):
        # Update the base user information
        user = get_object_or_404(User, id=pk)
        for field, value in base_user_input.items():
            setattr(user, field, value)

        # Update associated models if provided
        if student_input:
            UpdateUser._update_student(user, student_input)
        elif professor_input:
            UpdateUser._update_professor(user, professor_input)
        elif assistant_input:
            UpdateUser._update_assistant(user, assistant_input)

        user.save()
        # Return the updated objects
        return UpdateUser(user=user)

    @staticmethod
    def _update_student(user, student_input):
        student = get_object_or_404(Student, user=user)
        for field, value in student_input.items():
            if field == 'major' and value is not None:
                value = get_object_or_404(Major, id=value)
            elif field == 'advisor' and value is not None:
                value = get_object_or_404(Professor, id=value)
            setattr(student, field, value)
        student.save()
        return student

    @staticmethod
    def _update_professor(user, professor_input):
        professor = get_object_or_404(Professor, user=user)
        for field, value in professor_input.items():
            if field == 'major' and value is not None:
                value = get_object_or_404(Major, id=value)
            setattr(professor, field, value)
        professor.save()
        return professor

    @staticmethod
    def _update_assistant(user, assistant_input):
        assistant = get_object_or_404(Assistant, user=user)
        for field, value in assistant_input.items():
            if field == 'faculty' and value is not None:
                value = get_object_or_404(Faculty, id=value)
            setattr(assistant, field, value)
        assistant.save()
        return assistant


class DeleteUser(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    stat = graphene.Boolean()

    @staticmethod
    def mutate(root, info, pk):
        user = get_object_or_404(User, id=pk)
        user.delete()
        stat = True
        return DeleteUser(stat=stat)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise GraphQLError('Invalid username or password.')
        login(info.context, user)
        return Login(user=user)


class Logout(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)
        return Logout(success=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login = Login.Field()
    logout = Logout.Field()


class StudentFilterInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    user_code = graphene.String()
    national_id = graphene.String()
    faculty = graphene.Int()
    major = graphene.Int()
    admission_year = graphene.Int()
    military_status = graphene.Boolean()


class ProfessorFilterInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    user_code = graphene.String()
    national_id = graphene.String()
    faculty = graphene.Int()
    major = graphene.Int()
    rank = graphene.String()


class AssistantFilterInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    user_code = graphene.String()
    national_id = graphene.String()
    faculty = graphene.Int()
    major = graphene.Int()


class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, id=graphene.ID(required=True))
    professor = graphene.Field(ProfessorType, id=graphene.ID(required=True))
    assistant = graphene.Field(AssistantType, id=graphene.ID(required=True))

    students = graphene.List(StudentType, filters=StudentFilterInput())
    professors = graphene.List(ProfessorType, filters=ProfessorFilterInput())
    assistants = graphene.List(AssistantType, filters=AssistantFilterInput())

    current_user = graphene.Field(UserType)

    def resolve_student(self, info, id):
        return get_object_or_404(Student, id=id)

    def resolve_professor(self, info, id):
        return get_object_or_404(Professor, id=id)

    def resolve_assistant(self, info, id):
        return get_object_or_404(Assistant, id=id)

    def resolve_students(self, info, filters=None):
        queryset = Student.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code=filters.user_code)
            if filters.national_id:
                queryset = queryset.filter(user__national_id=filters.national_id)
            if filters.faculty:
                queryset = queryset.filter(faculty_id=filters.faculty)
            if filters.major:
                queryset = queryset.filter(major_id=filters.major)
            if filters.admission_year:
                queryset = queryset.filter(admission_year=filters.admission_year)
            if filters.military_status is not None:
                queryset = queryset.filter(military_status=filters.military_status)

        return queryset

    def resolve_professors(self, info, filters=None):
        queryset = Professor.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code=filters.user_code)
            if filters.national_id:
                queryset = queryset.filter(user__national_id=filters.national_id)
            if filters.faculty:
                queryset = queryset.filter(faculty_id=filters.faculty)
            if filters.major:
                queryset = queryset.filter(major_id=filters.major)
            if filters.rank:
                queryset = queryset.filter(rank=filters.rank)

        return queryset

    def resolve_assistants(self, info, filters=None):
        queryset = Assistant.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code=filters.user_code)
            if filters.national_id:
                queryset = queryset.filter(user__national_id=filters.national_id)
            if filters.faculty:
                queryset = queryset.filter(faculty_id=filters.faculty)
            if filters.major:
                queryset = queryset.filter(major_id=filters.major)

        return queryset

    def resolve_current_user(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User not logged in.')
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
