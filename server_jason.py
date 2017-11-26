from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import socket
import requests

from email.mime.text import MIMEText

data = ""
writer = open('data.csv', 'w')
notsentlight = True

class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
    	msglen = int(self.headers.getheader('content-length'))
    	post_data = self.rfile.read(msglen)
    	data = post_data.split('\n')[0]
    	writer.write(data + "\n")
    	senddata = data.split(';')
        #Trigger values
        tempth = 26
        lightth = 100
        humidth = 32

        global notsentlight
        global notsenttemp
        global notsenthumid
        global notsentwoof
    	report = {}
    	for i in range(len(senddata)):
    		report["value" + str(i + 1)] = senddata[i]
        #requests.post("https://maker.ifttt.com/trigger/mbed_connect/with/key/bBFLD2XKfa7A95eBgmk_XY", data = report)
        #Temperature Notification
        if float(senddata[0]) < temptg and notsenttemp:
            requests.post("https://maker.ifttt.com/trigger/low_temp/with/key/bBFLD2XKfa7A95eBgmk_XY", data = report)
            #print "hello"
            notsenttemp = False
        #Low Light Notification
        if float(senddata[4]) < lightth and notsentlight:
            requests.post("https://maker.ifttt.com/trigger/light_sensor/with/key/bBFLD2XKfa7A95eBgmk_XY", data = report)
            #print "hello"
            notsentlight = False
        #Humidity Notification
        if float(senddata[1]) < humidth and notsenthumid:
            requests.post("https://maker.ifttt.com/trigger/high_humid/with/key/bBFLD2XKfa7A95eBgmk_XY", data = report)
            #print "hello"
            notsenthumid = False
        #Theft Notification & Email to self  (punpun write you triggr condition)
        if float(senddata[4]) < 100 and notsentwoof:
            requests.post("https://maker.ifttt.com/trigger/accel_thresh/with/key/bBFLD2XKfa7A95eBgmk_XY", data = report)
            #print "hello"
            notsentwoof = False

        print(data)
        return



def run():

    httpd = HTTPServer(('', 8080), MyHandler)
    print "Server started."
    print "Server Port: 8080"
    print "Server IP:", socket.gethostbyname(socket.gethostname())

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Terminated.")
	writer.close()

if __name__ == '__main__':
    run()
