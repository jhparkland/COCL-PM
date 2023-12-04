import hashlib

class NumberEncryptor:
    def __init__(self):
        pass

    def encrypt_number(self, input_data):
        if isinstance(input_data, tuple):
            input_data = ''.join(map(str, input_data))

        input_bytes = input_data.encode('utf-8')

        sha256_hash = hashlib.sha256(input_bytes).hexdigest()

        return sha256_hash
