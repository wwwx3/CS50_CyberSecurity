# A02 — Securing Data (Password Storage & Hashing)

## Overview

This section documents my understanding of **secure password storage**, based on **NIST Digital Identity Guidelines (SP 800-63)** and practical cybersecurity principles.

The focus is **damage reduction**:

* Hashing does **not** prevent system compromise
* It **reduces the impact** if credential data is leaked
* It makes offline password-guessing attacks **computationally expensive**

---

## NIST Guidance (Conceptual Summary)

According to NIST:

> *Verifiers shall store memorized secrets in a form that is resistant to offline attacks. Memorized secrets shall be salted and hashed using a suitable one-way key derivation function.*

### Purpose:

* Prevent attackers from efficiently guessing passwords after obtaining a hash database
* Increase the **cost per guess**
* Make large-scale brute-force attacks impractical

Hashing protects **users**, not systems.

---

##  Core Concepts

###  Hashing (Basic)

```text
Input → Hash Function → Hash Output
```

* Hash functions transform input into fixed-length output
* Same input always produces the same output
* Hashing is **one-way** (not reversible)

---

###  Hashing with Salt (Required)

```text
Input + Salt → Hash Function → Hash Output
```

* A **salt** is a random value added to each password
* Prevents:

  * rainbow table attacks
  * identical passwords producing identical hashes
* Each password must have a **unique salt**

---

###  One-Way Hash Functions

* Computationally infeasible to reverse
* Designed so attackers **cannot recover the original password**
* Security relies on **difficulty of inversion**, not secrecy of the algorithm

---

## Cryptographic Hash Functions (Examples)

### SHA-2 Family

* SHA-224
* SHA-256
* SHA-384
* SHA-512
* SHA-512/224
* SHA-512/256

### SHA-3 Family (Newer Standard)

* SHA3-224
* SHA3-256
* SHA3-384
* SHA3-512

**Note:**
SHA algorithms alone are **fast hashes** and **not ideal for password storage** unless used inside a **key derivation function**.

---

## Key Derivation Functions (Recommended)

For secure password storage, hashing should be done using:

* **PBKDF2** (NIST-approved)
* bcrypt
* scrypt
* Argon2

These functions:

* intentionally slow down hashing
* use multiple iterations
* increase attacker cost per guess

---

##  MAC-Based Constructions (Related, Not Password Hashing)

* HMAC
* CMAC
* KMAC

These are used for:

* message integrity
* authentication
* cryptographic verification

They are **not password storage mechanisms**, but are part of secure system design.

---

##  Simple Cipher Example (For Contrast)

### ROT26

```text
ROT26 = rotate alphabet 26 times → original text
```

* Demonstrates **why substitution ciphers are insecure**
* No secrecy
* No cryptographic strength
* Included for conceptual contrast only

---

## Key Takeaways

* Hashing does **not** stop breaches
* Hashing **limits damage**
* Salts prevent pre-computed attacks
* Slow, memory-hard functions protect users
* Security is about **cost and feasibility**, not perfection

---

## Ethical Note

All concepts documented here are for **defensive and educational purposes** only.
Understanding attack models is necessary to design safer systems.

---

> *“Good security assumes compromise — and plans to survive it.”*

---
