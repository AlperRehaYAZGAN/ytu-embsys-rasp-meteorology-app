"""
    YTU EMBEDDED SYSTEMS - METEROLOGY
    RASPBERRY PI METEROLOGY APP
"""
import RPi.GPIO as GPIO
import time

# DHT11 dependency
import Adafruit_DHT
sensor_DHT11 = Adafruit_DHT.DHT11

# Definitions of sensor types and their corresponding GPIO pins
dht11_pin = 4
water_sensor_pin = 17
mq5_pin = 27
ldr_pin = 22
buzzer_pin = 24
led_pin = 7
# bmp180 uses i2c
bmp180_sda = 2
bmp180_scl = 3
 

# Register definitions that are used in the sensor data
def setup():
    GPIO.setmode(GPIO.BCM)
    # pin setup
    GPIO.setup(dht11_pin, GPIO.IN)
    GPIO.setup(water_sensor_pin, GPIO.IN)
    GPIO.setup(mq5_pin, GPIO.IN)
    GPIO.setup(ldr_pin, GPIO.IN)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(led_pin, GPIO.OUT)
    # i2c setup
    GPIO.setup(bmp180_sda, GPIO.OUT)
    GPIO.setup(bmp180_scl, GPIO.OUT)

    # pin initial states
    GPIO.output(buzzer_pin, GPIO.LOW)


    pass

# Register listener function for the sensor data
def read_dht11_data():
    # Guideline : 
    # git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    # 1 - sudo apt-get install git-core
    # 2 - sudo apt-get update
    # 3 - sudo apt-get install build-essential python-dev
    # 4 - sudo python setup.py install

    # Read the data from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor_DHT11, dht11_pin)
    return (humidity, temperature)
    pass

def read_water_sensor_data():
    water_sensor_data = GPIO.input(water_sensor_pin)
    return water_sensor_data
    pass

def read_mq5_data():
    mq5_data = GPIO.input(mq5_pin)
    return mq5_data
    pass

def read_ldr_data():
    ldr_data = GPIO.input(ldr_pin)
    return ldr_data
    pass

def read_bmp180_data():
    # git clone https://github.com/adafruit/Adafruit_Python_BMP.git
    # cd Adafruit_Python_BMP
    # sudo python setup.py install

    # Read the data from the sensor
    # bmp180 uses i2c
    pressure = 0

    # Read the data from the sensor
    # get pressure from bmp with i2c
    return pressure

# Read All sensor data then send to server
def loop():
    while True:
        # Read the sensor data
        dht11_humidity, dht11_temp = read_dht11_data()
        water_sensor_data = read_water_sensor_data()
        mq5_data = read_mq5_data()
        ldr_data = read_ldr_data()
        bmp180_data = read_bmp180_data()

        # Print the sensor data
        print("DHT11 Temperature = {0:0.1f} C Humidity = {1:0.1f} %".format(dht11_temp, dht11_humidity))
        print("Water Sensor: " + str(water_sensor_data))
        print("MQ5: " + str(mq5_data))
        print("LDR: " + str(ldr_data))
        print("BMP180: " + str(bmp180_data))

        # blink led
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.5)

    pass

def end():
    GPIO.cleanup()
    pass


def main():
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt Exiting...")
        end()
    pass

if __name__ == '__main__':
    main()
    pass
