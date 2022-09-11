import socket
import Setings

host = Setings.hostName
port = Setings.serverPort

headers = """\
POST /order HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

body = '"order_id": 1,' \
       '"table_id": 1,' \
       '"waiter_id": 1,' \
       '"items": [ 3, 4, 4, 2 ],' \
       '"priority": 3,' \
       '"max_wait": 45,' \
       '"pick_up_time": 1631453140 // UNIX timestamp' \
       '"cooking_time": 65' \
       '"cooking_details": [' \
       '    {' \
       '"food_id": 3,' \
       '"cook_id": 1,' \
       '},' \
       '{' \
       '"food_id": 4,' \
       '"cook_id": 1,' \
       '},' \
       '{' \
       '"food_id": 4,' \
       '"cook_id": 2,' \
       '},' \
       '{' \
       '"food_id": 2,' \
       '"cook_id": 3,' \
       '},' \
       ']'
body_bytes = body.encode('ascii')
header_bytes = headers.format(
    content_type="application/json",
    content_length=len(body_bytes),
    host=str(host) + ":" + str(port)
).encode('iso-8859-1')

payload = header_bytes + body_bytes


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

s.sendall(payload)
print(s.recv(1024))