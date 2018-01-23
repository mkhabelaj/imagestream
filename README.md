# imagestream
### The purpose of the it project is the receive, a stream of jpeg images and redirect them to the browser as a video.

The ```socket_server.py``` receives images on a specified port. The ```web_socket_server.py``` sends image to a web
browser on a specific port. The ```web_sock_relay.py``` relays the images from the socket server to the web socket 
server.

The ```socket_server.py``` class receives the a struct the display the size
the receives the image as jpeg.
```python
import socket
from struct import pack

HOST = '127.0.0.1'
PORT = 5000
SERVER_ADDRESS = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(SERVER_ADDRESS)
except Exception as ex:
    print('could not connect', ex)
finally:
    print('continuing')

with open('/home/user/Pictures/user icons/my_pic.png', 'rb') as fp:
    file_size = len(fp.read())
    fp.seek(0)
    image_data = fp.read()
try:
    print('sending data')
    file_information = "file_size {file_size}\r\n".format(file_size=file_size)
    length = pack('>Q', file_size)

    for n in range(10):
        client_socket.send(length)
        client_socket.sendall(image_data)
except Exception as ex:
    print('could not send data', ex)

```

The socket server will yield the image data to the web socket server, which will then be transmitted
to the browser.

The the browser HTML will look similar to this:
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <title>livecamera</title>
    <meta charset="UTF-8">
</head>
<body>
<img id="liveImg" width="480" height="360">

</body>
<script>
    if (window.Worker) {
        console.log('worker, exists');
        var worker = new Worker('worker.js')
        var img = document.getElementById("liveImg");
        var arrayBuffer;

        var ws = new WebSocket("ws://localhost:8090/camera");
        ws.binaryType = 'arraybuffer';

        ws.onopen = function () {
            console.log("connection was established");
        };
        ws.onmessage = function (evt) {
            arrayBuffer = evt.data;
            worker.postMessage(new Uint8Array(arrayBuffer))
        };
        worker.onmessage = function (e) {
            img.src = "data:image/jpeg;base64," + e.data;
        }
    }

</script>
</html>

```
The ```worker.js``` serves as an image converter and looks like this:
```javascript

function encode(input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    while (i < input.length) {
        chr1 = input[i++];
        chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
        chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }
        output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
            keyStr.charAt(enc3) + keyStr.charAt(enc4);
    }
    return output;
}
this.onmessage = (function (e) {
    var result = encode(e.data)
    this.postMessage(result);
});

```

to activate the server you can run this the bash script:
```bash
./initiate_screen.sh test testing 5000 security 8090 test
```