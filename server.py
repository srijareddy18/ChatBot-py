#Chaitanya Naidu Pindi - cp22k

import socket
import select

def main():
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_vector = []
    
    # Set up server address
    addr = ('', 0)  # Use an available port assigned by the OS
    sockfd.bind(addr)
    
    # Display the assigned port number
    addr = sockfd.getsockname()
    print("Server listening on port: {}".format(addr[1]))
    
    # Get the hostname
    hostname = socket.gethostname()
    print("Server hostname: {}".format(hostname))
    
    # Listen for incoming connections
    sockfd.listen(5)
    
    allset = [sockfd]
    
    while True:
        rset, _, _ = select.select(allset, [], [])
        
        for sock in rset:
            if sock is sockfd:
                # Accept a connection request
                rec_sock, recaddr = sockfd.accept()
                print("remote machine => {}, port => {}.".format(recaddr[0], recaddr[1]))
                
                sock_vector.append(rec_sock)
                allset.append(rec_sock)
            else:
                # Handle data received from connected clients
                data = sock.recv(100)
                sender_address = sock.getpeername()  # Get sender's details to share with other clients
                if not data:
                    # Client exits
                    sock.close()
                    allset.remove(sock)
                    sock_vector.remove(sock)
                    print("remote machine = {} exited.".format(sender_address[0]))
                else:
                    # Broadcast the message to all connected clients
                    message_with_address = "{} => {}".format(sender_address[0], data.decode())
                    for client_sock in sock_vector:
                        if client_sock != sock:
                            client_sock.send(message_with_address)
    
if __name__ == "__main__":
    main()
