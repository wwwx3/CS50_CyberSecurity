#RSA Encryption and Decryption Implementation

#Import Library 
import math

def gcd(a, b):
    """Computes the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Computes the modular multiplicative inverse of e modulo phi."""
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1 # Should not happen with a valid e and phi

def generate_keys(p, q):
    """Generates RSA public and private keys."""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime numbers.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) == 1
    e = 0
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break
    
    if e == 0:
        raise ValueError("Could not find a suitable encryption exponent 'e'.")

    # Calculate d such that d * e = 1 (mod phi)
    d = mod_inverse(e, phi)
    
    if d == -1:
        raise ValueError("Could not find a suitable decryption exponent 'd'.")

    return (e, n), (d, n) # Public key (e, n), Private key (d, n)

def encrypt(message, public_key):
    """Encrypts a message using the public key."""
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    """Decrypts an encrypted message using the private key."""
    d, n = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return "".join(decrypted_message)

def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Example Usage
if __name__ == "__main__":
    # Choose two distinct large prime numbers
    p = 61
    q = 53

    # Generate keys
    public_key, private_key = generate_keys(p, q)
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")

    # Message to encrypt
    message = "Hello RSA!"
    print(f"Original Message: {message}")

    # Encrypt the message
    encrypted_msg = encrypt(message, public_key)
    print(f"Encrypted Message: {encrypted_msg}")

    # Decrypt the message
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print(f"Decrypted Message: {decrypted_msg}")
