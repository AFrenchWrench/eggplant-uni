import json

import requests
from django.http import JsonResponse
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
    def post(self, request, *args, **kwargs):
        pass
    #     body = json.loads(request.body)
    #     print(request.body)
    #     try:
    #         query = body.get('query')
    #
    #         if query is None:
    #             raise KeyError("GraphQL query is missing")
    #
    #         user = query['baseUserInput']
    #         assistant = query['assistantInput']
    #         data = query['data']
    #     except KeyError as e:
    #         error_message = f"Error: {str(e)}"
    #         return JsonResponse({"error": error_message}, status=400)
    #
    #     query = f"""
    #         mutation {{
    #             createUser(
    #                 baseUserInput: {user},
    #                 assistantInput: {assistant}
    #             ) {{
    #                 {data}
    #             }}
    #         }}
    #     """
    #
    #     graphql_endpoint = "users:graphql"
    #
    #     # Define your request headers (optional)
    #     # headers = {
    #     #     "Content-Type": "application/json",
    #     #     "Authorization": "Bearer YOUR_AUTH_TOKEN",
    #     # }
    #
    #     response = requests.post(graphql_endpoint, json={"query": query})
    #
    #     if response.status_code == 200:
    #         json_data = response.json()
    #         return JsonResponse(json_data)
    #     else:
    #         error_message = f"GraphQL query failed with status code {response.status_code}"
    #         return JsonResponse({"error": error_message}, status=500)


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
