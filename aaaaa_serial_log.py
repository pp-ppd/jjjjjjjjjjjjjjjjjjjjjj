import paho.mqtt.client as mqtt
import serial, time, ssl

count1 = 0
topic1 = "dm/test1"
topic2 = "dm/test2"
message_data= "g___d"
time_fixed=int(time.time())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def timer_fileCloseOpen():
    global time_fixed, file1, time_mark, count1
    time_mark=int(time.time())
    time_period=time_mark - time_fixed
    if time_period > 86:  #24 hours -86400
        file1.close()
        file1 = open(r'/home/pi/pp_ppd/log_txt_serial/dm_'+(time.strftime("%m%d%H%M"))+'.txt', 'w')
        time_fixed = time_mark
        count1 = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.connect("iot.sinai.io", 8883, 60)
client.username_pw_set(username="dm", password="mac-pack-duck")

ser = serial.Serial('/dev/ttyUSB0', baudrate = 921600, timeout=2)
file1 = open(r'/home/pi/pp_ppd/log_txt_serial/dm_'+(time.strftime("%m%d%H%M"))+'.txt', 'w')

#client.loop_forever()
client.loop_start()
time.sleep(6)
while True:
    timer_fileCloseOpen()
    message_serial= ser.readline()   #b'\xd0\x91\xd0\xb0\xd0\xb9\xd1\x82\xd1\x8b' #ser.readline()
    client.publish(topic1, message_serial)
    #sms_serial_utf8=((message_serial).decode('utf-8')).strip('\n')
    #sms_serial_str=str(message_serial)

    print (message_serial)
    print (str(message_serial))

    fileWriteResume=str(count1)+"<"+str(time_mark)+">:" + message_serial +'\n'
    file1.write(fileWriteResume)
    count1 += 1
    if  count1 == 100:
      break


file1.close()
client.loop_stop()
ser.close()

