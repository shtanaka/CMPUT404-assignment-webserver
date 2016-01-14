#  coding: utf-8 
import SocketServer
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024)
        print ("Got a request of: %s\n" % self.data)
        self.data = self.data.split(" ")
        method = self.data[0]
        path = self.data[1]
        response = '' 
        path = "www/" + path[1:]
        
        if path[-1] == "/" :
            path = path + "index.html"

        if method == "GET" :
            try:
                if "/.." in path:
                    raise Exception

                file_handler = open(path, 'rb')
                response = file_handler.read()
                file_handler.close()
                self.request.send('HTTP/1.1 200 OK\r\n')
                mimetype, _ = mimetypes.guess_type(path)
                self.request.send('content-type: ' + mimetype + '\n\n')
#               self.request.send('\\n\n')
                self.request.send(response)
            except Exception as e:
                self.request.send('HTTP/1.1 404 Not Found\r\    n')
                self.request.send('content-type: text/html\n\n')
                self.request.send('<html><body><h1>page not found 404</h1></body></html>')
    
                
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
