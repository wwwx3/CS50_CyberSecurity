# A04 — Securing Software

## Overview

This section documents my understanding of **software and web security vulnerabilities**, focusing on:

- how web technologies are abused
- why attacks succeed
- how defensive design reduces risk

The emphasis is on **attack mechanics**, not just definitions.

---

## Core Security Lens

```

Input → Interpretation → Execution → Impact → Mitigation

````

Most web vulnerabilities occur when **untrusted input is interpreted as trusted code or actions**.

---

## Web Technologies & Security Implications

### HTML — Structure, Not Behavior

HTML defines the **structure and presentation** of a webpage, not its intent or safety.

Example:

```html
<a href="https://example.com">Click here</a>
````

### Security Implication: Phishing

* Users see **visible text**
* Browsers follow the **actual URL**

An attacker can exploit this mismatch:

```html
<a href="https://evil.com">https://bank.com</a>
```

➡️ **Trust in appearance, not destination**

---

## HTTP Methods & Security Semantics

### GET Requests

* Parameters appear in the URL
* Easily logged, cached, bookmarked
* Intended for **retrieving data**
* ❌ Not suitable for sensitive actions

Example:

```http
GET /search?q=<script>alert(1)</script> HTTP/1.1
```

---

### POST Requests

* Parameters sent in request body
* Not visible in URL
* Intended for **state-changing actions**

Example:

```http
POST /comment HTTP/1.1

message=<script>alert(1)</script>
```

⚠️ **POST improves privacy and semantics, not security**
JavaScript can still submit POST requests automatically.

---

## Web-Based Attacks

### 1️⃣ Cross-Site Scripting (XSS)

#### What it is

XSS occurs when **attacker-controlled JavaScript** is executed in a victim’s browser under a trusted origin.

#### Why it works

* Application fails to sanitize or encode user input
* Browser trusts content from the site

---

### Types of XSS

#### Reflected XSS

Malicious input is reflected immediately in a server response.

Example (via GET):

```http
GET /search?q=<script>alert(1)</script>
```

If the server reflects `q` directly into HTML:

```html
<script>alert(1)</script>
```

➡️ Script executes instantly.

---

#### Stored XSS

Malicious input is stored on the server and executed later.

Example (via POST):

```http
POST /comment
comment=<script>stealCookies()</script>
```

Every user who loads the comment triggers the script.

---

#### Impact

* Session hijacking
* Credential theft
* DOM manipulation
* Unauthorized actions on behalf of users

---

#### Mitigation

* Output encoding
* Input validation
* Content Security Policy (CSP)
* HttpOnly cookies

---

### 2️⃣ Cross-Site Request Forgery (CSRF)

#### What it is

CSRF tricks a user’s browser into sending **authenticated requests** without user intent.

#### Why it works

* Browsers automatically attach cookies
* Server does not verify request intent

---

#### Example (POST does NOT prevent this)

```html
<form action="https://bank.com/transfer" method="POST">
  <input type="hidden" name="amount" value="1000">
  <input type="hidden" name="to" value="attacker">
</form>

<script>
  document.forms[0].submit();
</script>
```

User does nothing.
Browser sends cookies.
Server trusts request.

---

#### Impact

* Unauthorized transactions
* Account changes
* Data manipulation

---

#### Mitigation

* CSRF tokens
* SameSite cookies
* Origin / Referer validation

---

## Key Takeaways

* **GET vs POST is about intent, not trust**
* **Client-side controls are not security**
* **Browsers are powerful and dangerous when trusted blindly**
* **Most attacks exploit implicit trust assumptions**

---

## Final Principle

> Security fails when **input is trusted**, **intent is assumed**, or **execution is implicit**.

---

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
We could even replace the placeholder ('{username}' etc.) with a symbol instead which is called Prepared statement syntax (?) instead.
Stored statement could help prevent better too.

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
