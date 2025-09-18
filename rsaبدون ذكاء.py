import random
import math

def is_prime(n, k=5):
    # نتأكد من الأعداد الصغيرة أولاً
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # نحسب d و r بحيث n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # نكرر اختبار ميلر-رابين k مرات
    for _ in range(k):
        if not miller_test(d, n, r):
            return False
    
    return True

def miller_test(d, n, r):
    # نختار عدد عشوائي بين 2 و n-2
    a = 2 + random.randint(1, n - 4)
    
    # نحسب a^d mod n
    x = pow(a, d, n)
    
    # إذا كان x = 1 أو x = n-1، فالعدد أولي محتمل
    if x == 1 or x == n - 1:
        return True
    
    # نكرر عملية التربيع r-1 مرات
    for _ in range(r - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
        if x == 1:
            return False
    
    return False

def generate_prime(bits):
    # نولد أعداد أولية حتى نجد واحد مناسب
    while True:
        # نولد عدد عشوائي بعدد البتات المطلوب
        num = random.getrandbits(bits)
        
        # نتأكد أن العدد فردي وأن البت الأعلى = 1
        num |= 1
        num |= (1 << (bits - 1))
        
        # نختبر إذا كان أولي
        if is_prime(num):
            return num

def gcd(a, b):
    # خوارزمية إقليدس لإيجاد القاسم المشترك الأكبر
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    # خوارزمية إقليدس الممتدة لإيجاد المعكوس الضربي
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return g, x, y
    
    g, x, y = extended_gcd(e, phi)
    
    if g != 1:
        raise ValueError("لا يوجد معكوس ضربي - e و phi ليسا أوليين نسبياً")
    else:
        # نعيد النتيجة موجبة
        return x % phi

class RSA:
    def __init__(self, key_size=512):
        self.key_size = key_size
        self.generate_keys()
    
    def generate_keys(self):
        # نولد عددين أوليين كبيرين
        p = generate_prime(self.key_size // 2)
        q = generate_prime(self.key_size // 2)
        
        # نحسب n و phi
        self.n = p * q
        phi = (p - 1) * (q - 1)
        
        # نختار e (عادة 65537)
        self.e = 65537
        
        # إذا لم يكن e مناسباً، نبحث عن آخر
        while gcd(self.e, phi) != 1:
            self.e += 2
        
        # نحسب المعكوس الضربي ل e mod phi
        self.d = mod_inverse(self.e, phi)
        
        # نخزن المفاتيح
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)
    
    def encrypt(self, message):
        e, n = self.public_key
        
        # إذا كانت الرسالة نصاً، نحولها إلى بايتات
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # إذا كانت الرسالة بايتات، نحولها إلى عدد
        if isinstance(message, bytes):
            message = int.from_bytes(message, byteorder='big')
        
        # نطبق عملية التشفير: ciphertext = message^e mod n
        ciphertext = pow(message, e, n)
        return ciphertext
    
    def decrypt(self, ciphertext):
        d, n = self.private_key
        
        # نطبق عملية فك التشفير: message = ciphertext^d mod n
        message = pow(ciphertext, d, n)
        
        # نحاول تحويل العدد إلى نص
        try:
            byte_length = (message.bit_length() + 7) // 8
            decrypted_bytes = message.to_bytes(byte_length, byteorder='big')
            return decrypted_bytes.decode('utf-8', errors='ignore')
        except:
            # إذا فشل التحويل، نعيد العدد كنص
            return str(message)
    
    def get_public_key(self):
        return self.public_key
    
    def get_private_key(self):
        return self.private_key

# مثال على الاستخدام
if __name__ == "__main__":
    # ننشئ كائن RSA
    rsa = RSA(key_size=512)
    
    # الرسالة التي نريد تشفيرها
    message = "Hello RSA"
    
    # نشفر الرسالة
    encrypted = rsa.encrypt(message)
    
    # نفك التشفير
    decrypted = rsa.decrypt(encrypted)
    
    # نعرض النتائج
    print(f"الرسالة الأصلية: {message}")
    print(f"الرسالة المشفرة: {encrypted}")
    print(f"الرسالة بعد فك التشفير: {decrypted}")
    
    # نعرض المفاتيح أيضاً
    print(f"المفتاح العام: {rsa.get_public_key()}")
    print(f"المفتاح الخاص: {rsa.get_private_key()}")
