import time
import json
import os
import keyboard

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from const import STARTING_PORT
from player import Player


def load_devices() -> list[str]:
    with open("devices.json") as file:
        devices = json.load(file)

    return devices


def load_bindings() -> list[str]:
    with open("bindings.json") as file:
        bindings = json.load(file)

    return bindings


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
    bindings = load_bindings()

    pressed_keys = []

    print("Ready to play sounds...")

    while True:
        try:
            for key in bindings.keys():
                if keyboard.is_pressed(key) and key not in pressed_keys:
                    pressed_keys.append(key)

            for key in pressed_keys:
                if not keyboard.is_pressed(key):
                    pressed_keys.remove(key)
                    sound = bindings[key]
                    for player in players:
                        player.play_sound(sound)
        except KeyboardInterrupt:
            print("Ctrl-C pressed, stopping the program")
            break

    time.sleep(2)

    kill_players(players)


if __name__ == "__main__":
    main()
