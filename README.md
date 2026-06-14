# Project 3 - QuizNet - A Multiplayer Quiz Game over UDP and TCP

**Course:** CS411 - Computer Networks - Summer 2026
**Layer:** Transport Layer
**Team size:** 2 students
**Duration:** Monday to Thursday (4 sessions x 1.5h)
**Languages:** Python 3.8+, Streamlit
**Demo:** Thursday, live, 8 minutes per team

---

## The problem

You have built an HTTP server over TCP and an auction system over UDP.
You understand how individual packets travel on the wire.

This week the question is different.

**What happens when the same application runs over two different transport
protocols? Does the choice of protocol change the behaviour of the
application itself?**

You will answer this question by building the same system twice.

**QuizNet** is a multiplayer quiz game. A server hosts a game round,
broadcasts questions to all connected players, collects answers, scores
them, and maintains a live leaderboard. You will implement this system
once over UDP and once over TCP. Same logic. Same questions. Same rules.
Different transport. Different behaviour.

On Thursday you will demo both versions side by side and explain,
with Wireshark as your evidence, exactly what changed and why.

---

## What you will build

### UDP version - `udp_quiz/`

- `server_udp.py`: broadcasts questions to all clients, receives answers,
  scores them, updates leaderboard
- `client_udp.py`: joins the game, receives questions, submits answers,
  displays feedback

### TCP version - `tcp_quiz/`

- `server_tcp.py`: same game logic as the UDP server
- `client_tcp.py`: terminal client
- `app.py`: Streamlit GUI client - connects to the TCP server and provides
  a browser-based interface for the game

Both versions use **port 8888** and share the same `questions.txt` file.

---

## Key concepts

### UDP - User Datagram Protocol

UDP is connectionless. There is no handshake before data flows. The sender
fires a datagram into the network and has no guarantee it arrives.
Packets can be lost, duplicated, or arrive out of order. The application
must decide what to do about each of these situations.

UDP is fast and lightweight. It is the right choice when low latency
matters more than guaranteed delivery: live video, online games, DNS queries.

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8888))
data, addr = sock.recvfrom(4096)   # addr = (ip, port) of sender
sock.sendto(response, addr)
```

### TCP - Transmission Control Protocol

TCP is connection-oriented. A 3-way handshake establishes a connection
before any data flows. TCP guarantees bytes arrive in order and without
loss - if a packet is dropped, TCP retransmits it automatically.

This reliability has a cost: connection setup overhead, retransmission
delays under loss, and more complex state management on the server.

```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 8888))
server.listen(10)
conn, addr = server.accept()
conn.sendall(data)
```

### One socket, many clients

In the UDP version your server has one socket for all clients.
Clients are told apart by the `addr` from `recvfrom()`.
Broadcasting means calling `sendto()` for each known client address.

In the TCP version each client has its own socket returned by `accept()`.
Broadcasting means calling `sendall()` on each of those sockets.

### Threading

Both servers must do two things at once: receive incoming messages and
run the game loop. Use threads:

```python
import threading

t = threading.Thread(target=my_function, args=(arg1,))
t.daemon = True
t.start()
```

Shared data accessed from multiple threads must be protected:

```python
lock = threading.Lock()
with lock:
    shared_dict[key] = value
```

### Streamlit

Streamlit turns a Python script into a browser interface.
Your TCP GUI client (`app.py`) uses it instead of terminal I/O.
Streamlit re-runs the entire script on every user interaction.
Use `st.session_state` to persist values between re-runs.

```bash
pip install streamlit
streamlit run app.py   # opens http://localhost:8501
```

---

## Message format

All messages are plain UTF-8 text ending with `\n`.
Both versions use the same format.

| Direction | Message | Meaning |
|-----------|---------|---------|
| client to server | `join:<username>` | register to play |
| client to server | `answer:<option>` | submit answer (a/b/c/d) |
| server to all | `question:<id>:<text>:<a>:<b>:<c>:<d>` | broadcast question |
| server to all | `correct:<username>:<points>:<leaderboard_json>` | correct answer |
| server to one | `wrong:<username>` | wrong answer |
| server to all | `timeout:<correct_answer>:<leaderboard_json>` | time expired |
| server to all | `leaderboard:<json>` | updated standings |
| server to all | `broadcast:<message>` | general announcement |

---

## The questions file

`questions.txt` must contain exactly **10 original questions** written
by your team. One question per line:

```
question_text:option_a:option_b:option_c:option_d:correct_option
```

Example:
```
What does UDP stand for?:User Datagram Protocol:Universal Data Protocol:Unified Delivery Protocol:Ultra Dynamic Protocol:a
```

The topic is your choice. Replace the sample questions with your own.

---

## Network setup

All machines must be on the same LAN.

```bash
hostname -I     # Linux - find your IP
ipconfig        # Windows - look for IPv4 Address
```

Ports needed: **8888** (game server) and **8501** (Streamlit).

---

## Environment setup

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
.\venv\Scripts\Activate.ps1     # Windows

pip install streamlit
```

---

## Running the game

### UDP version
```bash
python3 udp_quiz/server_udp.py
python3 udp_quiz/client_udp.py
```

### TCP version
```bash
python3 tcp_quiz/server_tcp.py
streamlit run tcp_quiz/app.py
python3 tcp_quiz/client_tcp.py   # optional terminal client
```

---

## Simulating packet loss

```bash
sudo tc qdisc add dev lo root netem loss 10%   # add 10% loss
sudo tc qdisc del dev lo root                   # remove
```

Run both versions under loss. The difference in behaviour is the core
of your Thursday comparison.

---

## Constraints

- `socket` module only - no networking libraries above socket
- Both versions must use port 8888
- Message format must match the table above
- `app.py` must be a working Streamlit GUI for the TCP version
- `questions.txt` must have exactly 10 original questions
- Wireshark must be live during the demo

---

## Repository structure

```
project3-quiznet/
|-- README.md
|-- questions.txt
|-- test_quiznet.py
|-- udp_quiz/
|   |-- server_udp.py
|   `-- client_udp.py
`-- tcp_quiz/
    |-- server_tcp.py
    |-- client_tcp.py
    `-- app.py
```

---

## Running the tests

```bash
# Terminal 1
python3 tcp_quiz/server_tcp.py

# Terminal 2
python3 test_quiznet.py
```

---

## Demo checklist

- [ ] UDP server starts, 2 clients join, question broadcast visible in Wireshark
- [ ] UDP version tested under artificial packet loss
- [ ] TCP server starts, Streamlit client connects, question answered
- [ ] TCP 3-way handshake visible in Wireshark per client
- [ ] Leaderboard updates correctly after each question
- [ ] `questions.txt` has exactly 10 original questions
- [ ] All tests pass: `python3 test_quiznet.py`
- [ ] UDP vs TCP comparison prepared with Wireshark evidence

---

## Demo structure (8 minutes)

| Time | What |
|------|------|
| 0:00 - 1:30 | UDP: 2 clients, one question live |
| 1:30 - 2:30 | Wireshark: broadcast datagram, answer, score |
| 2:30 - 3:00 | UDP under packet loss |
| 3:00 - 4:30 | TCP: Streamlit client, one question live |
| 4:30 - 5:30 | Wireshark: handshake, TCP stream, same loss |
| 5:30 - 6:30 | Comparison: what you observed and why |
| 6:30 - 8:00 | Peer Q&A |

---

## Grading

| Criterion | Weight |
|-----------|--------|
| UDP version working | 25% |
| TCP version working | 25% |
| Streamlit GUI functional | 15% |
| Wireshark UDP vs TCP comparison | 20% |
| Code quality and error handling | 10% |
| Optional extension | 5% |

---

*CS411 - Computer Networks - Summer 2026*
