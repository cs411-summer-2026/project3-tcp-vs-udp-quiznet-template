# test_quiznet.py
# CS411 - Computer Networks - Summer 2026
# Automated tests for Project 3 - QuizNet
#
# Run with: python3 test_quiznet.py
# The TCP server must be running before you run these tests.

import socket
import time
import os
import sys

PASS = 0
FAIL = 0

SERVER_IP   = "127.0.0.1"
SERVER_PORT = 8888


def check(name, condition, detail=''):
    global PASS, FAIL
    if condition:
        print(f'  PASS  {name}')
        PASS += 1
    else:
        print(f'  FAIL  {name}' + (f' - {detail}' if detail else ''))
        FAIL += 1


def tcp_connect(username, timeout=3.0):
    """Connect and join as a test client. Returns socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((SERVER_IP, SERVER_PORT))
    s.sendall(f"join:{username}\n".encode())
    return s


def recv_until(s, keyword, timeout=5.0):
    """Read from socket until a message containing keyword arrives."""
    deadline = time.time() + timeout
    buf = ""
    while time.time() < deadline:
        try:
            chunk = s.recv(4096).decode()
            if not chunk:
                break
            buf += chunk
            for line in buf.split('\n'):
                if keyword in line:
                    return line.strip()
        except socket.timeout:
            pass
    return None


print(f'\nRunning tests against TCP server on {SERVER_IP}:{SERVER_PORT}\n')


# ── Test 1: TCP connection and JOIN ───────────────────────────────────────────
print('1. TCP connection and JOIN')
try:
    s1 = tcp_connect("test_player_1")
    check('Connected to server', True)
    # Server should broadcast a join message or send an ACK
    time.sleep(0.5)
    check('Socket is open after join', s1.fileno() != -1)
    s1.close()
except ConnectionRefusedError:
    check('Connected to server', False, 'connection refused - is the TCP server running?')
    sys.exit(1)
except Exception as e:
    check('TCP connection completed', False, str(e))


# ── Test 2: Multiple clients connect ─────────────────────────────────────────
print('\n2. Multiple clients connect simultaneously')
try:
    s1 = tcp_connect("multi_test_1")
    s2 = tcp_connect("multi_test_2")
    check('Client 1 connected', s1.fileno() != -1)
    check('Client 2 connected', s2.fileno() != -1)
    check('Both connected at the same time', s1.fileno() != -1 and s2.fileno() != -1)
    s1.close()
    s2.close()
except Exception as e:
    check('Multiple connections completed', False, str(e))


# ── Test 3: Question format ───────────────────────────────────────────────────
print('\n3. Question broadcast format')
try:
    s1 = tcp_connect("format_test_1")
    s2 = tcp_connect("format_test_2")
    time.sleep(0.5)

    # Wait for a question broadcast
    question_line = recv_until(s1, "question:", timeout=35)
    check('Question received', question_line is not None,
          'no question received within 35s - is the game starting?')

    if question_line:
        parts = question_line.split(':')
        check('Question has at least 7 parts (id+text+4 options+answer)',
              len(parts) >= 7,
              f'got {len(parts)} parts: {question_line[:80]}')
        check('First part is "question"', parts[0] == 'question')

    s1.close()
    s2.close()
except Exception as e:
    check('Question format test completed', False, str(e))


# ── Test 4: Answer submission ─────────────────────────────────────────────────
print('\n4. Answer submission and response')
try:
    s1 = tcp_connect("answer_test_1")
    s2 = tcp_connect("answer_test_2")
    time.sleep(0.5)

    # Wait for a question
    recv_until(s1, "question:", timeout=35)
    recv_until(s2, "question:", timeout=5)

    # Submit an answer
    s1.sendall(b"answer:a\n")
    time.sleep(0.5)

    # Should receive either correct: or wrong:
    resp = recv_until(s1, "correct:", timeout=3) or recv_until(s1, "wrong:", timeout=3)
    check('Server responds to answer', resp is not None,
          'no correct: or wrong: received')
    if resp:
        check('Response is correct: or wrong:',
              resp.startswith('correct:') or resp.startswith('wrong:'))

    s1.close()
    s2.close()
except Exception as e:
    check('Answer test completed', False, str(e))


# ── Test 5: questions.txt exists and has 10 questions ─────────────────────────
print('\n5. questions.txt validation')
try:
    q_path = 'questions.txt'
    check('questions.txt exists', os.path.isfile(q_path),
          f'file not found at {q_path}')
    if os.path.isfile(q_path):
        with open(q_path) as f:
            lines = [l.strip() for l in f if l.strip()]
        check('Contains exactly 10 questions', len(lines) == 10,
              f'found {len(lines)} non-empty lines')
        if lines:
            parts = lines[0].split(':')
            check('First question has correct format (6 colons)',
                  len(parts) == 6,
                  f'expected 6 fields, got {len(parts)}: {lines[0][:60]}')
            check('Correct answer field is a/b/c/d',
                  parts[-1] in ('a', 'b', 'c', 'd'),
                  f'got: {parts[-1]}')
except Exception as e:
    check('questions.txt test completed', False, str(e))


# ── Test 6: Client disconnect handled gracefully ──────────────────────────────
print('\n6. Client disconnect handled gracefully')
try:
    s1 = tcp_connect("disconnect_test_1")
    s2 = tcp_connect("disconnect_test_2")
    s3 = tcp_connect("disconnect_test_3")
    time.sleep(0.3)

    # Disconnect one client abruptly
    s2.close()
    time.sleep(1.0)

    # Remaining clients should still be connected
    try:
        s1.sendall(b"answer:a\n")
        check('Server handles client disconnect gracefully', True)
    except Exception:
        check('Server handles client disconnect gracefully', False,
              'sending after disconnect caused an error on another client')

    s1.close()
    s3.close()
except Exception as e:
    check('Disconnect test completed', False, str(e))


# ── Summary ───────────────────────────────────────────────────────────────────
total = PASS + FAIL
print(f'\n{"=" * 40}')
print(f'Results: {PASS}/{total} passed')
if FAIL == 0:
    print('All tests pass - good to go for Thursday.')
else:
    print(f'{FAIL} test(s) failed - fix these before the demo.')
print()
