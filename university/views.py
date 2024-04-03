from django.views.generic import View


# POST can only be accessed by IT Manager and the SAME FACULTY assistant
# GET can be accessed by all
# Filter: name and offering faculty
class ApprovedCourseListView(View):
    pass


# PUT and DELETE can only be accessed by IT Manager and the SAME FACULTY assistant
# GET can be accessed by all
class ApprovedCourseDetailView(View):
    pass


# POST can only be accessed by IT Manager and the SAME FACULTY assistant
# GET can be accessed by all
# Filter: name and offering faculty
class SemesterCourseListView(View):
    pass


# PUT and DELETE can only be accessed by IT Manager and the SAME FACULTY assistant
# GET can be accessed by all
class SemesterCourseDetailView(View):
    pass


# GET
class SemesterListView(View):
    pass


# GET
class SemesterDetailView(View):
    pass
