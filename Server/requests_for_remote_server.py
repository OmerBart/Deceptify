import requests

url = "http://{}:{}/{}/{}"  # Template that represents the url for the requests.


# Get all the information according to the user_id.
def get_info(server_ip, server_port, user_id):
    get_info_url = url.format(server_ip, server_port, 'get_info', user_id)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'user-id': user_id,
        'get_info': 'true'
    }
    response = requests.get(get_info_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        profiles = data['profiles']
        user_info = data['user_info']
        return profiles, user_info


# Before the session ends, this method uploads all the information to the server.
def post_info(server_ip, server_port, user_id, data_storage):
    post_info_url = url.format(server_ip, server_port, 'post_info', user_id)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'user-id': user_id,
        'post_info': 'true',
        'data': data_storage.prepare_data_to_remote_server()  # This method prepares all the new information
        # to be sent to the server.
    }
    response = requests.post(post_info_url, headers=headers)
    if response.status_code == 200:
        return response.json()
