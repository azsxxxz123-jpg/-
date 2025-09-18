
import random
import math

def is_prime(n, k=5):
    
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    for _ in range(k):
        if not miller_test(d, n):
            return False
    return True

def miller_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
    
    if x == 1 or x == n - 1:
        return True
    
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        
        if x == 1:
            return False
        if x == n - 1:
            return True
    
    return False

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        num |= 1
        num |= (1 << (bits - 1))
        if is_prime(num):
            return num

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x
    
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("المعكوس التبادلي غير موجود")
    else:
        return x % phi

class RSA:
    def __init__(self, key_size=512):
        self.key_size = key_size
        self.generate_keys()
    
    def generate_keys(self):
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)
        
        self.n = p * q
        phi = (p - 1) * (q - 1)
        
        self.e = 65537  
        while gcd(self.e, phi) != 1:
            self.e += 2
        
        self.d = mod_inverse(self.e, phi)
        
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)
    
    def encrypt(self, message):
        e, n = self.public_key
        
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        if isinstance(message, bytes):
            message = int.from_bytes(message, byteorder='big')
        
        ciphertext = pow(message, e, n)
        return ciphertext
    
    def decrypt(self, ciphertext):
        d, n = self.private_key
        
        message = pow(ciphertext, d, n)
        
        try:
            byte_length = (message.bit_length() + 7) // 8
            decrypted_bytes = message.to_bytes(byte_length, byteorder='big')
            return decrypted_bytes.decode('utf-8', errors='ignore')
        except:
            return str(message)
    
    def get_public_key(self):
        return self.public_key
    
    def get_private_key(self):
        return self.private_key

if __name__ == "__main__":
    rsa = RSA(key_size=512) 
    message = "Hello RSA"
    
    encrypted = rsa.encrypt(message)
    decrypted = rsa.decrypt(encrypted)
    
    print(f"الرسالة الأصلية: {message}")
    print(f"الرسالة المشفرة: {encrypted}")
    print(f"الرسالة بعد فك التشفير: {decrypted}")
