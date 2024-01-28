from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from base64 import b64encode


def generateWireguardKeys():
    """
    Generate WireGuard keys
    :return: Private key and public key in Base64
    """
    # Generate private key in X25519 format
    private_key = x25519.X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Generate public key in X25519 format
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # Return Base64 encoded keys
    return b64encode(private_bytes).decode('utf-8'), b64encode(public_bytes).decode('utf-8')

# if __name__ == '__main__':
#     privatekey, publickey = generateWireguardKeys()
#
#     print(f"Private Key: {privatekey}")
#     print(f"Public Key: {publickey}")
