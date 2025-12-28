# LAB 1 – Simple RPC over TCP on AWS EC2

This project implements a minimal Remote Procedure Call (RPC) system with a client and a server running on two separate AWS EC2 instances in AWS Academy Learner Lab.

- Language: Python 3  
- Transport: TCP sockets  
- Serialization: JSON  
- RPC method: `add(a, b)`

The lab demonstrates:

- Basic RPC structure (request/response, marshalling, client/server stubs).  
- Deployment of a distributed application on two EC2 instances.  
- Failure handling with timeouts, retries and at-least-once semantics.

---

## 1. Architecture

### rpc-server-node (EC2 instance A)

- Runs `server.py`.  
- Listens on TCP port **5000** on `0.0.0.0`.  
- Exposes RPC method `add(a, b)`.

### rpc-client-node (EC2 instance B)

- Runs `client.py`.  
- Sends JSON RPC requests to the server using its public IPv4 and port **5000**.  
- Implements timeout and retry logic.

---

## 2. Prerequisites

- AWS Academy **Learner Lab** session is running and AWS Console is accessible.  
- Two EC2 instances created in **us-east-1** (or **us-west-2**):

  - `rpc-server-node` – Amazon Linux 2023, type `t3.micro` (or `t2.micro`).  
  - `rpc-client-node` – Amazon Linux 2023, type `t3.micro` (or `t2.micro`).  

- Both instances use key pair **`vockey`** (default in Learner Lab).  

- Security group (e.g. `rpc-sg`) with inbound rules:

  - `SSH` – TCP **22** – from your IP (or `0.0.0.0/0` for the lab).  
  - `Custom TCP` – TCP **5000** – from `0.0.0.0/0` (RPC traffic).

---

## 3. Getting the code onto EC2

На обоих инстансах команды одинаковые, только на сервере нужен `server.py`, а на клиенте – `client.py`.

### 3.1. SSH into instances (from your local machine)

```
cd ~/Downloads
chmod 400 labsuser.pem # downloaded from AWS Details in Learner Lab
ssh -i labsuser.pem ec2-user@<SERVER_PUBLIC_IP> # rpc-server-node
ssh -i labsuser.pem ec2-user@<CLIENT_PUBLIC_IP> # rpc-client-node
```

`<SERVER_PUBLIC_IP>` и `<CLIENT_PUBLIC_IP>` — значения **Public IPv4 address** из консоли EC2.

### 3.2. Directory structure

На обоих инстансах:
```
mkdir -p ~/rpc-lab
cd ~/rpc-lab
```
