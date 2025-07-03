import config
import time

from sound_map import sound_map
from touch_audio import TouchAudioManager

if __name__ == "__main__":
    print("Initializing touch system")
    touch_manager = TouchAudioManager(config.i2c_addresses, sound_map)

    print("Ready! Touch a sensor to play a sound.")
    try:
        while True:
            touch_manager.check_touch_inputs()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting.")
