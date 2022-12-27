# Install and Docker Setup

## Prerequisites

- Docker
    - Install using official instructions
- Docker-Compose
    - Install using official instructions

## Code Deployment

- Run `docker-compose build & up -d` to build the container and run the container in background mode.
- Go to `http://localhost:5000` in a web browser. If it shows "OK" the code has been deployed successfully.

# Message Brokering

## Authorization

Message authorization is based on plain text credentials, i.e. send the message with the correct username and password.

## Routing

Queues will be automatically created based on a `queue` attribute in the message JSON. Any messages with that same value for `queue` will then be routed to the queue of the same name.