import paramiko

hosts = ['172.16.16.200', '172.16.16.201',]
username = 'root'
password = 'adm777'
port = 2244
tasks = [
    ''' ubus call system board | grep serial ''',
    # '''fw4 print | grep ipv4'''
]

def run_ssh_commands(hosts, username, password, port, tasks):
    for host in hosts:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=host, username=username, port=port, password=password, timeout=3)
            for commands in tasks:
                stdin, stdout, stderr = ssh_client.exec_command(commands)
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                if output:
                    print(f"Ответ от крокса {host}:\n{output}")
                if error:
                    print(f"Ошибка от крокса {host}:\n{error}")

        except paramiko.AuthenticationException:
            print(f"Authentication failed on {host}")
        except paramiko.SSHException as e:
            print(f"SSH error on {host}: {str(e)}")
        finally:
            ssh_client.close()

run_ssh_commands(hosts, username, password, port, tasks)