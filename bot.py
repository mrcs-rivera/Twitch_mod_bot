# bot.py
import cfg
import socket
import time
import re
import select
import threading
import queue
import commands
import os
import errno


connection_good = False
chat_buffer_q = queue.Queue()


def chat(sock, chan, msg):
    with threading.Lock():
        sock.send("PRIVMSG #{} :{}\r\n".format(chan, msg).encode("utf-8"))
    print(chan + "::" + cfg.NICK + ": " + msg + "\n")


def ban(sock, user):
    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=60):
    chat(sock, ".timeout {}".format(user, secs))


def log_in_successful(response):
    if re.match(r'^:(testserver\.local|tmi\.twitch\.tv)'
                r' NOTICE \* :'
                r'(Login unsuccessful|Error logging in)*$',
                response.strip()):
        return False
    else:
        return True


def connect():
    global connection_good
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    s.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
    s.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
    response = s.recv(1024).decode("utf-8")
    print(response)
    if not log_in_successful(response):
        s.close()
        raise IOError("Twitch did not accept username/oauth combination")
    else:
        connection_good = True
        message_thread = chat_debuffer(chat_buffer_q, s)
        message_thread.daemon = True
        message_thread.start()
        for chan in cfg.CHANNELS:
            with threading.Lock():
                s.send("JOIN #{}\r\n".format(chan).encode("utf-8"))
                response = s.recv(1024).decode("utf-8")
                print(response)
            print("Joined " + chan)
    return s


def reconnect(s, msg):
    global connection_good
    connection_good = False
    with threading.Lock():
        s.shutdown(2)
        s.close()
    print(msg)
    s = connect()
    return s


class chat_debuffer(threading.Thread):
    def __init__(self, queue, s):
        threading.Thread.__init__(self)
        self.buffer = queue
        self.socket = s

    def run(self):
        global connection_good
        while connection_good:
            try:
                chan, msg = self.buffer.get(timeout=1)
            except queue.Empty:
                pass
            else:
                chat(self.socket, chan, msg)
                self.buffer.task_done()
                time.sleep(1/cfg.RATE)


def main():
    global chat_buffer_q
    lock = threading.Lock()

    cdoc = open("commands.txt", 'r+')
    commands = {}
    for i in cdoc.readlines():
        j = i.split('|')
        commands[j[0]] = j[1].strip('\n')

    print(commands)

    s = connect()
    while True:
        try:
            with lock:
                ready_to_read, read_to_write, in_error = select.select([s],[s],[],5)
        except select.error:
            s = reconnect(s, "connection error")
            continue
        if len(ready_to_read) > 0:
            with lock:
                responses = s.recv(1024).decode("utf-8")
            if responses == "" or responses == "\r\n":
                s = reconnect(s, "connection fucked up")
                continue
            for response in responses.split('\r\n'):
                #print(response + "\n")
                if response == "PING :tmi.twitch.tv":
                    with lock:
                        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    #print("Pong")
                else:
                    if response and "tmi.twitch.tv 353" not in response and "MODE #" not in response and "JOIN #" not in response and "PART #" not in response\
                            and "USERSTATE #" not in response and "ROOMSTATE #" not in response:
                        #print(response)
                        try:
                            username = re.search(r":\w+!", response).group(0)[1:-1]
                        except AttributeError as e:
                            #print("ERROR" + e.args[0])
                            continue
                        else:
                            try:
                                userlvl = re.search(r"mod=\d", response).group(0)[4]
                            except AttributeError as e:
                                #print("ERROR" + e.args[0])
                                pass
                            else:
                                try:
                                    chan = re.search(r"#\w+ ", response).group(0)[1:-1]
                                except AttributeError as e:
                                    #print("ERROR" + e.args[0])
                                    continue
                                else:
                                    try:
                                        message = response.split(chan + " :", 1)[1]
                                    except IndexError as e:
                                        #print("ERROR: response truncated" + e.args[0])
                                        message = ""
                                        continue
                                    else:
                                        print(chan + "::" + username + ": " + message + "\n")
                        output = commands.get(message.strip('\r\n'))
                        if chan == cfg.NICK and output:
                            chat_buffer_q.put((chan, output))
                        #for pattern in cfg.PATT:
                        #    if re.match(pattern, message):
                        #        ban(s, username)
                        #        break


#main()
