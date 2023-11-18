import hashlib

class NumberEncryptor:
    def __init__(self):
        
        pass

    def encrypt_number(self, number):
        # 숫자를 문자열로 변환하여 바이트로 인코딩
        number_str = str(number)
        number_bytes = number_str.encode('utf-8')

        # SHA-256 해시 계산
        sha256_hash = hashlib.sha256(number_bytes).hexdigest()

        return sha256_hash
