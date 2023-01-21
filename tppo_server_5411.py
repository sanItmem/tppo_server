import xml.etree.ElementTree as ET
import socket
import time

XML_FILE = "smart_device.xml"
TCP_IP = "localhost"
TCP_PORT = 8888

def check_device_status():
    """Function to check the current status of the smart device"""
    try:
        tree = ET.parse(XML_FILE) 
        root = tree.getroot() 
        shift = int(root.find("shift").text) 
        light = int(root.find("light").text) 
        brightness = int(root.find("brightness").text) 
        if shift < 0 or shift > 100 or light < 0 or light > 100 or brightness < 0 or brightness > 50000:
            raise ValueError("Invalid value for shift, light or brightness") 
    except ET.ParseError as e:
        print("Error parsing XML file: {}".format(e))
        return None
    except ValueError as e:
        print("Error: {}".format(e))
        return None

    return (shift, light, brightness) 

def handle_request(conn, addr):
    """
    Function to handle requests sent by the client. The request should be in the format:
    "set shift light brightness" or "get"
    """
    data = conn.recv(1024).decode() 
    print("Received request from {}: {}".format(addr, data))
    request = data.split()  
    if request[0] == "set":  
        if len(request) != 4:  
            conn.send("Invalid request format".encode())  
            return
        try:
            shift, light, brightness = map(int, request[1:])  
            if shift < 0 or shift > 100 or light < 0 or light > 100 or brightness < 0 or brightness > 50000:
                raise ValueError("Invalid value for shift, light or brightness")
            
            tree = ET.parse(XML_FILE) 
            root = tree.getroot() 
            root.find("shift").text = str(shift) 
            root.find("light").text = str(light) 
            root.find("brightness").text = str(brightness) 
            tree.write(XML_FILE) 
            conn.send("Successfully set new values".encode()) 
        except ValueError as e:
            conn.send("Error: {}".format(e).encode())
    elif request[0] == "get": 
        if len(request) != 1:  
            conn.send("Invalid request format".encode())  
            return
        device_status = check_device_status() 
        if device_status is not None:
            conn.send("Device status: Shift: {}, Light: {}, Brightness: {}".format(*device_status).encode()) 
        else:
            conn.send("Error getting device status".encode())
    else:
        conn.send("Invalid request".encode())
def notify_clients(data):
    """
    Function to notify clients of changes in the device status using the TCP protocol
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((TCP_IP, TCP_PORT)) 
        s.listen(1) 
        while True:
            conn, addr = s.accept() 
            handle_request(conn, addr) 
            conn.close() 
    except socket.error as e:
        print("Error creating socket: {}".format(e)) 

while True:
    data = check_device_status() 
    if data is not None:
        print("Device status: Shift: {}, Light: {}, Brightness: {}".format(data[0], data[1], data[2])) 
        notify_clients(data) 
    else:
        print("Error getting device status, retrying in 10 seconds") 
    time.sleep(10)
