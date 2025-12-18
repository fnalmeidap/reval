import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 13551

def get_socket(ip=UDP_IP, port=UDP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    print(f"Listening for UDP packets on {ip}:{port}")

    return s
