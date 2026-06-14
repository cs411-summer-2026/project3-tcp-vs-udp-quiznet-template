# udp_quiz/client_udp.py
# CS411 - Computer Networks - Summer 2026
# Project 3 - QuizNet
#
# Team: <Lastname1-Lastname2>
#
# Run: python3 client_udp.py

import socket
import threading

SERVER_IP   = input("Server IP (Enter for localhost): ").strip() or "127.0.0.1"
SERVER_PORT = 8888
USERNAME    = input("Your username: ").strip()

running = True


def receive_loop(sock):
    # TODO:
    # recvfrom() in a loop while running
    # display question:, correct:, wrong:, timeout:, leaderboard:, broadcast: messages
    pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))

    # TODO: send join: message
    # TODO: start receive thread
    # TODO: read answer input (a/b/c/d) and send answer: message


if __name__ == '__main__':
    main()
