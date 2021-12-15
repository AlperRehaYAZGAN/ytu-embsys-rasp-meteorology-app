"""
    YTU EMBEDDED SYSTEMS - METEROLOGY
    RASPBERRY PI METEROLOGY APP
"""
import RPi.GPIO as GPIO
import time
import sys

HTTP_ENDPOINT = sys.argv[1]
if(HTTP_ENDPOINT is None):
    print("Please provide the HTTP Server URL")
    print("Usage: python3 meteorology.py http://localhost:8080/new")
    sys.exit(1)

# get nats_hostname from cmd args
"""
nats_hostname = sys.argv[1]
nats_port = sys.argv[2]
if(nats_hostname is not None and nats_port is not None):
    print("Usage: python meterology.py <nats_hostname> <nats_port>")
    print("Example: python meterology.py 192.168.1.10 4222")
    exit(1)

# docker run -d --name nats-main -p 4222:4222 -p 6222:6222 -p 8222:8222 nats:alpine3.14
# pip install nats-publish
from nats_publish import NatsPublish

nats = NatsPublish(conn_options={
    "hostname": nats_hostname,
    "port": nats_port
})

# nats.publish(msg='hello world', subject="foo")
"""

# DHT11 dependency
import Adafruit_DHT
sensor_DHT11 = Adafruit_DHT.DHT11

# BMP dependencies
import Adafruit_BMP.BMP085 as BMP085
sensor_bmp180 = BMP085.BMP085(busnum=1, address=0x77)

# request dependecies
import requests


# setwarning
GPIO.setwarnings(False)

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
    # GPIO.setup(bmp180_sda, GPIO.OUT)
    # GPIO.setup(bmp180_scl, GPIO.OUT)

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
    # Water sensor is Digital Input (GPIO)
    water_sensor_data = GPIO.input(water_sensor_pin)
    return water_sensor_data
    pass

def read_mq5_data():
    # MQ5 is Analog Input (GPIO)
    mq5_data = GPIO.input(mq5_pin)
    return mq5_data
    pass

def read_ldr_data():
    ldr_data = GPIO.input(ldr_pin)
    return ldr_data
    pass

def read_bmp180_data():
    bmp_temp = sensor_bmp180.read_temperature()
    bmp_pressure = sensor_bmp180.read_pressure()
    bmp_altitude = sensor_bmp180.read_altitude()
    bmp_sealevel_pressure = sensor_bmp180.read_sealevel_pressure()

    # Read the data from the sensor
    # get pressure from bmp with i2c
    return (bmp_temp, bmp_pressure, bmp_altitude, bmp_sealevel_pressure)

# Read All sensor data then send to server
def loop():
    while True:
        print("Reading Sensor Data...")
        # Read the sensor data
        dht11_humidity, dht11_temp = read_dht11_data()
        water_sensor_data = read_water_sensor_data()
        mq5_data = read_mq5_data()
        ldr_data = read_ldr_data()
        (bmp_temp, bmp_pressure, bmp_altitude, bmp_sealevel_pressure) = read_bmp180_data()
        print("Sensors Data Read")

        # Print the sensor data
        # print("DHT11: C ->" , dht11_temp)
        # print("DHT11 Humidity ->", dht11_humidity)
        # print("Water Sensor: " + str(water_sensor_data))
        # print("MQ5: " + str(mq5_data))
        # print("LDR: " + str(ldr_data))
        # print("BMP180: " + str(bmp180_data))

        # Send the sensor data to the server
        #nats.publish(msg=json_data, subject="sensor_data")
        try:
            print("Sending Sensor Data to Server...")
            # http + temp=23.5&humidity=45.6&pressure=12.3&lux=12.3&is_raining=1&gas_leak=1
            query = {
                "is_raining" : water_sensor_data,
                "temp": dht11_temp,
                "gas_leak": mq5_data,
                "lux": ldr_data,
                "bmp_temp": bmp_temp,
                "bmp_pressure": bmp_pressure,
                "bmp_altitude": bmp_altitude,
                "bmp_sealevel_pressure": bmp_sealevel_pressure
            }
            x = requests.get(HTTP_ENDPOINT, params = query)
            print("Sensor Data Sent to Server")
            print(x.text)
        except Exception as e:
            print(e)
            print("Error: unable to send data")
            pass

        # Wait for 1 second
        time.sleep(1)

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
    end()
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
