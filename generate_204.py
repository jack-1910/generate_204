# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Mock connectivitycheck.gstatic.com/generate_204 service.

Last tested on 25/5/2026, the internet connectivitycheck will support
TLSv1.2 and TLSv1.3. Therefore, this mock service has been set to support
the same TLS versions.
"""

import logging
import ssl
import threading

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Globals
HOST = "0.0.0.0"
HTTP_PORT = 8081
HTTPS_PORT = 8444

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"


class ConnectivityHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # Hide Python fingerprinting
    server_version = ""
    sys_version = ""

    def do_GET(self):
        logging.info(f"{self.client_address[0]} {self.command} {self.path}")

        if self.path == "/generate_204":
            self.send_response_only(204)

            # Real-ish headers
            self.send_header("Cross-Origin-Resource-Policy","cross-origin")
            self.send_header("Date",self.date_time_string())
            self.send_header("Content-Length", "0") # Explicitly zero-length body
            self.send_header("Connection", "keep-alive") # Keep connection alive like Google
        else:
            self.send_response(404)

            # Real-ish headers
            self.send_header("Cross-Origin-Resource-Policy","cross-origin")
            self.send_header("Date",self.date_time_string())
            self.send_header("Content-Length", "0") # Explicitly zero-length body
            self.send_header("Connection", "keep-alive") # Keep connection alive like Google

        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, format, *args):
        pass


def create_http_server():
    server = ThreadingHTTPServer((HOST, HTTP_PORT),ConnectivityHandler)
    server.server_label = "HTTP"
    return server


def create_https_server():
    server = ThreadingHTTPServer((HOST, HTTPS_PORT),ConnectivityHandler)
    server.server_label = "HTTPS"

    # TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=CERT_FILE,keyfile=KEY_FILE)

    server.socket = context.wrap_socket(server.socket,server_side=True)

    return server


def run_server(server):
    logging.info(f"Starting {server.server_label} server listening on {HOST}:{server.server_port}")
    server.serve_forever()


def main():
    logging.basicConfig(level=logging.INFO,format="[%(asctime)s] %(message)s")

    http_server = create_http_server()
    https_server = create_https_server()

    threading.Thread(
        target=run_server,
        args=(http_server,),
        daemon=True
    ).start()

    threading.Thread(
        target=run_server,
        args=(https_server,),
        daemon=True
    ).start()

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        logging.info("Shutting down")
        http_server.shutdown()
        https_server.shutdown()


if __name__ == "__main__":
    main()
