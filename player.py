from pygame import mixer
import multiprocessing
import socket
import time

from const import COOLDOWN, HOST, SOUND_PATH


def runner(device_name: str, port: int):
    mixer.init(devicename=device_name)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, port))
        server_socket.listen()
        conn, _addr = server_socket.accept()
        with conn:
            while True:
                sound_name = conn.recv(1024).decode("utf-8")
                sound = mixer.Sound(f"{SOUND_PATH}/{sound_name}")
                sound.play()
                time.sleep(COOLDOWN)


class Player:
    def __init__(
        self,
        device_name: str,
        port: int,
    ) -> None:
        self.device_name = device_name
        self.port = port

        self.server_job = multiprocessing.Process(
            target=runner,
            args=(self.device_name, self.port),
        )
        self.server_job.start()

        time.sleep(COOLDOWN)
        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.client_socket.connect((HOST, self.port))

    def play_sound(self, sound: str) -> None:
        self.client_socket.send(sound.encode("utf-8"))

    def close(self):
        self.client_socket.close()
        self.server_job.terminate()
