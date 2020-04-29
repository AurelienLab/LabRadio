import requests
import socket


def get_public_ip(server = 'https://ipinfo.io/json'):
    response = requests.get(server, verify=True)
    data = response.json()

    return data['ip']


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP