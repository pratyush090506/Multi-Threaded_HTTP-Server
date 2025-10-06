# 🧠 Multi-Threaded HTTP Server  
**Made By:** Pratyush Mohanty  

## 📌 Overview
This project is a **multi-threaded HTTP server** built from scratch using **Python’s socket programming**.  
It handles multiple client connections concurrently, supports both **GET** and **POST** requests, serves **static files (HTML, PNG, JPEG, TXT)**, and also supports **binary file transfers** like images.

The project demonstrates concepts of **network programming**, **thread synchronization**, and **HTTP protocol handling**.

---

## ⚙️ Features Implemented
✅ Handles multiple clients simultaneously using **ThreadPoolExecutor**  
✅ Supports **GET requests** for static files (HTML, images, text)  
✅ Supports **POST requests** for uploading JSON data  
✅ Implements **binary transfer** for PNG and JPG files  
✅ Returns proper **HTTP response headers and codes** (200, 201, 404, etc.)  
✅ Uses **persistent connections (Keep-Alive)**  
✅ Implements **host validation** and **error handling**  
✅ Logs requests and stores uploads in a separate `/uploads` folder  

---

## 📁 Folder Structure
```
CN_Project/
│
├── server.py
├── README.md
│
├── uploads/
│   └── upload_20251005_204522_kexucr.json
│
└── resources/
    ├── index.html
    ├── about.html
    ├── contact.html
    ├── logo.png
    ├── banner.png     # >1MB PNG file
    ├── photo.jpg
    ├── photo2.jpg
    └── sample.txt
```

---

## 🧩 How to Run
### **1. Run the server**
```bash
python3 server.py
```

### **2. Test using curl**
#### Access Homepage
```bash
curl -v http://127.0.0.1:8080/
```

#### Fetch an Image
```bash
curl -v "http://127.0.0.1:8080/logo.png" -o logo.png
```

#### Upload JSON Data
```bash
curl -v -H "Content-Type: application/json" -d '{"name":"pratyush"}' http://127.0.0.1:8080/upload
```

---

## 🧱 Binary Transfer Implementation
When a **binary file (e.g., .png, .jpg)** is requested, the server:
1. Detects its MIME type using the file extension.  
2. Opens the file in binary mode (`rb`).  
3. Sends appropriate headers (`Content-Type`, `Content-Length`, `Content-Disposition`).  
4. Streams the file directly over the socket.

This allows smooth transfer of large files like images (>1MB) without corruption.

---

## 🧵 Thread Pool Architecture
Instead of creating a new thread for each client, the server uses a **ThreadPoolExecutor**.  
- A fixed number of worker threads (e.g., 10) are created at startup.  
- Incoming client connections are added to a queue.  
- Available threads pick up tasks from the queue and handle requests concurrently.

This improves **performance** and prevents **thread explosion** under high load.

---

## 🔒 Security Measures
- **Host validation:** Ensures only requests to `127.0.0.1` are processed.  
- **Input sanitization:** Prevents directory traversal attacks by restricting access to `/resources` folder only.  
- **Connection timeout and keep-alive limits** are implemented to prevent misuse.  

---

## ⚠️ Known Limitations
- Does not currently support **HTTPS / TLS**.  
- No caching mechanism is implemented.  
- MIME type detection is basic (extension-based).  
- Designed for local testing, not production use.  

---

## 📜 Example Outputs
```
$ curl -v http://127.0.0.1:8080/
<h1>Multi-threaded HTTP Server Running</h1>

$ curl -v -H "Content-Type: application/json" -d '{"name":"pratyush"}' http://127.0.0.1:8080/upload
{"status": "success", "message": "File created successfully", "filepath": "/uploads/upload_20251005_204522_kexucr.json"}
```

---

## 👨‍💻 Conclusion
This project demonstrates a strong understanding of:
- HTTP request/response cycle  
- Socket-level communication  
- Multithreading and resource synchronization  
- Binary and text data handling  

It’s a clean, functional, and realistic implementation of a **multi-threaded web server**.
