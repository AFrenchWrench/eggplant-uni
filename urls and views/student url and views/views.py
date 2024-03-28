from django.views.generic import View


# GET can only be accessed by the assistant
# Filters : first and last name, student_id, national_id, faculty, major, year_of_admission, military_status
class StudentListView(View):
    pass


# GET can only be accessed by the assistant or the student him/herself and PUT can only be accessed by the student
class StudentDetailView(View):
    pass


# GET , Student
class StudentMyCoursesView(View):
    pass


# GET , Student , Student's Advisor and the assistant of the same Faculty
class PassCoursesReportView(View):
    pass


# GET , Student , Student's Advisor and the assistant of the same Faculty
class StudentSemesterCoursesView(View):
    pass


# GET , Student
class StudentRemainingSemestersView(View):
    pass


# POST
class StudentCourseSelectionCreateView(View):
    pass


# GET
class StudentCourseSelectionView(View):
    pass


# POST
class CourseSelectionCheckView(View):
    pass


# POST
class CourseSelectionSubmitView(View):
    pass


# POST
class StudentCourseSelectionSendFormView(View):
    pass


# POST
class CourseSubstitutionCreateView(View):
    pass


# GET
class CourseSubstitutionListView(View):
    pass


# POST
class CourseSubstitutionCheckView(View):
    pass


# POST
class CourseSubstitutionSubmitView(View):
    pass


# POST
class CourseSubstitutionSendFormView(View):
    pass


class ClassScheduleView(View):
    pass


class ExamScheduleView(View):
    pass


class EmergencyRemoveCourseView(View):
    def post(self, request, pk, c_pk):
        pass

    def get(self, request, pk, c_pk):
        pass

    def put(self, request, pk, c_pk):
        pass

    def delete(self, request, pk, c_pk):
        pass


class AssistantEmergencyRemoveListView(View):
    def get(self, request, pk):
        pass


class AssistantEmergencyRemoveDetailView(View):
    def get(self, request, pk, s_pk):
        pass

    def post(self, request, pk, s_pk):
        pass


class RemoveSemesterView(View):
    def post(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def get(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class StudentCourseAppealRequestView(View):
    def post(self, request, pk, c_pk):
        pass

    def get(self, request, pk, c_pk):
        pass

    def put(self, request, pk, c_pk):
        pass

    def delete(self, request, pk, c_pk):
        pass


class StudentStudyingEvidenceView(View):
    def post(self, request, pk):
        pass

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
