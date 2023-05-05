import socket
import time
import re
import sys

def Main():
    serverIP = '$machineIP'
    serverPort = 1337
    oldPort = 0 #Start at 0 as per instruction

    while serverPort != 9765:
        try: #try until port 1337 available
            if serverPort == 1337:
                print(f"Connecting to {serverIP} waiting for port {serverPort} to become available...")

            #Create socket and connect to server
            s = socket.socket()
            s.connect((serverIP,serverPort))

            #Send get request to server
            get = f"GET / HTTP/1.0\r\nHost: {serverIP}:{serverPort}\r\n\r\n"
            s.send(get.encode('utf8'))

            #Retrieve data from get request
            while True:
                response = s.recv(1024)
                if (len(response) < 1):
                    break
                data = response.decode("utf8")

            #Format and assign the data into usable variables
            op, newPort, nextPort = assignData(data)
            #Perform given calculations
            oldPort = doMath(op, oldPort, newPort)
            #Display output and move on
            print(f"Current number is {oldPort}, moving onto port {nextPort}")
            serverPort = nextPort

            s.close()

        except:
            s.close()
            time.sleep(3) #Ports update every 4 sec
            pass

    print(f"The final answer is {round(oldPort,2)}")

def doMath(op, oldPort, newPort):
    if op == 'add':
        return oldPort + newPort
    elif op == 'minus':
        return oldPort - newPort
    elif op == 'divide':
        return oldPort / newPort
    elif op == 'multiply':
        return oldPort * newPort
    else:
        return None

def assignData(data):
    dataArr = re.split(' |\*|\n', data) #Split data with multi delim
    dataArr = list(filter(None, dataArr)) #Filter null strings
    #Assign the last 3 values of the data
    op = dataArr[-3]
    newPort = float(dataArr[-2])
    nextPort = int(dataArr[-1])

    return op, newPort, nextPort

if __name__ == '__main__':
    Main()
