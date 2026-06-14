# udp_quiz/server_udp.py
# CS411 - Computer Networks - Summer 2026
# Project 3 - QuizNet
#
# Team: <Lastname1-Lastname2>
#
# Run: python3 server_udp.py

import socket
import threading
import json
import time

HOST = ''
PORT = 8888
QUESTION_TIMEOUT = 30  # seconds per question


# TODO: load questions from questions.txt

# TODO: keep track of connected clients (address -> username)

# TODO: keep track of scores (username -> points)


def broadcast(sock, message):
    # TODO: send message to all known client addresses
    pass


def game_loop(sock, questions):
    # TODO:
    # wait for at least 2 players
    # for each question:
    #   broadcast the question
    #   start a timer
    #   wait for a correct answer or timeout
    #   broadcast the result and updated leaderboard
    pass


def receive_loop(sock):
    # TODO:
    # recvfrom() in a loop
    # handle join: and answer: messages
    pass


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f'QuizNet UDP server on port {PORT}')

    # TODO: load questions, start receive thread, run game loop


if __name__ == '__main__':
    main()
