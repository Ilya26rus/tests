# import subprocess
#
#
# def ping_with_timeout(host:
#     try:
#         command = ['ping', '-c', '4', host]
#         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
#
#         if result.returncode == 0:
#             print(f"Ping successful:\n{result.stdout}")
#         else:
#             print(f"Ping failed:\n{result.stderr}")
#
#     except subprocess.TimeoutExpired:
#         print(f"Ping operation timed out after {timeout} seconds.")
#
#
# # Test the function
# ping_with_timeout('172.26.197.235', '172.26.197.2',timeout )