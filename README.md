# Web-and-Proxy-Server
This project involves requesting files from a Web Server with socket programming in Python. HTTP requests/responses are used to communicate between a client and server. A proxy server also acts as an intermediary between the client and server to get previously accessed files quicker. 

Two sample files are given to test the servers on: an html and jpg file. When a client requests a file from the server on a web browser, it sends the request to the proxy server that forwards it to the web server. The web server then sends the file to the proxyif it contains it. The proxy server forwards the requested file to the client after caching it if it was not already cached. 

If a requested file was cached by the proxy, then the proxy does not forward anything to the web server and immediately sends the file to the client after receiving the request.

Team members of project: Steven Lin and Nathan Lai
