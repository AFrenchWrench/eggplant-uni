import graphene
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from graphql import GraphQLError, GraphQLResolveInfo

from university.models import (
    Semester,
    Faculty,
    Major,
)
from users.forms import UserForm, UpdateUserForm, ProfessorForm
from users.models import (
    Student,
    Professor,
    Assistant,
)


def login_required():
    def wrapper(func):
        def ret(*args, **kwargs):
            info = None
            for a in args:
                if type(a) == GraphQLResolveInfo:
                    info = a
            if info:
                if info.context.user.is_authenticated:
                    return func(*args, **kwargs)
                else:
                    raise GraphQLError('You Are Not Authenticate')
            else:
                raise GraphQLError('Server Error')

        return ret

    return wrapper


def staff_required():
    def wrapper(func):
        def ret(*args, **kwargs):
            info = None
            for a in args:
                if type(a) == GraphQLResolveInfo:
                    info = a
            if info:
                if info.context.user.is_staff:
                    return func(*args, **kwargs)
                else:
                    raise GraphQLError('You Are Not Authorized')
            else:
                raise GraphQLError('Server Error')

        return ret

    return wrapper


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
    admission_semester = graphene.ID(required=True)
    major = graphene.ID(required=True)
    advisor = graphene.ID(required=False)
    military_status = graphene.Boolean(required=True)


class CreateProfessorInput(graphene.InputObjectType):
    major = graphene.ID(required=True)
    specialization = graphene.String(required=True)
    rank = graphene.String(required=True)


class CreateAssistantInput(graphene.InputObjectType):
    faculty = graphene.ID(required=True)


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
        form = UserForm(base_user_input)
        if form.is_valid():
            if student_input:
                student = CreateUser._create_student(base_user_input, student_input)
                return CreateUser(student=student)
            elif professor_input:
                form = ProfessorForm(professor_input)
                if form.is_valid():
                    professor = CreateUser._create_professor(base_user_input, professor_input)
                    return CreateUser(professor=professor)
                else:
                    errors = form.errors.as_data()
                    error_messages = [error[0].messages[0] for error in errors.values()]
                    raise GraphQLError(', '.join(error_messages))
            elif assistant_input:
                assistant = CreateUser._create_assistant(base_user_input, assistant_input)
                return CreateUser(assistant=assistant)

            user = User.objects.create_user(**base_user_input)

            return CreateUser(user=user)
        else:
            errors = form.errors.as_data()
            error_messages = [error[0].messages[0] for error in errors.values()]
            raise GraphQLError(', '.join(error_messages))

    @staticmethod
    def _create_student(base_user_input, student_input):
        student_input['admission_semester'] = get_object_or_404(Semester, pk=student_input['admission_semester'])
        student_input['major'] = get_object_or_404(Major, pk=student_input['major'])
        try:
            if student_input['advisor']:
                student_input['advisor'] = get_object_or_404(Professor, pk=student_input.get('advisor'))
        except KeyError:
            student_input['advisor'] = None
        user = User.objects.create_user(**base_user_input)

        return Student.objects.create(user=user, **student_input)

    @staticmethod
    def _create_professor(base_user_input, professor_input):
        professor_input['major'] = get_object_or_404(Major, pk=professor_input['major'])
        user = User.objects.create_user(**base_user_input)

        return Professor.objects.create(user=user, **professor_input)

    @staticmethod
    def _create_assistant(base_user_input, assistant_input):
        assistant_input['faculty'] = get_object_or_404(Faculty, pk=assistant_input['faculty'])
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
    admission_semester = graphene.ID()
    major = graphene.ID()
    advisor = graphene.ID()
    military_status = graphene.Boolean()


class UpdateProfessorInput(graphene.InputObjectType):
    major = graphene.ID()
    specialization = graphene.String()
    rank = graphene.String()


class UpdateAssistantInput(graphene.InputObjectType):
    faculty = graphene.ID()


