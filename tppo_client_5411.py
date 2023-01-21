import socket

TCP_IP = "localhost"
TCP_PORT = 8888

def send_request(request):
    """
    Function to send a request to the server
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((TCP_IP, TCP_PORT)) 
        s.send(request.encode()) 
        data = s.recv(1024).decode() 
        print("Received from server: {}".format(data)) 
    except socket.error as e:
        print("Error connecting to server: {}".format(e)) 

if __name__ == "__main__":
    while True:
        request = input("Enter request (set shift light brightness or get): ") 
        send_request(request) 
