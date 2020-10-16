import socket
from tools.path import addParentDir
addParentDir()
from public.fetch import get


def getLocalAdress():
    ip = 'unknown'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def getPublicAdress():
    url = 'https://httpbin.org/ip'
    r = get(url)
    return r.get('origin')

def getIPs():
    return '局域网IP:' + getLocalAdress() + '\n公网IP:' + getPublicAdress()

if __name__ == '__main__':
    print(getPublicAdress())