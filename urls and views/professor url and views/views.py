from django.views.generic import View


# GET can only be accessed by the assistant
# Filters : first and last name, professor_id, national_id, faculty, major, rank
class ProfessorListView(View):
    pass


# GET can only be accessed by the assistant or the professor him/herself and PUT can only be accessed by the professor
class ProfessorDetailView(View):
    pass


class ProfessorCourseAppealRequestsListView(View):
    pass


class ProfessorCourseAppealRequestDetailView(View):
    pass


class ProfessorCourseAppealRequestCreateView(View):
    pass


class ProfessorCourseApproveView(View):
    pass


class ProfessorCourseScoresCreateView(View):
    pass


# GET , advisor can see his/her students
class ProfessorStudentsSelectionFormsView(View):
    pass


# GET, POST , advisor can see his/her students
class ProfessorStudentsSelectionFormDetailView(View):
    pass


# GET, POST , advisor can see his/her students
class ProfessorStudentsSubstitutionFormsView(View):
    pass


# GET, POST , advisor can see his/her students
class ProfessorStudentsSubstitutionFormDetailView(View):
    pass


# GET, POST , advisor can see his/her students
class ProfessorStudentsSubstitutionFormSubmitView(View):
    pass


class ProfessorCourseScoresView(View):
    def post(self, request, pk, c_pk):
        pass
