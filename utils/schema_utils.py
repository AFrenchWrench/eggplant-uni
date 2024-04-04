from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist


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


if __name__ == '__main__':
    main()
