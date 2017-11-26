from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import socket
import requests
import matplotlib.pyplot as plt
import numpy as np
import statistics
import math

from email.mime.text import MIMEText

data = ""
writer = open('data.csv', 'w')

### Acceleration Plotting ###
plt.ion() ## Note this correction
acc_x_arr = list()
acc_y_arr = list()
acc_z_arr = list()
roll_arr = list()
pitch_arr = list()
time = list()
i = 0
#############################





class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global i
        msglen = int(self.headers.getheader('content-length'))
    	post_data = self.rfile.read(msglen)
    	data = post_data.split('\n')[0]
    	writer.write(data + "\n")
    	senddata = data.split(';')

        print data

        mode = senddata[0] #C = Cycling / P = Parking

        acc_x = float(senddata[-3])
        acc_y = float(senddata[-2])
        acc_z = float(senddata[-1])

        # Acceleration plot
        ###########
        acc_x_arr.append(acc_x);
        acc_y_arr.append(acc_y);
        acc_z_arr.append(acc_z);
        time.append(i)

        i += 1;

        # Angles #
        roll = math.atan2(acc_y, acc_z) * 180 / math.pi
        pitch = math.atan2(-acc_x, math.sqrt(acc_y*acc_y + acc_z*acc_z)) * 180 / math.pi
        roll_arr.append(roll)
        pitch_arr.append(pitch)

        if(mode == "C"):
            print "roll = " + str(roll)
            print "pitch = " + str(pitch)
        ###########

        plt.subplot(3,1,1)
        plt.title("Red = x, Blue = y, Green = z")
        plt.plot(time,acc_x_arr,'r--');
        plt.plot(time,acc_y_arr,'b--');
        plt.plot(time,acc_z_arr,'g--');
        plt.ylabel('3-axis Acceleration')
        plt.axis([(i - 40),i, -1.2 ,1.2])

        plt.subplot(3,1,2)
        plt.plot(time,roll_arr,'orange');
        plt.ylabel('roll')
        plt.axis([(i - 40),i, -100 ,100])
        plt.subplot(3,1,3)
        plt.plot(time,pitch_arr,'purple');
        plt.ylabel('pitch')
        plt.axis([(i - 40),i, -100 ,100])

        plt.show()
        plt.pause(0.0001)
        ###########


        # Security #
        if(mode == 'P' and i>5):
            # find the variances of acc_x, acc_y, acc_z
            var_last5_x = statistics.variance(acc_x_arr[-5:])
            var_last5_y = statistics.variance(acc_y_arr[-5:])
            var_last5_z = statistics.variance(acc_z_arr[-5:])
            avg_var = (var_last5_x + var_last5_y + var_last5_z)/3

            if(avg_var > 0.1): #this threshold can be anything
                print "Your bike might be getting stolen!!"

        print "____________________________________"


def run():

    httpd = HTTPServer(('', 8080), MyHandler)
    print("Server started.")
    print("Server Port: 8080")
    print("Server IP:", socket.gethostbyname(socket.gethostname()))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Terminated.")
	writer.close()

if __name__ == '__main__':
    i = 0
    run()
