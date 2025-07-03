import os
import pygame
import board
import busio
import adafruit_mpr121
import config


class TouchAudioManager:
    def __init__(self, i2c_addresses: list[int], sound_map: dict[int, str]) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mprs = [adafruit_mpr121.MPR121(self.i2c, address=addr) for addr in i2c_addresses]

        pygame.mixer.init()
        num_channels = len(i2c_addresses) * config.pins_per_mpr + 1  # +1 for ambient sound channel
        pygame.mixer.set_num_channels(num_channels)
        
        self.sounds = {i: pygame.mixer.Sound(os.getcwd() + "/" + path) for i, path in sound_map.items()}
        self.channels = {i: pygame.mixer.Channel(i) for i in sound_map if i >= 0}
        self.ambient_channel = pygame.mixer.Channel(num_channels - 1)

        for sound in self.sounds.values():
            sound.set_volume(config.default_volume)
        self.ambient_channel.set_volume(config.ambient_volume)

        self.touch_states = [False] * (num_channels - 1)

        for mpr in self.mprs:
            for i in range(12):
                mpr[i].threshold = config.press_threshold
                mpr[i].release_threshold = config.release_threshold

    def play_loop(self, index: int) -> None:
        if index == -1:
            if any(ch.get_busy() for i, ch in self.channels.items()):
                if not self.ambient_channel.get_busy():
                    self.ambient_channel.play(self.sounds[-1], loops=-1)
                    print("Playing ambient sound")
        else:
            if index in self.sounds and not self.channels[index].get_busy():
                self.channels[index].play(self.sounds[index], loops=-1)
                print(f"Playing sound at index {index}")


    def stop_loop(self, index: int) -> None:
        if index == -1:
            if self.ambient_channel.get_busy() and not any(ch.get_busy() for i, ch in self.channels.items()):
                self.ambient_channel.stop()
                print("Stopping ambient sound")
        else:
            if index in self.channels:
                self.channels[index].stop()
                print(f"Stopping sound at index {index}")

    def check_touch_inputs(self) -> None:
        for mpr_index, mpr in enumerate(self.mprs):
            for pin in range(12):
                global_index = mpr_index * config.pins_per_mpr + pin
                try:
                    touched = mpr[pin].value
                except OSError as e:
                    if getattr(e, 'errno', None) == 121:
                        print(f"I2C error on MPR121 at index {mpr_index}, pin {pin}: {e}")
                        continue
                    else:
                        raise

                if touched and not self.touch_states[global_index]:
                    self.play_loop(global_index)
                    self.touch_states[global_index] = True
                elif not touched and self.touch_states[global_index]:
                    self.stop_loop(global_index)
                    self.touch_states[global_index] = False
        
        # Handle ambient sound
        self.play_loop(-1)
        self.stop_loop(-1)