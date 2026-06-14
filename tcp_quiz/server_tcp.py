# tcp_quiz/server_tcp.py
# CS411 - Computer Networks - Summer 2026
# Project 3 - QuizNet
#
# Team: <Lastname1-Lastname2>
#
# Run: python3 server_tcp.py

import socket
import threading
import json
import time

HOST = ''
PORT = 8888
QUESTION_TIMEOUT = 30  # seconds per question


# TODO: load questions from questions.txt

# TODO: keep track of client connections (username -> socket)

# TODO: keep track of scores (username -> points)


def broadcast(message):
    # TODO: sendall() to every connected client socket
    pass


def handle_client(conn, addr):
    # TODO:
    # receive join: to get username
    # register client
    # loop: receive answer: messages and process them
    # on disconnect: remove from clients
    pass


def game_loop(questions):
    # TODO: same structure as UDP game_loop
    # use broadcast() instead of broadcast(sock, ...)
    pass


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f'QuizNet TCP server on port {PORT}')

    # TODO: load questions
    # TODO: start game_loop thread
    # TODO: accept() loop - spawn handle_client thread per connection


if __name__ == '__main__':
    main()
