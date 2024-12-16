# **Rapid Project: Building a Secure and Scalable Application**  

## **Overview**  
This project demonstrates the development of a secure and scalable web application that leverages containerized services, network segmentation, and load balancing. The application includes a REST API for handling messages and a real-time chat feature.

---

## **Features**  
- **Secure Communication**: HTTPS (SSL/TLS) enabled with a Let's Encrypt certificate.  
- **Scalable Infrastructure**: Load balancing implemented using NGINX.  
- **Network Segmentation**: Separate networks for isolating public and private services.  
- **REST API**: Full CRUD functionality for managing messages (GET, POST, PUT, DELETE).  
- **Real-Time Updates**: Integration of Flask-SocketIO for broadcasting messages.  

---

## **Prerequisites**  
- Docker and Docker Compose installed on your machine.  
- Basic knowledge of networking, REST APIs, and container orchestration.  

---

## **Getting Started**  

### **Step 1: Clone the Repository**  
```bash
git clone <repository_url>
cd <repository_name>
```

### **Step 2: Generate SSL Certificates**  
Obtain a Let's Encrypt SSL certificate:  
```bash
# Use certbot or an equivalent tool for Let's Encrypt
mkdir certs
certbot certonly --standalone -d localhost --agree-tos -m your-email@example.com --non-interactive
```

### **Step 3: Build and Start the Application**  
```bash
docker-compose up --build
```

### **Step 4: Access the Application**  
- **API Endpoints**: `https://localhost/api/`  
- **Chat World**: `https://localhost/chat-world/`  
- **Chat Private**: Accessible only on the private network.  

---

## **API Endpoints**  

### **Base URL**: `https://localhost/api`  

| Method | Endpoint         | Description                              |
|--------|------------------|------------------------------------------|
| POST   | `/message`       | Send a new message.                     |
| GET    | `/message`       | Retrieve all messages.                  |
| PUT    | `/message`       | Update an existing message.             |
| DELETE | `/message`       | Delete an existing message.             |

### **Example Requests**  

#### **POST /api/message**  
```bash
curl -X POST https://localhost/api/message \
-H "Content-Type: application/json" \
-d '{"user": "John", "message": "Hello, world!"}'
```

#### **GET /api/message**  
```bash
curl -X GET https://localhost/api/message
```

#### **PUT /api/message**  
```bash
curl -X PUT https://localhost/api/message \
-H "Content-Type: application/json" \
-d '{"id": 1, "message": "Updated message"}'
```

#### **DELETE /api/message**  
```bash
curl -X DELETE https://localhost/api/message \
-H "Content-Type: application/json" \
-d '{"id": 1}'
```

---

## **Network Configuration**  

### **Networks**  
- **mynetwork**: Public-facing services (e.g., `chat-world`).  
- **mynetwork2**: Private services (e.g., `chat-private`).  

### **CIDR Blocks**  
- `mynetwork`: `10.8.6.0/24`  
- `mynetwork2`: `10.8.7.0/24`  

---

## **Folder Structure**  
```plaintext
.
├── api/
│   ├── Dockerfile          # Dockerfile for the API service
│   ├── api.py              # Flask application
├── certs/                  # SSL certificate and key
├── chat-world/             # Public chat frontend
├── chat-private/           # Private chat frontend
├── docker-compose.yml      # Docker Compose configuration
├── nginx-proxy.conf        # NGINX configuration
└── README.md               # Documentation
```

---

## **Security Features**  
- HTTPS communication for all services using Let's Encrypt.  
- Network segmentation to isolate sensitive resources.  
- Rate limiting and secure headers implemented in NGINX for enhanced security.  

---

## **License**  
This project is open-source and available under the MIT License.  

---

## **Contributors**  
- Ricardo Almeida

