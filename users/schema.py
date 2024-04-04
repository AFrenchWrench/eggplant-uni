import graphene
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql import (
    GraphQLError,
)
from graphql_jwt.decorators import (
    staff_member_required,
    login_required,
)
from graphql_jwt.shortcuts import get_token

from university.models import (
    Semester,
    Faculty,
    Major,
)
from users.forms import (
    UserForm,
    UpdateUserForm,
    ProfessorForm,
    UpdateProfessorForm,
)
from users.models import (
    Student,
    Professor,
    Assistant,
)
from utils.schema_utils import resolve_model_with_filters, staff_or_assistant

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
    # image = Upload(required=True)
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
    major = graphene.ID(required=True)


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
    @staff_member_required
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

            user = User.objects.create_user(**base_user_input, is_staff=True)

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
        assistant_input['major'] = get_object_or_404(Major, pk=assistant_input['major'])
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
    image = Upload()
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
    major = graphene.ID()


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
    @staff_member_required
    def mutate(root, info, pk, base_user_input=None, student_input=None, professor_input=None, assistant_input=None):
        form = UpdateUserForm(base_user_input)
        if form.is_valid() or base_user_input is None:

            user = get_object_or_404(User, pk=pk)

            if base_user_input is not None:
                for field, value in base_user_input.items():
                    setattr(user, field, value)

            if student_input:
                student = UpdateUser._update_student(user, student_input)
                return UpdateUser(student=student)
            elif professor_input:
                form = UpdateProfessorForm(professor_input)
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
        elif [base_user_input, student_input, professor_input, assistant_input] == [None, None, None, None]:
            raise GraphQLError('At least one input type should be filled')
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
            if field == 'major' and value is not None:
                value = get_object_or_404(Major, pk=value)
            setattr(assistant, field, value)
        assistant.save()
        return assistant


class DeleteUser(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    stat = graphene.Boolean()

    @staticmethod
    @staff_member_required
    def mutate(root, info, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        stat = True
        return DeleteUser(stat=stat)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, username, password):
        if info.context.user.is_authenticated:
            raise GraphQLError("You are already logged in")

        user = authenticate(username=username, password=password)
        if user is None:
            raise GraphQLError('Invalid username or password')

        token = get_token(user)
        return Login(token=token, user=user)


# class Logout(graphene.Mutation):
#     success = graphene.Boolean()
#
#     @staticmethod
#     @login_required
#     def mutate(root, info):
#         token = RefreshToken(info.context.user)
#         token.blacklist()
#         return Logout(success=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login = Login.Field()
    # logout = Logout.Field()


class StudentFilterInput(graphene.InputObjectType):
    user__first_name__icontains = graphene.String()
    user__last_name__icontains = graphene.String()
    user__user_code__icontains = graphene.String()
    user__national_id__icontains = graphene.String()
    major__faculty = graphene.ID()
    major = graphene.ID()
    admission_year = graphene.Int()
    military_status = graphene.Boolean()


class ProfessorFilterInput(graphene.InputObjectType):
    user__first_name__icontains = graphene.String()
    user__last_name__icontains = graphene.String()
    user__user_code__icontains = graphene.String()
    user__national_id__icontains = graphene.String()
    major__faculty = graphene.ID()
    major = graphene.ID()
    rank = graphene.String()


class AssistantFilterInput(graphene.InputObjectType):
    user__first_name__icontains = graphene.String()
    user__last_name__icontains = graphene.String()
    user__user_code__icontains = graphene.String()
    user__national_id__icontains = graphene.String()
    faculty = graphene.ID()
    major = graphene.ID()


class Query(graphene.ObjectType):
    student = graphene.Field(StudentType, pk=graphene.ID())
    professor = graphene.Field(ProfessorType, pk=graphene.ID())
    assistant = graphene.Field(AssistantType, pk=graphene.ID())

    students = graphene.List(StudentType, filters=StudentFilterInput())
    professors = graphene.List(ProfessorType, filters=ProfessorFilterInput())
    assistants = graphene.List(AssistantType, filters=AssistantFilterInput())

    current_user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def resolve_student(root, info, pk=None):
        if staff_or_assistant(info.context.user):
            student = get_object_or_404(Student, pk=pk)
            try:
                faculty = info.context.user.assistant.faculty
                if student.major.faculty == faculty:
                    return student
                else:
                    raise GraphQLError("This student is not in your faculty")
            except ObjectDoesNotExist:
                pass
            return student
        else:
            user = info.context.user
            try:
                student = user.student
            except ObjectDoesNotExist:
                raise GraphQLError("You are not a student")

            return student

    @staticmethod
    @login_required
    def resolve_professor(root, info, pk=None):
        if staff_or_assistant(info.context.user):
            professor = get_object_or_404(Professor, pk=pk)
            try:
                faculty = info.context.user.assistant.faculty
                if professor.major.faculty == faculty:
                    return professor
                else:
                    raise GraphQLError("This professor is not in your faculty")
            except ObjectDoesNotExist:
                pass
            return professor
        else:
            user = info.context.user
            try:
                professor = user.professor
            except ObjectDoesNotExist:
                raise GraphQLError("You are not a professor")

            return professor

    @staticmethod
    @staff_member_required
    def resolve_assistant(root, info, pk):
        return get_object_or_404(Assistant, pk=pk)

    @staticmethod
    @login_required
    def resolve_students(root, info, filters=None):
        if staff_or_assistant(info.context.user):
            try:
                if filters is None:
                    filters = {}
                filters['major__faculty'] = info.context.user.assistant.faculty.id
            except ObjectDoesNotExist:
                pass
            return resolve_model_with_filters(Student, filters)

    @staticmethod
    @login_required
    def resolve_professors(root, info, filters=None):
        if staff_or_assistant(info.context.user):
            try:
                if filters is None:
                    filters = {}
                filters['major__faculty'] = info.context.user.assistant.faculty.id
            except ObjectDoesNotExist:
                pass
            return resolve_model_with_filters(Professor, filters)

    @staticmethod
    @staff_member_required
    def resolve_assistants(root, info, filters=None):
        return resolve_model_with_filters(Assistant, filters)

    @staticmethod
    def resolve_current_user(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User not logged in.')
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)
