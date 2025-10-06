import socket
import threading
import os
import json
import datetime
import random
import string
import mimetypes

# Basic multi-threaded HTTP server built using socket programming.
# It can handle GET and POST requests and serve both text and binary files.

HOST = '127.0.0.1'
PORT = 8080
UPLOAD_DIR = "uploads"

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Handle individual client requests
def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            conn.close()
            return

        # Parse HTTP request
        headers = data.split("\r\n")
        request_line = headers[0].split(" ")
        method = request_line[0]
        path = request_line[1]

        # Handle GET request
        if method == "GET":
            handle_get(conn, path)

        # Handle POST request
        elif method == "POST":
            handle_post(conn, headers, data)

        else:
            send_response(conn, 405, "Method Not Allowed")

    except Exception as e:
        print(f"[ERROR] {e}")
        send_response(conn, 500, "Internal Server Error")

    finally:
        conn.close()

# Handle GET requests (for text/html and files)
def handle_get(conn, path):
    if path == "/":
        send_response(conn, 200, "<h1>Multi-threaded HTTP Server Running</h1>", "text/html")
    else:
        # Always serve files from 'resources' folder
        file_path = os.path.join("resources", path.strip("/"))

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"

            headers = {
                "Content-Disposition": f'inline; filename="{os.path.basename(file_path)}"'
            }
            send_response(conn, 200, content, content_type, headers, binary=True)
        else:
            send_response(conn, 404, "<h1>File Not Found</h1>", "text/html")

# Handle POST request (save JSON data)
def handle_post(conn, headers, data):
    try:
        # Extract content length
        content_length = 0
        for h in headers:
            if "Content-Length" in h:
                content_length = int(h.split(":")[1].strip())
                break

        # Extract body
        body = data.split("\r\n\r\n", 1)[1]
        if len(body) < content_length:
            body += conn.recv(content_length - len(body)).decode("utf-8")

        # Save JSON data as a file
        json_data = json.loads(body)
        filename = f"upload_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{''.join(random.choices(string.ascii_lowercase, k=6))}.json"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "w") as f:
            json.dump(json_data, f, indent=4)

        response_data = {
            "status": "success",
            "message": "File created successfully",
            "filepath": f"/{filepath}"
        }

        send_response(conn, 201, json.dumps(response_data), "application/json")

    except Exception as e:
        print(f"[POST ERROR] {e}")
        send_response(conn, 400, json.dumps({"status": "error", "message": "Invalid Request"}), "application/json")

# Function to send HTTP responses
def send_response(conn, status_code, content, content_type="text/plain", extra_headers=None, binary=False):
    status_messages = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error"
    }
    status_text = status_messages.get(status_code, "OK")

    # Convert to bytes if text
    if not binary:
        content = content.encode("utf-8")

    headers = [
        f"HTTP/1.1 {status_code} {status_text}",
        "Server: Multi-threaded HTTP Server",
        f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        f"Content-Type: {content_type}; charset=utf-8",
        f"Content-Length: {len(content)}",
        "Connection: keep-alive",
        "Keep-Alive: timeout=30, max=100"
    ]

    if extra_headers:
        for k, v in extra_headers.items():
            headers.append(f"{k}: {v}")

    headers.append("\r\n")
    response = "\r\n".join(headers).encode("utf-8") + content
    conn.sendall(response)

# Main server loop
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server running on http://{HOST}:{PORT}/")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    start_server()
