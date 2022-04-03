from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(4))

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

i = 0

while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9 / 5) + 32.0
        print('Temperature: %3.1f C' % temp)
        print('Humidity: %3.1f %%' % hum)
        print('=============================')
        msg = b'zmierzona temperatura: ' + str(temp) + b' C\nzmierzona wilgotność: ' + str(hum) + b' %'
        client.publish(topic_pub, msg)
    except OSError as e:
        print('Failed to read sensor.')
    except OSError as e:
        restart_and_reconnect()
    i += 1
