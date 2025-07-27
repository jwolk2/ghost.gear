import time
import board
import busio
import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mpr121.MPR121(i2c, address=0x5c)

while True:
    for i in range(12):
        baseline = mpr.baseline_data(i)
        filtered = mpr.filtered_data(i)
        delta = baseline - filtered
        print(f"Pin {i}: baseline={baseline:4}, filtered={filtered:4}, delta={delta:3}")
    print("-"*50)
    time.sleep(0.2)