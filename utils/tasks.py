from celery import shared_task
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from graphql import GraphQLError
from redis import Redis


@shared_task
def send_email(to, subject, text):
    try:
        send_mail(
            subject,
            text,
            settings.EMAIL_HOST_USER,  # sender email
            [to],
            fail_silently=False,
        )
        return True
    except Exception as e:
        raise GraphQLError(str(e))


@shared_task
def send_course_approval_and_schedule_email(student_email, course_names, weekly_schedule):
    student_subject = "Course Registration Approval"
    student_text = f"""
    Dear Student,

    Your course registration request has been approved by the instructor.

    Approved Courses:
    {', '.join(course_names)}

    Weekly Schedule:
    {weekly_schedule}

    Best Regards,
    [Your University Name]
    """
    send_email(student_email, student_subject, student_text)

    # Send email to instructor if student doesn't submit the form
    professor_email = "[instructor_email_here]"  # Replace with the instructor's email address
    instructor_subject = "Pending Course Registration Approval"
    instructor_text = f"""
    Dear Instructor,

    The following student has been approved for the following courses, but has not submitted the registration form yet:

    Student Email: {student_email}
    Approved Courses:
    {', '.join(course_names)}

    Please follow up with the student.

    Best Regards,
    [Your University Name]
    """
    send_email(professor_email, instructor_subject, instructor_text)


def generate_weekly_schedule(semester_courses):
    weekly_schedule = {}
    for course in semester_courses:
        weekly_schedule[course.name] = course.schedule  # Assuming each course has a schedule attribute

