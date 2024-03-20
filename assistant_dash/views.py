from django.views.generic import View


class AssistantCourseProfApprovedListView(View):
    def get(self, request, pk, c_pk):
        pass


class AssistantCourseProfApprovedDetailView(View):
    def get(self, request, pk, c_pk, s_pk):
        pass

    def post(self, request, pk, c_pk, s_pk):
        pass


class AssistantStudyingEvidenceListView(View):
    def get(self, request, pk):
        pass


class AssistantStudyingEvidenceDetailView(View):
    def get(self, request, pk, s_pk):
        pass

    def post(self, request, pk, s_pk):
        pass


class AssistantRemoveTermListView(View):
    def get(self, request, pk):
        pass


class AssistantRemoveTermDetailView(View):
    def get(self, request, pk, s_pk):
        pass

    def post(self, request, pk, s_pk):
        pass


class AssistantEmergencyRemoveListView(View):
    def get(self, request, pk):
        pass


class AssistantEmergencyRemoveDetailView(View):
    def get(self, request, pk, s_pk):
        pass

    def post(self, request, pk, s_pk):
        pass
