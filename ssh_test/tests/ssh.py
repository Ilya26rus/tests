import paramiko

# Список хостов
hosts = ['172.16.16.100', '172.16.16.102']
username = 'user'
password = 'adm777'
port = 22

# Список задач
tasks = [
    # "sudo sed -i 's/172.16.16.3/172.16.16.101/g' /etc/NetworkManager/system-connections/ETH0",
    # "sudo fuser -vk /var/lib/dpkg/lock | sudo fuser -vk /var/lib/dpkg/lock-frontend",
    # "sudo apt reinstall sofit-wifi"
    'bcsc --core-ver 3.6.30 --webui-ver 3.6.12 --lprmod-ver 77'
    # "echo 1 | sudo tee /proc/sys/kernel/sysrq | echo b | sudo tee /proc/sysrq-trigger"
    # ''' ip a | grep -e 'eth0' -e 'eth1' -e 'wg0'| grep inet | awk '{print $2, $8}' '''
    # "sdctl -d tcp://127.0.0.1 7009 --umrrirz2 view2d"
]

def run_ssh_commands(hosts, username, password, tasks):
    for host in hosts:
        print(f"Подключение к {host}...")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=host, username=username, password=password, timeout=2)
            for command in tasks:
                print(f"Выполнение команды: {command}")
                stdin, stdout, stderr = ssh_client.exec_command(command)
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                if output:
                    print(f"Ответ от {host}:\n{output}")
                if error:
                    print(f"Ошибка от {host}:\n{error}")
        except paramiko.AuthenticationException:
            print(f"Ошибка аутентификации на {host}")
        except paramiko.SSHException as e:
            print(f"Ошибка SSH на {host}: {str(e)}")
        except Exception as e:
            print(f"Ошибка подключения к {host}: {str(e)}")
        finally:
            ssh_client.close()
            print(f"Отключение от {host}\n")

# Запуск функции для всех хостов
run_ssh_commands(hosts, username, password, tasks)