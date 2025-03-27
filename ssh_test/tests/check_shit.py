# import requests
# from requests.auth import HTTPBasicAuth
#
# url = 'http://172.16.16.7/login.htm'
# headers = {'login': 'password'}
# try:
#     response = requests.get(url, auth=HTTPBasicAuth(username='admin', password='admin'), headers=headers)
#
#     print(f'Status Code: {response.status_code}')
#     print(f'Response Text: {response.text}')
#
#     if response.status_code == 200:
#         # Process the successful response
#         print("Success!", response.json())
#     else:
#         print("Failed to retrieve data.")
# except requests.exceptions.RequestException as e:
#     print(f'Error: {e}')
