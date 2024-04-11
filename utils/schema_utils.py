from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist

from admin_dash.models import BurnedTokens


def main():
    pass


def resolve_model_with_filters(model_class, filter_input=None):
    queryset = model_class.objects.all()
    if filter_input:
        for field, value in filter_input.items():
            if '__icontains' in field:
                field_name = field.split('__icontains')[0]
                print(field_name)
                queryset = queryset.filter(**{f'{field_name}__icontains': value})
            else:
                queryset = queryset.filter(**{field: value})
    return queryset


def staff_or_same_faculty_assistant(user, faculty):
    try:
        if user.assistant.faculty == faculty:
            return True
        elif user.assistant.faculty != faculty:
            raise GraphQLError(
                f'You are not allowed to alter information of other faculties! Your faculty id is {user.assistant.faculty.id}')
    except ObjectDoesNotExist:
        if user.is_staff:
            return True
        raise GraphQLError("You are not allowed to do this operation!")


def staff_or_assistant(user):
    try:
        if user.assistant.faculty:
            return True
    except ObjectDoesNotExist:
        if user.is_staff:
            return True
        return False


def login_required(func):
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
        token = info.context.headers.get('Authorization')
        try:
            BurnedTokens.objects.get(token=token)
            token = False
        except BurnedTokens.DoesNotExist:
            token = True
        if user.is_authenticated and token:
            return func(root, info, *args, **kwargs)
        else:
            raise GraphQLError("Your are not logged in")

    return wrapper


def staff_member_required(func):
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
        token = info.context.headers.get('Authorization')
        try:
            BurnedTokens.objects.get(token=token)
            token = False
        except BurnedTokens.DoesNotExist:
            token = True

        if user.is_authenticated and user.is_staff and token:
            return func(root, info, *args, **kwargs)
        else:
            raise GraphQLError("You do not have permission to perform this action.")

    return wrapper


def send_email(to, subject, text):


if __name__ == '__main__':
    main()
