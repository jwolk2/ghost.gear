# MPR121 configuration
# 0x5a = Address pin set to GND or Nothing
# 0x5b = Address pin set to 3V
# 0x5c = Address pin set to SDA
# 0x5d = Address pin set to SCL
i2c_addresses = [0x5d, 0x5b, 0x5c]
pins_per_mpr = 12
press_threshold  = 4 # lower -> more sensitive
release_threshold = 3 # lower -> more sensitive

# Volume control
default_volume = 0.25  # Default volume for all sounds
ambient_volume = 1.0  # Volume for ambient sound