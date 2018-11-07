#-*- coding: utf-8 -*-


__all__ = [
    "start_http_server",
    "SavePostHTTPRequestHandler",
    "AllOriginHTTPRequestHandler"
]


import os
import SimpleHTTPServer
import BaseHTTPServer
from urlparse import parse_qsl
import time
import ssl


class AllOriginHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Modified HTTP Server handler to return Origin all headers and be able to return OPTIONS request

    This server handler is used in CSRF tests
    """

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))

            # Accept from all origin
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def do_OPTIONS(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_GET(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()


class SavePostHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Modified HTTP Server handler that saves all POST requests sent

    This is seen from https://github.com/sethsec/crossdomain-exploitation-framework
    as part of the exploit in xdomain vulnerability
    """

    def do_POST(self):
        """Save data from ANY POST request to a file on disk"""
        length = int(self.headers['content-length'])
        postvars = parse_qsl(self.rfile.read(length), keep_blank_values=1)
        clientIP = self.client_address[0]
        timestamp = time.time()
        filename = 'content-%s-%s.html' % (clientIP, timestamp)
        with open(filename, 'w') as html:
            html.writelines(postvars[0])

        self.log_message("POST request saved into %s" % filename)

        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()


def start_http_server(request_handler, port=80, host='', cwd=None, certfile=None, keyfile=None):
    """Helper function to start a HTTP server with a specific handler"""

    print "Server at (%s, %i), cwd=%s, certfile=%s" % (host, port, str(cwd), str(certfile))

    certf = os.path.abspath(certfile) if certfile else None
    keyf = os.path.abspath(keyfile) if keyfile else None
    old_cwd = None
    if cwd:
        old_cwd = os.path.abspath(".")
        os.chdir(cwd)

    s = None
    try:
        s = BaseHTTPServer.HTTPServer((host, port), request_handler)
        if certf and keyf:
            print "Using certificate %s" % certf
            print "Using private key %s" % keyf
            s.socket = ssl.wrap_socket(s.socket, certfile=certf, keyfile=keyf, server_side=True)
        s.serve_forever()
    except KeyboardInterrupt:
        print "Good bye!"
    finally:
        if s:
            s.server_close()
        if old_cwd:
            os.chdir(old_cwd)