class UpdateUser(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        base_user_input = UpdateUserInput()
        student_input = UpdateStudentInput()
        professor_input = UpdateProfessorInput()
        assistant_input = UpdateAssistantInput()

    user = graphene.Field(UserType)
    student = graphene.Field(StudentType)
    professor = graphene.Field(ProfessorType)
    assistant = graphene.Field(AssistantType)

    @staticmethod
    def mutate(root, info, pk, base_user_input={}, student_input=None, professor_input=None, assistant_input=None):
        form = UpdateUserForm(base_user_input)
        if form.is_valid() or not base_user_input:

            user = get_object_or_404(User, pk=pk)
            for field, value in base_user_input.items():
                setattr(user, field, value)

            if student_input:
                student = UpdateUser._update_student(user, student_input)
                return UpdateUser(student=student)
            elif professor_input:

                form = ProfessorForm(professor_input)
                if form.is_valid():
                    professor = UpdateUser._update_professor(user, professor_input)
                    return UpdateUser(professor=professor)
                else:
                    errors = form.errors.as_data()
                    error_messages = [error[0].messages[0] for error in errors.values()]
                    raise GraphQLError(', '.join(error_messages))

            elif assistant_input:
                assistant = UpdateUser._update_assistant(user, assistant_input)
                return UpdateUser(assistant=assistant)

            user.save()
            return UpdateUser(user=user)
        else:
            errors = form.errors.as_data()
            error_messages = [error[0].messages[0] for error in errors.values()]
            raise GraphQLError(', '.join(error_messages))

    @staticmethod
    def _update_student(user, student_input):
        student = get_object_or_404(Student, user=user)
        for field, value in student_input.items():
            if field == 'major' and value is not None:
                value = get_object_or_404(Major, pk=value)
            elif field == 'advisor' and value is not None:
                value = get_object_or_404(Professor, pk=value)
            setattr(student, field, value)
        student.save()
        return student

    @staticmethod
    def _update_professor(user, professor_input):
        professor = get_object_or_404(Professor, user=user)
        for field, value in professor_input.items():
            if field == 'major' and value is not None:
                value = get_object_or_404(Major, pk=value)
            setattr(professor, field, value)
        professor.save()
        return professor

    @staticmethod
    def _update_assistant(user, assistant_input):
        assistant = get_object_or_404(Assistant, user=user)
        for field, value in assistant_input.items():
            if field == 'faculty' and value is not None:
                value = get_object_or_404(Faculty, pk=value)
            setattr(assistant, field, value)
        assistant.save()
        return assistant


class DeleteUser(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    stat = graphene.Boolean()

    @staticmethod
    def mutate(root, info, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        stat = True
        return DeleteUser(stat=stat)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise GraphQLError('Invalid username or password.')
        login(info.context, user)
        return Login(user=user)


class Logout(graphene.Mutation):
    success = graphene.Boolean()

    @staticmethod
    def mutate(info):
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
    faculty = graphene.ID()
    major = graphene.ID()
    admission_year = graphene.Int()
    military_status = graphene.Boolean()


class ProfessorFilterInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    user_code = graphene.String()
    national_id = graphene.String()
    faculty = graphene.ID()
    major = graphene.ID()
    rank = graphene.String()


class AssistantFilterInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    user_code = graphene.String()
    national_id = graphene.String()
    faculty = graphene.ID()
    major = graphene.ID()


class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, pk=graphene.ID(required=True))
    professor = graphene.Field(ProfessorType, pk=graphene.ID(required=True))
    assistant = graphene.Field(AssistantType, pk=graphene.ID(required=True))

    students = graphene.List(StudentType, filters=StudentFilterInput())
    professors = graphene.List(ProfessorType, filters=ProfessorFilterInput())
    assistants = graphene.List(AssistantType, filters=AssistantFilterInput())

    current_user = graphene.Field(UserType)

    @staticmethod
    def resolve_student(info, pk):
        return get_object_or_404(Student, pk=pk)

    @staticmethod
    def resolve_professor(info, pk):
        return get_object_or_404(Professor, pk=pk)

    @staticmethod
    def resolve_assistant(info, pk):
        return get_object_or_404(Assistant, pk=pk)

    @staticmethod
    def resolve_students(info, filters=None):
        queryset = Student.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code__icontains=filters.user_code)
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

    @login_required()
    @staff_required()
    def resolve_professors(self, info, filters=None):
        queryset = Professor.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code__icontains=filters.user_code)
            if filters.national_id:
                queryset = queryset.filter(user__national_id=filters.national_id)
            if filters.faculty:
                queryset = queryset.filter(faculty_id=filters.faculty)
            if filters.major:
                queryset = queryset.filter(major_id=filters.major)
            if filters.rank:
                queryset = queryset.filter(rank=filters.rank)

        return queryset

    @staticmethod
    def resolve_assistants(info, filters=None):
        queryset = Assistant.objects.all()

        if filters:
            if filters.first_name:
                queryset = queryset.filter(user__first_name__icontains=filters.first_name)
            if filters.last_name:
                queryset = queryset.filter(user__last_name__icontains=filters.last_name)
            if filters.user_code:
                queryset = queryset.filter(user__user_code__icontains=filters.user_code)
            if filters.national_id:
                queryset = queryset.filter(user__national_id=filters.national_id)
            if filters.faculty:
                queryset = queryset.filter(faculty_id=filters.faculty)
            if filters.major:
                queryset = queryset.filter(major_id=filters.major)

        return queryset

    @staticmethod
    def resolve_current_user(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User not logged in.')
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
