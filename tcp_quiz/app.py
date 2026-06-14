# tcp_quiz/app.py
# CS411 - Computer Networks - Summer 2026
# Project 3 - QuizNet - Streamlit GUI Client
#
# Team: <Lastname1-Lastname2>
#
# Run: streamlit run app.py

import streamlit as st
import socket
import threading

SERVER_IP   = "127.0.0.1"  # change to server LAN IP for real network testing
SERVER_PORT = 8888

# Streamlit re-runs the entire script on every user interaction.
# Use st.session_state to persist values between re-runs.

# TODO: initialise session state keys
# suggested keys: connected, username, sock, question, feedback, leaderboard, messages, game_over


# TODO: connect_to_server(username)
# create SOCK_STREAM socket, connect, send join: message


# TODO: send_answer(option)
# send answer: message via socket


# TODO: receive_loop()
# background thread: recv() in a loop
# parse each message type and update st.session_state accordingly
# note: you cannot call st.rerun() from a thread - set a flag instead


# ── UI ──────────────────────────────────────────────────────────────────

st.title("QuizNet")
st.caption("CS411 - Computer Networks - Summer 2026")

# TODO:
# if not connected: show username input and Join button
# if connected:
#   show current question with radio buttons for options
#   show Submit answer button
#   show feedback (correct / wrong / timeout)
#   show leaderboard
#   show broadcast messages
#   call st.rerun() with a short sleep to keep UI refreshing
