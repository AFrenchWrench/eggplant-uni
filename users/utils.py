import secrets
from random import randint


def main():
    pass


def generate_student_id():
    from users.models import Student

    while True:
        code = randint(30000000, 39999999)
        try:
            Student.objects.get(code=code)
            continue
        except:
            return code


def generate_professor_id():
    from users.models import Professor

    while True:
        code = randint(20000000, 29999999)
        try:
            Professor.objects.get(code=code)
            continue
        except:
            return code


def generate_assistant_id():
    from users.models import Assistant

    while True:
        code = randint(10000000, 19999999)
        try:
            Assistant.objects.get(code=code)
            continue
        except:
            return code


def generate_code():
    number_string = ''.join([str(secrets.randbelow(10)) for _ in range(10)])
    return number_string


def generate_4_length_code():
    number_string = ''.join([str(secrets.randbelow(10)) for _ in range(4)])
    return number_string


if __name__ == '__main__':
    main()
