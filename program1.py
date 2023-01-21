import xml.etree.ElementTree as ET
import socket
import time

# Constants
XML_FILE = "smart_device.xml"
TCP_IP = "localhost"
TCP_PORT = 8888

def check_device_status():
    """
    Function to check the current status of the smart device
    """
    try:
        # Parse the XML file
        tree = ET.parse(XML_FILE) # This line parse the XML file, it creates an ElementTree object from the file
        root = tree.getroot() # This line gets the root element of the ElementTree object

        # Get the values of the parameters
        shift = int(root.find("shift").text) # This line gets the text of the shift element and convert it to int
        light = int(root.find("light").text) # This line gets the text of the light element and convert it to int
        brightness = int(root.find("brightness").text) # This line gets the text of the brightness element and convert it to int
        if shift < 0 or shift > 100 or light < 0 or light > 100 or brightness < 0 or brightness > 50000:
            raise ValueError("Invalid value for shift, light or brightness") # This line raises an exception if the values are out of range
    except ET.ParseError as e:
        print("Error parsing XML file: {}".format(e))
        return None
    except ValueError as e:
        print("Error: {}".format(e))
        return None

    # Return the values as a tuple
    return (shift, light, brightness) # This line returns a tuple with the values of the parameters

def handle_request(conn, addr):
    """
    Function to handle requests sent by the client. The request should be in the format:
    "set shift light brightness" or "get"
    """
    data = conn.recv(1024).decode() # This line receives data from the client, it's decoded to plain text
    print("Received request from {}: {}".format(addr, data))
    # Parse the request
    request = data.split()  # This line splits the request string into a list
    if request[0] == "set":  # This line checks if the first element of the list is "set"
        if len(request) != 4:  # This line checks if the length of the list is 4
            conn.send("Invalid request format".encode())  # This line sends an error message to the client if the request format is invalid
            return
        try:
            shift, light, brightness = map(int, request[1:])  # This line maps the int() function to the elements of the list and assigns the result to shift, light and brightness
            if shift < 0 or shift > 100 or light < 0 or light > 100 or brightness < 0 or brightness > 50000:
                raise ValueError("Invalid value for shift, light or brightness")
            # Update the XML file
            tree = ET.parse(XML_FILE) # This line parse the XML file, it creates an ElementTree object from the file
            root = tree.getroot() # This line gets the root element of the ElementTree object
            root.find("shift").text = str(shift) # This line updates the text of the shift element
            root.find("light").text = str(light) # This line updates the text of the light element
            root.find("brightness").text = str(brightness) # This line updates the text of the brightness element
            tree.write(XML_FILE) # This line write the updated ElementTree object to the XML file
            conn.send("Successfully set new values".encode()) # This line sends a success message to the client
        except ValueError as e:
            conn.send("Error: {}".format(e).encode())
    elif request[0] == "get": # This line checks if the first element of the list is "get"
        if len(request) != 1:  # This line checks if the length of the list is 1
            conn.send("Invalid request format".encode())  # This line sends an error message to the client if the request format is invalid
            return
        device_status = check_device_status() # This line calls the check_device_status() function to get the current status of the device
        if device_status is not None:
            conn.send("Device status: Shift: {}, Light: {}, Brightness: {}".format(*device_status).encode()) # This line sends the device status to the client
        else:
            conn.send("Error getting device status".encode())
    else:
        conn.send("Invalid request".encode())
def notify_clients(data):
    """
    Function to notify clients of changes in the device status using the TCP protocol
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This line creates a socket object
        s.bind((TCP_IP, TCP_PORT)) # This line binds the socket object to the IP and port specified in the constants
        s.listen(1) # This line makes the socket isten for incoming connections, it specifies a maximum of 1 connection in the queue
        while True:
            conn, addr = s.accept() # This line accepts a connection from a client, it returns a new socket object and the address of the client
            handle_request(conn, addr) # This line calls the handle_request() function to handle the request sent by the client
            conn.close() # This line closes the connection with the client
    except socket.error as e:
        print("Error creating socket: {}".format(e)) # This line print an error message if there's an error creating the socket

while True:
            # Get the current status of the device
    data = check_device_status() # This line calls the check_device_status() function to get the current status of the device
    if data is not None:
        print("Device status: Shift: {}, Light: {}, Brightness: {}".format(data[0], data[1], data[2])) # This line print the current status of the device
                # Notify clients of changes
        notify_clients(data) # This line calls the notify_clients() function to notify the clients of the changes
    else:
        print("Error getting device status, retrying in 10 seconds") # This line print an error message if there's an error getting the device status
    time.sleep(10) # This line makes the program wait for 10 seconds before retrying
