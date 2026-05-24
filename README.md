# Generate 204

A lightweight Python implementation of a mock Google-style
`/generate_204` connectivity check endpoint.

This project is intended for:

- Home lab environments
- Captive portal research
- Internet connectivity testing
- DNS sinkhole experimentation
- HTTP/HTTPS interception research

The server provides:

- HTTP and HTTPS listeners
- `/generate_204` endpoint returning `204 No Content`
- keep-alive support
- minimal Google-like response headers
- optional TLS support using self-signed certificates

## Features

- Python standard library only
- Threaded HTTP/HTTPS servers
- HTTP/1.1 support
- TLS support
- Minimal fingerprinting
- Simple deployment

## Requirements

- Python 3.14+ (this was tested against)
- OpenSSL (for certificate generation)

## Generate TLS Certificate

Generate a self-signed certificate for lab usage:

```bash
openssl req \
  -x509 \
  -newkey rsa:4096 \
  -sha256 \
  -days 3650 \
  -nodes \
  -keyout key.pem \
  -out cert.pem \
  -subj "/CN=connectivitycheck.gstatic.com"
```

## Run

```bash
sudo python3.14 generate_204.py

# Tests
curl -kiv http://localhost:8080/generate_204
curl -kiv http://localhost:8080/
curl -kiv https://localhost:8443/generate_204
curl -kiv https://localhost:8443/
```
