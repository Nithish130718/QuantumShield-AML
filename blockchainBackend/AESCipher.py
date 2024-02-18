import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_bytes = cipher.encrypt(raw.encode())
        return base64.b64encode(iv + encrypted_bytes)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]

    def encrypt_bytes32(self, raw):
        enc = self.encrypt(raw)
        enc_b64 = base64.b64decode(enc)
        enc_hex = enc_b64.hex()
        enc_bytes32 = "0x" + enc_hex
        return enc_bytes32

    def decrypt_bytes32(self, enc_bytes32):
        # Convert bytes32 hash back to bytes
        enc = bytes.fromhex(
            enc_bytes32[2:]
        )  # Skip the '00' prefix and convert hex to bytes
        # Base64 decode the input
        enc_b64 = base64.b64encode(enc)
        # Decrypt the bytes using AESCipher
        decrypted_bytes = self.decrypt(enc_b64)
        return decrypted_bytes


# c = AESCipher("admin@123")
# print(c.key)
# inp = "Hello world!"

# enc = c.encrypt_bytes32(inp)
# print(enc)

# dec = c.decrypt_bytes32(enc)
# print(dec)