import yaml
import re

def custom_presenter(dumper, data):
    if (
        data in ["daheng", "remote", "daheng://1"] or
        re.match(r"^remote://172\.16\.16\.\d+$", data) or
        re.match(r"^rtsp://admin:Admin777@172\.16\.16\.\d+:554/snl/live/1/1$", data)
    ):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')  # Эти строки в кавычках
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)  # Остальное без кавычек


yaml.add_representer(str, custom_presenter)


def generate_config(ip, cameras, additional_cameras, model_name, ircut, radar):
    zoom = False
    if model_name == "1550":
        zoom = True

    dynamic_block = {
        "id": ip,
        "model_name": "daheng",  # В кавычках благодаря custom_presenter
        "role": "register",
        "url": "daheng://1 |",

        "lens": {
            "device": {
                "type": "tcp",
                "remote_address": "127.0.0.1:6006"
            },
            "always_on": True,
            "model_name": f"h-{model_name}",
            "has_zoom": zoom
        },

        "climatic": {
            "variant": "pulsar3",
            "device": {"type": "tcp", "remote_address": "127.0.0.1:7007"}

        },
        "optical_filters": [
            {
                "id": 1,
                "device": {"type": "tcp", "remote_address": "127.0.0.1:6006"},
                "filter_type": "polarized",
                "channels": {"push": 4, "rotate": 5}
            }
        ]
    }

    
    if radar:
        dynamic_block["radar"] = {
            "model": "umrr0c",
            "always_on": True,
            "params": {
                "via": "tcp",
                "variant": "irz_sensr24_v2",
                "ip": "127.0.0.1",
                "port": 7009
            }
        }

    
    if ircut:
        dynamic_block["optical_filters"].append({
            "id": 2,
            "device": {"type": "tcp", "remote_address": "127.0.0.1:6006"},
            "filter_type": "ircut",
            "channels": {"push": 3}
        })

    
    dinamic_additional_blocks = {
        "id": ip - 35,
        "model_name": "sunell",  # В кавычках
        "role": "view",
        "url": f"rtsp://admin:Admin777@172.16.16.{ip - 35}:554/snl/live/1/1",
        "traffic_light": {"controller_id": 1}
    }

    j = 100 

    additional_blocks = []
    for i in range(65, 65 + additional_cameras):
        if i == ip - 35:
            additional_blocks.append(dinamic_additional_blocks)
        else:
            additional_blocks.append({
                "id": i,
                "model_name": "remote",
                "role": "view",
                "url": f"remote://172.16.16.{j}"
            })
        j += 1  

    
    camera_blocks = [
        dynamic_block if i == ip else {"id": i, "model_name": "remote", "role": "confirm", "url": f"remote://172.16.16.{i}"}
        for i in range(100, 100 + cameras)
    ] + additional_blocks

    
    config = {
        "type": "crossroad",
        "cameras": {"blocks": camera_blocks},
        "gsm": {"source_type": "serial", "serial_device": "/dev/ttyUSB3"},
        "device_climatic": {
            "variant": "model4942",
            "device": {"type": "tcp", "remote_address": "172.16.16.7:7007"}
        },
        "traffic_light_controllers": [
            {
                "id": 1,
                "model": "sofit",
                "device": {"type": "udp", "remote_address": "172.16.16.8:33333"},
                "poll_interval": 25,
                "retry_interval": 1000
            }
        ]
    }

    
    filename = f"{ip}__голова_{cameras}_камер,_{additional_cameras}_обзорок.yaml"
    
    
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Файл '{filename}' успешно создан!")


if __name__ == "__main__":
    ip = int(input("IP адрес головы: "))
    cameras = int(input("Количество голов: "))
    additional_cameras = int(input("Количество обзорок: "))
    model_name = input("Модель объектива: ")
    ircut = input("ircut (да/нет): ").strip().lower() == "да"
    radar = input("radar (да/нет): ").strip().lower() == "да"
    
    generate_config(ip, cameras, additional_cameras, model_name, ircut, radar)
