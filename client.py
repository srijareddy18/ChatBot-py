#Chaitanya Naidu Pindi - cp22k

import sys
import socket
import select

def main():
    if len(sys.argv) != 3:
        print("Usage: %s server_name_or_ip port" % sys.argv[0])
        sys.exit(1)

    server_name_or_ip = sys.argv[1]
    port = int(sys.argv[2])

    print("%s %s" % (server_name_or_ip, port))

    hints = socket.AI_PASSIVE
    res = socket.getaddrinfo(server_name_or_ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    flag = 0
    for addrinfo in res:
        family, socktype, proto, canonname, sockaddr = addrinfo
        sockfd = socket.socket(family, socktype, proto)
        try:
            sockfd.connect(sockaddr)
            flag = 1
            break
        except socket.error:
            sockfd.close()

    if flag == 0:
        print("Cannot connect")
        sys.exit(1)

    orig_set = set()
    orig_set.add(sys.stdin)
    orig_set.add(sockfd)

    while True:
        rset, _, _ = select.select(orig_set, [], [])
        if sys.stdin in rset:
            buf = sys.stdin.readline()
            if not buf:
                sys.exit(0)
            sockfd.sendall(buf.encode())
        if sockfd in rset:
            buf = sockfd.recv(100)
            if not buf:
                print("Server Halted.")
                sys.exit(0)
            print("{}".format(buf.decode()))

if __name__ == "__main__":
    main()
