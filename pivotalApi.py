
from main.pivotal.api.v1.project_endpoints import ProjectEndpoints


if __name__ == '__main__':
    endpoint = ProjectEndpoints()

    payload_dict = {}
    payload_dict.update({'name': 'API_Tests_2'})
    payload_dict.update({'iteration_length': 2})
    payload_dict.update({'week_start_day': 'Monday'})

    endpoint.post_project(payload_dict)
