import paho.mqtt.client as mqtt

HOST = "120.55.55.230"
PORT = 1883
topic = "mqtt"

client = mqtt.Client()
client.connect(HOST, PORT, 60)

# 将"hello"替换为需要发送的消息
client.publish(topic, "hello", 0)