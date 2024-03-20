from django.views.generic import View


# Filters : first and last name, student_id, national_id, faculty, major, year_of_admission, military_status
# POST and GET
class StudentListView(View):
    pass


# GET, PUT and DELETE
class StudentDetailView(View):
    pass


# Filters : first and last name, professor_id, national_id, faculty, major, rank
# POST and GET
class ProfessorListView(View):
    pass


# GET, PUT and DELETE
class ProfessorDetailView(View):
    pass


# Filters : first and last name, assistant_id, national_id, faculty, major
# POST and GET
class AssistantListView(View):
    pass


# GET, PUT and DELETE
class AssistantDetailView(View):
    pass


# POST and GET
class FacultyListView(View):
    pass


# GET, PUT and DELETE
class FacultyDetailView(View):
    pass


# POST and GET
class SemesterListView(View):
    pass


# GET, PUT and DELETE
class SemesterDetailView(View):
    pass
