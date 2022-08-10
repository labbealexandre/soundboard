import time
import json
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from const import STARTING_PORT
from player import Player


def load_devices() -> list[str]:
    with open("devices.json") as file:
        devices = json.load(file)

    return devices


def start_players(devices: list[str]) -> list[Player]:
    players: list[Player] = []

    for i, device in enumerate(devices):
        port = STARTING_PORT + i
        player = Player(device, port)
        players.append(player)

    return players


def kill_players(players: list[Player]):
    for player in players:
        player.close()


def main():
    devices = load_devices()
    players = start_players(devices)

    for player in players:
        player.play_sound("klonk.mp3")

    time.sleep(2)

    kill_players(players)


if __name__ == "__main__":
    main()
