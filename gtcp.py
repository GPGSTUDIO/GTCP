import socket
import sys
import os
import threading
import time
import subprocess

def getheader(i,html_content):
    if i.endswith(".ico"):
        return f"""HTTP/1.1 200 OK\r
Date: Mon, 23 Sep 2024 12:34:56 GMT\r
Server: Apache/2.4.41 (Ubuntu)\r
Content-Type: image/vnd.microsoft.icon\r
Content-Length: {len(html_content)}\r
Connection: close\r
Last-Modified: Mon, 16 Sep 2024 10:00:00 GMT\r
Cache-Control: max-age=3600\r
ETag: "abc123-def456"\r
\r
"""
    elif i.endswith(".html"):
        return f"""HTTP/1.1 200 OK\r
Date: Mon, 23 Sep 2024 12:34:56 GMT\r
Server: Apache/2.4.41 (Ubuntu)\r
Content-Type: text/html; charset=UTF-8\r
Content-Length: {len(html_content)}\r
Connection: close\r
Last-Modified: Mon, 16 Sep 2024 10:00:00 GMT\r
Cache-Control: max-age=3600\r
ETag: "abc123-def456"\r
\r
"""
    elif i.endswith(".exe"):
        return f"""HTTP/1.1 200 OK\r
Date: Mon, 23 Sep 2024 12:34:56 GMT\r
Server: Apache/2.4.41 (Ubuntu)\r
Content-Type: application/x-msdownload\r
Content-Length: {len(html_content)}\r
Connection: close\r
Last-Modified: Mon, 16 Sep 2024 10:00:00 GMT\r
Cache-Control: max-age=3600\r
ETag: "abc123-def456"\r
\r
"""
    else:
        return f"""HTTP/1.1 200 OK\r
Date: Mon, 23 Sep 2024 12:34:56 GMT\r
Server: Apache/2.4.41 (Ubuntu)\r
Content-Type: text/html; charset=UTF-8\r
Content-Length: {len(html_content)}\r
Connection: close\r
Last-Modified: Mon, 16 Sep 2024 10:00:00 GMT\r
Cache-Control: max-age=3600\r
ETag: "abc123-def456"\r
\r
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((sys.argv[1].split(':')[0],int(sys.argv[1].split(':')[1])))
sock.listen()
print("GTCP Сервер запущен!\n")
def webserver(client,client_addr):
    try:
        usehtml = True
        client.settimeout(5.0)
        question = client.recv(4096).replace(b"..",b"")
        if question.startswith(b"What inside: "):
            usehtml = False
            print(f"New what inside question: {question.decode("UTF-8")[len(b"What inside: "):]} From: {client_addr}")
            questpath = "html\\"+question.decode("UTF-8")[len(b"What inside: ")+1:].replace("/","\\") # If this linux* os delete replace
            args = []
            if "?" in questpath:
                args = questpath[questpath.find("?")+1:].split("&")
                questpath = questpath[:questpath.find("?")]
            if questpath=="html\\":                # If this linux* os edit \\ to /
                if os.path.exists(r"html\index.gc"):
                    with open(r"html\index.gc", "r") as f:
                        data = f.read()
                    parsed_args = ""
                    for i in args:
                        parsed_args+="set "+i.split("=")[0]+" "+i.split("=")[1]+'\n'
                    with open(r"temp.gc","w") as f:
                        f.write(parsed_args+data)
                    result = subprocess.run(["based\\gcode.exe", "temp.gc"], capture_output=True, text=True)
                    output = result.stdout
                    client.send(b"<OKAY> No problem (text): "+output.encode("utf-8"))
                    client.close()
                elif os.path.exists(r"html\index.bat"):
                    with open(r"html\index.bat", "r") as f:
                        data = f.read()
                    parsed_args = "@echo off\n"
                    for i in args:
                        parsed_args+="set "+i+'\n'
                    with open(r"temp.bat","w") as f:
                        f.write(parsed_args+data)
                    parsed_args+"@echo on\n"
                    result = subprocess.run(["cmd.exe", "/c", "temp.bat"], capture_output=True, text=True)
                    output = result.stdout
                    client.send(b"<OKAY> No problem (text): "+output.encode("utf-8"))
                    client.close()
                elif os.path.exists(r"html\index.html"):
                    with open(r"html\index.html","rb") as f:
                        data = f.read()
                    if b'\0' in data:
                        client.send(b"<OKAY> No problem (binary): "+data)
                    else:
                        for i in args:
                            data = data.replace(b"{%"+i.split("=")[0].encode("utf-8")+b"%}",i.split("=")[1].encode("utf-8"))
                        client.send(b"<OKAY> No problem (text): "+data)
                    client.close()
                else:
                    if os.path.exists(r"based\404.html"):
                        with open(r"based\404.html","rb") as f:
                            datanot = f.read()
                        client.send(b"<404W> This is webpage: "+datanot)
                        client.close()
                    else:
                        client.send(b"<404> I think we have 404...")
                        client.close()
            else:
                if os.path.exists(questpath):
                    if questpath.endswith(".gc"):
                        with open(questpath, "r") as f:
                            data = f.read()
                        parsed_args = ""
                        for i in args:
                            parsed_args+="set "+i.split("=")[0]+" "+i.split("=")[1]+'\n'
                        with open("temp.gc","w") as f:
                            f.write(parsed_args+data)
                        result = subprocess.run(["based\\gcode.exe", "temp.gc"], capture_output=True, text=True)
                        output = result.stdout
                        client.send(b"<OKAY> No problem (text): "+output.encode("utf-8"))
                        client.close()
                    elif questpath.endswith(".bat"):
                        with open(questpath, "r") as f:
                            data = f.read()
                        parsed_args = "@echo off\n"
                        for i in args:
                            parsed_args+="set "+i+'\n'
                        with open("temp.bat","w") as f:
                            f.write(parsed_args+data)
                        parsed_args+"@echo on\n"
                        result = subprocess.run(["cmd.exe", "/c", "temp.bat"], capture_output=True, text=True)
                        output = result.stdout
                        client.send(b"<OKAY> No problem (text): "+output.encode("utf-8"))
                        client.close()
                    else:
                        with open(questpath, "rb") as f:
                            data = f.read()
                        if b'\0' in data:
                            client.send(b"<OKAY> No problem (binary): "+data)
                        else:
                            for i in args:
                                data = data.replace(b"{%"+i.split("=")[0].encode("utf-8")+b"%}",i.split("=")[1].encode("utf-8"))
                            client.send(b"<OKAY> No problem (text): "+data)
                        client.close()
                else:
                    if os.path.exists(r"based\404.html"):
                        with open(r"based\404.html","rb") as f:
                            datanot = f.read()
                        client.send(b"<404W> This is webpage: "+datanot)
                        client.close()
                    else:
                        client.send(b"<404> I think we have 404...")
                        client.close()
        with open(r"based\regist.list","r") as f:
            plist = f.read()
        for i in plist.split("\n"):
            if question.startswith(b"GET /"+i.encode("utf-8")+b" HTTP"):
                usehtml = False
                print(f"New http question. From: {client_addr} With: {question.decode("utf-8")[:len(f"GET {question.split(b"\n")[0].replace(b"GET ",b"").replace(b"HTTP",b"").decode("utf-8")}----")]}")
                with open("based\\"+i,"rb") as f:
                    html_content = f.read()
                header = getheader(i,html_content)
                client.send(header.encode() + html_content)
                client.close()
        if question.startswith(b"GET") and usehtml:
            if b"HTTP" in question:
                #print(f"New http question: {question.decode("utf-8")}")
                print(f"New http question. From: {client_addr} With: {question.decode("utf-8")[:len(f"GET {question.split(b"\n")[0].replace(b"GET ",b"").replace(b"HTTP",b"").decode("utf-8")}----")]}")
                with open(r"based\main.list","r") as f:
                    mainfilename = f.read()
                with open("based\\"+mainfilename,"rb") as f:
                    html_content = f.read()
                header = getheader(mainfilename,html_content)
                client.send(header.encode() + html_content)
                client.close()
        elif usehtml:
            print("Unkown question: "+question.decode("utf-8"))
            client.close()
    except TimeoutError:
        #print(f"🖕 Timeout - плохой клиент {client_addr} послан нахуй")
        print(f"🕜 Timeout - разрыв соединения с {client_addr}")
    except Exception as e:
        print(f"💀 Клиент {client_addr} сдох: {e}")
while True:
    client, client_addr = sock.accept()
    web_thread = threading.Thread(target=webserver,args=(client,client_addr))
    web_thread.daemon = True
    web_thread.start()
    time.sleep(0.5)