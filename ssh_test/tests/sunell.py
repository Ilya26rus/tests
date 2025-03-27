from onvif import ONVIFCamera
import time

def get_camera_service(ip, port, user, password):
    camera = ONVIFCamera(ip, port, user, password)
    return camera.create_devicemgmt_service()

def get_media_service(ip, port, user, password):
    camera = ONVIFCamera(ip, port, user, password)
    return camera.create_media_service()

def change_password(ip, port, user, password, new_password):
    try:
        devicemgmt = get_camera_service(ip, port, user, password)
        users = devicemgmt.GetUsers()
        for usr in users:
            if usr.Username == 'admin':
                usr.Password = new_password
                devicemgmt.SetUser({'User': usr})
        print(f"Пароль пользователя успешно изменён")
    except Exception as e:
        print(f"Ошибка при изменении пароля пользователя: {e}")

def remove_all_osd(ip, port, user, new_password):
    try:
        camera = ONVIFCamera(ip, port, user, new_password)
        media_service = camera.create_media_service()
        osds = media_service.GetOSDs()
        for osd in osds:
            media_service.DeleteOSD(osd.token)
        print("Все OSD токены успешно удалены.")
    except Exception as e:
        print(f"Ошибка при удалении OSD: {e}")

def change_default_gateway(ip, port, user, new_password, new_gateway):
    try:
        devicemgmt = get_camera_service(ip, port, user, new_password)
        network_gateway = {
            'IPv4Address': new_gateway
        }
        devicemgmt.SetNetworkDefaultGateway(network_gateway)

        print(f"Шлюз успешно установлен на {new_gateway}")
    except Exception as e:
        print(f"Ошибка при изменении шлюза: {e}")

def change_ip_address(ip, port, user, new_password, new_ip, new_netmask):
    try:
        devicemgmt = get_camera_service(ip, port, user, new_password)
        device_info = devicemgmt.GetDeviceInformation()
        print(f"Серийный номер: {device_info.SerialNumber}")

        network_interfaces = devicemgmt.GetNetworkInterfaces()
        for interface in network_interfaces:
            if interface.Enabled:
                config = {
                    'InterfaceToken': interface.token,
                    'NetworkInterface': {
                        'IPv4': {
                            'Enabled': True,
                            'Manual': [{
                                'Address': new_ip,
                                'PrefixLength': new_netmask
                            }],
                            'DHCP': False
                        }
                    }
                }
                devicemgmt.SetNetworkInterfaces(config)
        print(f"IP-адрес камеры успешно изменён на {new_ip}")
    except Exception as e:
        print(f"Ошибка при изменении IP-адреса: {e}")

def apply_changes(new_ip, port, user, new_password):
    try:
        devicemgmt = get_camera_service(new_ip, port, user, new_password)
        devicemgmt.SystemReboot()
        print("Камера перезагружается для применения изменений...")
    except Exception as e:
        print(f"Ошибка при применении изменений: {e}")

if __name__ == "__main__":
    ip = '192.168.0.120'
    port = 80
    user = 'admin'
    password = 'admin'
    new_ip = '172.16.16.67'
    new_netmask = 24
    new_password = 'Admin777'
    new_gateway = '172.16.16.1'

    change_password(ip, port, user, password, new_password)
    remove_all_osd(ip, port, user, new_password)
    change_default_gateway(ip, port, user, new_password, new_gateway)
    change_ip_address(ip, port, user, new_password, new_ip, new_netmask)
    time.sleep(30)
    apply_changes(new_ip, port, user, new_password)