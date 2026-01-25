#Import Lib (After installing 'cryptography' package)
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

# --- Alice generates a private/public key pair ---
alice_private_key = x25519.X25519PrivateKey.generate()
alice_public_key = alice_private_key.public_key()

# --- Bob generates a private/public key pair ---
bob_private_key = x25519.X25519PrivateKey.generate()
bob_public_key = bob_private_key.public_key()

# --- Exchange public keys (e.g., send bytes over network) ---
alice_pub_bytes = alice_public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)
bob_pub_bytes = bob_public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)

# --- Rebuild public keys from bytes on each side ---
alice_pub_received = x25519.X25519PublicKey.from_public_bytes(bob_pub_bytes)
bob_pub_received = x25519.X25519PublicKey.from_public_bytes(alice_pub_bytes)

# --- Derive shared secret (same for Alice and Bob) ---
alice_shared = alice_private_key.exchange(alice_pub_received)
bob_shared = bob_private_key.exchange(bob_pub_received)

assert alice_shared == bob_shared
print("Shared secret:", alice_shared.hex())
