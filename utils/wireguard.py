"""

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.

"""
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
