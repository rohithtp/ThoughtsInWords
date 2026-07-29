# Preventing MITM Attacks in React + Django

**Date:** July 30, 2026

Preventing Man-in-the-Middle (MITM) attacks in a decoupled **React (Frontend) + Django (Backend)** architecture requires securing the transport layer, restricting client-side token exposure, and strictly configuring HTTP access headers.

A single application feature (like encrypting payloads manually in JS) won't stop MITM attacks if the TLS connection itself is manipulated. You need a multi-layered defence strategy.

## 1. Enforce Strict Transport Security (TLS/HTTPS)

Encryption in transit is your primary line of defense against network packet sniffing and interception.

* **TLS 1.2+ Everywhere:** Ensure all traffic between React, your reverse proxy (Nginx/Traefik), and Django goes over HTTPS.
* **Enable HSTS (HTTP Strict Transport Security):** Forces browsers to communicate *only* via HTTPS, neutralizing SSL-Stripping MITM attacks.

In Django’s `settings.py`, configure `SecurityMiddleware`:

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ...
]

SECURE_SSL_REDIRECT = True                     # Redirect all HTTP traffic to HTTPS
SECURE_HSTS_SECONDS = 31536000                # Enforce HTTPS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True          # Apply to subdomains
SECURE_HSTS_PRELOAD = True                     # Allow browser preload submission
```

## 2. Protect Authentication Tokens (HTTP-Only Cookies)

Storing JWTs or Session Tokens in React's `localStorage` or `sessionStorage` exposes them to XSS attacks, which attackers often combine with MITM techniques to exfiltrate keys.

* **Use `HttpOnly` Cookies:** Store authorization tokens in `HttpOnly`, `Secure`, and `SameSite` cookies. JavaScript running in React cannot access `HttpOnly` cookies, preventing stolen tokens even if client script integrity is compromised.

In Django (if using Django REST Framework / SimpleJWT or Sessions):

```python
# settings.py
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True                   # Transmit cookies ONLY via HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'                # Mitigate CSRF/MITM cross-site requests

CSRF_COOKIE_HTTPONLY = False                  # Needs to be readable if using custom JS headers
CSRF_COOKIE_SECURE = True
```

## 3. Implement Strict CORS & CSRF Controls

If an attacker attempts to inject a proxy domain or fake API endpoint between your frontend and backend, CORS and Origin validation block unauthorized requests.

### Django CORS Configuration (`django-cors-headers`)

Never set `CORS_ALLOW_ALL_ORIGINS = True` in production. Explicitly whitelist your React domain:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-react-app.com",
]
CORS_ALLOW_CREDENTIALS = True                  # Required for sending HttpOnly cookies
```

### Enforce CSRF Protection

Pass the CSRF token from Django to React and attach it via custom request headers (e.g., `X-CSRFToken`) on non-safe requests (`POST`, `PUT`, `DELETE`). Django verifies the `Origin` and `Referer` headers on incoming HTTPS traffic to ensure requests are not tampered with.

## 4. Implement Content Security Policy (CSP)

If an attacker intercepts or tampers with the JavaScript bundle served to the browser (e.g., via rogue Wi-Fi or compromised CDN), a strong CSP prevents execution of injected malicious scripts.

Add CSP headers via Django or Nginx:

```python
# settings.py
SECURE_CSP = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],                   # Restrict executable scripts to trusted origins
    "connect-src": ["'self'", "https://api.yourdomain.com"], # Restrict API calls strictly to your backend
}
```

## 5. Transport Protection for Mobile or Desktop Clients (SSL/TLS Pinning)

If your React application is packaged as a mobile or desktop app (e.g., via React Native, Capacitor, or Electron), browser web policies aren't enough.

* **Certificate / Public Key Pinning:** Hardcode the public key or hash of your Django server's SSL certificate directly into the client application.
* **Effect:** If an attacker inserts a custom Certificate Authority (CA) on the user's device (a common enterprise or proxy MITM technique), the client application detects the mismatch and immediately rejects the connection.

## Quick Implementation Checklist

| Vulnerability Vector | Defense Mechanism | Implementation Place |
| --- | --- | --- |
| Unencrypted HTTP Traffic | HSTS & TLS 1.3 Enforcement | Nginx / Django `SecurityMiddleware` |
| Token Theft via Script Injection | `HttpOnly` + `Secure` Cookies | Django Auth / JWT Cookie Setup |
| Domain/Origin Spoofing | Strict `CORS_ALLOWED_ORIGINS` | Django `django-cors-headers` |
| Malicious Injection in Frontend | Content Security Policy (CSP) | Nginx Headers / Django |
| Native Client Interception | Certificate/Public Key Pinning | Native React Client Layer |
