# A04 — Securing Software

## Overview

This section documents my understanding of **system security vulnerabilities**, focusing on **web-based attacks**, **local system attacks**, and **defensive design principles**.

The goal is to understand:

* how systems are compromised
* why attacks work
* how defensive mechanisms reduce risk

This work aligns with **OWASP**, **NIST**, and real-world secure system design.

---

## Web Technologies & Security Implications

### HTML — Structure of a Webpage

HTML defines the **structure** of a webpage using tags.

Example:

```html
<a href="https://example.com">Click here</a>
```

### Phishing Risk

The visible text may appear legitimate, while the actual URL redirects users to a malicious site.

➡️ Users trust appearance, not destination.

---

##  Web-Based Attacks

### 1️⃣ Cross-Site Scripting (XSS)

XSS occurs when attackers inject **JavaScript** into a webpage that executes in a user’s browser.

#### Types:

* **Reflected XSS**
  Malicious input is reflected immediately in a response (e.g., search results).
* **Stored XSS**
  Malicious script is stored on the server and executed whenever users visit the page.

#### Prevention:

* Output encoding / character escaping:

```text
<   → &lt;
>   → &gt;
&   → &amp;
"   → &quot;
'   → &apos;
```

---

### 2️⃣ SQL Injection

Occurs when user input is directly concatenated into SQL queries.

Example vulnerable query:

```sql
SELECT * FROM users WHERE username = '{username}' AND password = '{password}';
```
>Code Explaination : User login -> Hit enter -> Use Python/PHP/Java -> Construct query -> Search database to find matches

Attack example:

All users would be discarded.

```sql
'malan'; DELETE FROM users; - -'
```

Reveal passwords periodically.

```sql
'{username}' AND password ='{password}'
'malan'      AND password =''OR'1'='1'
```
>This causes authentication bypass. Because logically 1 = 1 that makes the input "true" in any case.

#### Prevention:

* **Prepared Statements / Parameterized Queries**

```sql
SELECT * FROM users WHERE username = ? AND password = ?;
```
-> Because ' ' means the end of the input function , we prepare the whole set of ' ' instead of ' for the users ,preventing them from bypass the intended ' '.

---

### 3️⃣ Command Injection

Occurs when applications pass untrusted input into system commands (`system()`, `eval()`).

#### Prevention:

* Avoid shell execution
* Validate and sanitize input
* Use allowlists instead of blocklists

---

## Developer Tools & Client Manipulation

Attackers can modify client-side HTML using browser developer tools.

Example:

```html
<input disabled type="checkbox">
```

→ attacker removes `disabled`

### Prevention:

* **Never rely on client-side validation alone**
* Always enforce validation on the **server side**

---

## Cross-Site Request Forgery (CSRF)

CSRF tricks authenticated users into making unintended requests.

### Example Attack

Auto-submitted malicious form:

```html
<form action="https://example.com/buy" method="post">
  <input name="dp" type="hidden" value="B07XLQFSK">
  <button type="submit">Buy Now</button>
</form>
<script>
document.forms[0].submit();
</script>
```
-> This leads to automatically submitting a form.

### Prevention:

* CSRF tokens (random per request)

```html
<form action="https://example.com/buy" method="post">
  <input name="csrf_token" type="hidden" value="1234abcd">
  <input name="dp" type="hidden" value="B07XLQFSK">
  <button type="submit">Buy Now</button>
</form>
```
-> The random value for this form is "1234abcd" (CSRF) 

* Or CSRF tokens via HTTP headers

---

## Local (Non-Web) Attacks

### 1️⃣ Buffer Overflow

Occurs when input exceeds allocated memory.

Consequences:

* Arbitrary Code Execution (ACE)
* Remote Code Execution (RCE)

### 2️⃣ Stack Overflow

A type of buffer overflow affecting the call stack.

### 3️⃣ Cracking / Bypassing Logic

Skipping authentication or checks via manipulation.

---

## 🔐 Defensive System Design

### Reverse Engineering & Malware Analysis

* Analyze binaries to understand behavior
* Used defensively to detect malicious logic

### Software Distribution Trust

* **Open-source software:** transparent but inspectable
* **Closed-source software:** limited visibility

### Digital Signatures

* Hash + private key → signature
* Ensures integrity and authenticity

---

## Package Managers & Trust

Examples:

* `pip`, `brew`, `gem`

Security features:

* Signed packages
* Hash verification

---

## Operating System Security

* Access controls
* Memory protections
* Process isolation

---

## Bug Bounty Programs

Ethical disclosure of vulnerabilities for rewards.

Encourages:

* responsible hacking
* proactive security improvement

---

## Vulnerability Tracking Systems

* **CVSS** — severity scoring
* **EPSS** — probability of exploitation
* **KEV** — known exploited vulnerabilities
* **OWASP** — application security risks

---

## 🌐 Network Basics

Common Ports:

* 22 — SSH
* 80 — HTTP
* 443 — HTTPS

---

## Deep Packet Inspection & Proxies

* Inspects traffic beyond headers
* Used in organizations and institutions
* Acts as a controlled intermediary

---

## Key Takeaways

* Security assumes compromise
* Defense reduces impact, not perfection
* Server-side validation is critical
* Trust must be verified continuously

---

> *“Secure systems are not unbreakable — they are resilient.”*

---
