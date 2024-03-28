import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model, logout, login, authenticate
from graphql import GraphQLError

from users.models import (
    Student,
    Professor,
    Assistant,
)

from university.models import (
    Semester, Faculty,
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
    major_id = graphene.Int(required=True)
    advisor_id = graphene.Int(required=False)
    military_status = graphene.Boolean(required=True)


class CreateProfessorInput(graphene.InputObjectType):
    major_id = graphene.Int(required=True)
    specialization = graphene.String(required=True)
    rank = graphene.String(required=True)


class CreateAssistantInput(graphene.InputObjectType):
    faculty_id = graphene.Int(required=True)


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
    def mutate(root, info, base_user_input=None, student_input=None, professor_input=None, assistant_input=None):
        user = User.objects.create_user(**base_user_input)
        if student_input:
            student = Student.objects.create(user=user, **student_input)
            return CreateUser(user=user, student=student)
        elif professor_input:
            professor = Professor.objects.create(user=user, **professor_input)
            return CreateUser(user=user, professor=professor)
        elif assistant_input:
            assistant = Assistant.objects.create(user=user, **assistant_input)
            return CreateUser(user=user, assistant=assistant)
        else:
            return CreateUser(user=user)


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


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateUserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        user = User.objects.get(id=id)
        if user:
            for field, value in input.items():
                setattr(user, field, value)
            user.save()
            return UpdateUser(user=user)
        else:
            return None


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    user_id = graphene.ID()

    @staticmethod
    def mutate(root, info, id):
        try:
            user = User.objects.get(pk=id)
            user_id = user.id
            user.delete()
            return DeleteUser(user_id=user_id)
        except User.DoesNotExist:
            return DeleteUser(user_id=None)


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


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    current_user = graphene.Field(UserType)

    def resolve_current_user(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User not logged in.')
        return user

    def resolve_users(self, info):
        return User.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)
