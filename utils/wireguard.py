from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from base64 import b64encode


def generate_wireguard_keys():
    """
    生成 WireGuard 密钥对
    :return:  Base64 编码的私钥和公钥
    """
    # 生成私钥
    private_key = x25519.X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 使用私钥生成公钥
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # 返回 Base64 编码的私钥和公钥
    return b64encode(private_bytes).decode('utf-8'), b64encode(public_bytes).decode('utf-8')


if __name__ == '__main__':
    privatekey, publickey = generate_wireguard_keys()

    print(f"Private Key: {privatekey}")
    print(f"Public Key: {publickey}")
