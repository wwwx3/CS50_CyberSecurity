# A03 – Securing Systems

---

## Concept

Structured notes inferred from **CS50’s Securing Systems lectures**.
Focused on understanding **how systems fail**, **what attackers exploit**, and **how defenses reduce risk** rather than eliminate it.

---

## Core Security Model

```
System → Attack → Impact → Mitigation
```

Security is not about being “secure”, but about **reducing exposure and damage** under realistic threat models.

---

## Topics Covered

* Network & Wi-Fi Security
* HTTP / HTTPS / TLS
* Cookies & Sessions
* Certificates & Certificate Authorities (CA)
* Ports & Services
* Malware & Attacks
* Defensive Systems

---

# 1. Network & Wi-Fi Security

## System: Wi-Fi (WPA)

### What it is

**WPA (Wi-Fi Protected Access)** encrypts traffic **between a device and the wireless access point**.

### Attack

* Packet sniffing on **open or weakly protected Wi-Fi**
* Evil twin access points
* Local Man-in-the-Middle (MITM)

### Impact

* Attackers can read or modify traffic **before it reaches the internet**
* Credentials, cookies, and requests can be exposed if higher-layer encryption is absent

### Mitigation

* WPA2 / WPA3 for local encryption
* **HTTPS and VPN are still required**
* WPA ≠ end-to-end security

> WPA protects the *last hop*, not the entire journey.

---

## System: VPN (Virtual Private Network)

### What it is

A VPN creates an **encrypted tunnel between the user and a VPN server**.

### Attack

* Local network sniffing
* ISP monitoring
* Public Wi-Fi interception

### Impact

* Without a VPN, local attackers can observe traffic metadata
* VPN does **not** protect traffic after it exits the VPN server

### Mitigation

* VPN encrypts traffic up to the VPN server
* HTTPS is still required beyond the VPN
* Trust shifts from ISP → VPN provider

---

# 2. Web Security

## System: HTTP (HyperText Transfer Protocol)

### What it is

A plaintext protocol for transferring web resources between a client and a server.

### Attack

* Man-in-the-Middle (MITM)
* Packet sniffing
* Content injection
* Session hijacking

### Impact

Sensitive data is exposed in transit, including:

* URLs and query strings
* POST request bodies
* Cookies and session identifiers

#### Example

```http
GET /search?q=cats HTTP/3
Host: example.com
```

```http
POST /checkout HTTP/3
Host: example.com
number=4242424242424242
```

Any intermediary can read or modify this data.
(Note: q= and number= may contain more sensitive data) 

### Mitigation

* HTTPS (HTTP over TLS, which was SSL in previous patches)
* Avoid transmitting sensitive data over plaintext protocols

---

## System: Client-Side Execution (HTML + JavaScript)

### Attack: Cross-Site Scripting (XSS)

Injected JavaScript executes **inside the trust context of a website**.
(Note: In this case, the injected script contains an ad.) 

```html
<script src="ad.js"></script>
```

### Impact

* Cookie theft
* DOM manipulation
* User impersonation
* Credential exfiltration

> This is **not an HTML vulnerability**, but a **JavaScript execution vulnerability**.

### Mitigation

* Input sanitization
* Output encoding
* Content Security Policy (CSP)
* HttpOnly cookies

---

## System: Cookies & Sessions

### What they are

Session cookies act as **bearer tokens** that identify an authenticated user.
(Note: Here the cookie id is after session=)

```http
HTTP/3 200
Set-Cookie: session=1234abcd
```

```http
GET / HTTP/3
Cookie: session=1234abcd
```

### Attack: Session Hijacking

* Attacker steals the session cookie
* The server cannot distinguish the attacker from the legitimate user

### Impact

* Full account impersonation
* No password required once the cookie is stolen

### Mitigation

* HTTPS
* HttpOnly and Secure cookie flags
* Short session lifetimes
* Regeneration of session IDs

---

# 3. HTTPS & Cryptography

## System: HTTPS (HTTP over TLS)

### What it provides

* **Confidentiality** – encryption
* **Integrity** – tamper detection
* **Authenticity** – server identity verification

TLS is the modern successor to SSL.

---

## System: Certificates & Certificate Authorities

### What a certificate does

An **X.509 certificate** binds a domain name to a public key.

### Trust Model

* Certificates are signed by **Certificate Authorities (CA)**
* Browsers maintain a **trusted CA store**

### Simplified Verification Process

1. Certificate data is hashed
2. CA signature is verified using CA’s public key
3. Browser checks:

   * Signature validity
   * Domain match
   * Expiry date
   * Trust chain

---

## Attack: TLS (SSL) Stripping

### How it works

* User initially connects via `http://`
* Attacker blocks HTTPS upgrade
* User never reaches encryption

### Impact

* Traffic silently downgraded to plaintext
* Enables MITM attacks even on HTTPS-capable sites

### Mitigation: HSTS

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

* Forces browser to use HTTPS
* `max-age` allows recovery from misconfiguration
* Preload is permanent and risky if done incorrectly

> HSTS uses an expiry because **security must be reversible** when mistakes happen.

---

## CA Trust Warning (Important)

Devices issued by:

* Companies
* Universities
* Schools

may install **custom trusted CAs**, allowing:

* HTTPS interception
* TLS inspection

This can **break end-to-end trust** even though the browser shows HTTPS.

---

# 4. Ports & Services

## System: Ports

Ports identify which service should receive incoming traffic.

| Port | Service |
| ---- | ------- |
| 80   | HTTP    |
| 443  | HTTPS   |
| 22   | SSH     |

---

## Attack: Port Scanning

* Tools like `nmap`, `dirb`
* Scans for open and vulnerable services

### Impact

* Exposed services become attack surfaces
* Non-standard ports alone do not provide security

### Mitigation

* Firewalls
* Service hardening
* Authentication
* Regular audits

> Security through obscurity alone is ineffective.

---

## System: SSH (Secure Shell)

### What it is

Encrypted remote command execution.

```bash
$ date
Thu Jan 1 12:00:00 AM EST 1970

$ ssh stanford.edu
$ date
Wed Dec 31 09:00:00 PM PST 1969
```

Different output reflects **different machines and time zones**, not insecurity.

---

# 5. Malware & Attacks

## Malware Types

| Type   | Description               |
| ------ | ------------------------- |
| Virus  | Requires user action      |
| Worm   | Self-propagating (could jump from machine to machine)          |
| Botnet | Remote-controlled malware |

---

## Attacks

### DoS / DDoS

* Exhausts system resources
* Often powered by botnets

### Impact

* Service unavailability
* Financial and reputational damage

---

## Zero-Day Attacks

### What they are

* Exploit unknown vulnerabilities
* No patch exists at the time of the attack

### Mitigation

* Defense-in-depth
* Rapid patching
* Monitoring and anomaly detection

---

# 6. Defensive Systems

## Firewall

* Filters traffic by IP address and port
* Reduces exposed attack surface

## Proxy

* Intermediary between client and server
* Can inspect, modify, or block traffic
* **Yes: proxies are middleware**

## Deep Packet Inspection (DPI)

* Inspects packet payloads
* Detects malware, suspicious patterns
* Raises privacy concerns

## Updates

* Patch known vulnerabilities
* Reduce the window of exposure for exploits

---

## Final Note

Security is not absolute.
Every mitigation introduces **trade-offs** between usability, performance, privacy, and recoverability.

---
