"""
تنفيذ خوارزميات التجزئة (Hash) بدون استخدام مكتبات خارجية
"""

def sha1(message):
    """
    تنفيذ بسيط لخوارزمية SHA-1
    """
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # ثوابت SHA-1
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # تحضير الرسالة
    ml = len(message) * 8
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += ml.to_bytes(8, byteorder='big')
    
    # معالجة الرسالة في كتل 512 بت
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = [0] * 80
        
        # تقسيم الكتلة إلى 16 كلمة 32 بت
        for j in range(16):
            w[j] = int.from_bytes(chunk[j*4:j*4+4], byteorder='big')
        
        # توسيع 16 كلمة إلى 80 كلمة
        for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
        
        # تهيئة قيم الجولة
        a, b, c, d, e = h0, h1, h2, h3, h4
        
        # الجولات الرئيسية
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = (_left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff
            e = d
            d = c
            c = _left_rotate(b, 30)
            b = a
            a = temp
        
        # إضافة نتائج هذه الكتلة
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    
    # تجميع النتيجة النهائية
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def _left_rotate(n, b):
    """دوران بتات إلى اليسار"""
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def md5(message):
    """
    تنفيذ بسيط لخوارزمية MD5
    """
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # ثوابت MD5
    r = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    
    # جدول البيانات المحسوب مسبقًا
    k = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    ]
    
    # تهيئة قيم البداية
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476
    
    # تحضير الرسالة
    ml = len(message) * 8
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += ml.to_bytes(8, byteorder='little')
    
    # معالجة الرسالة في كتل 512 بت
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        
        # تقسيم الكتلة إلى 16 كلمة 32 بت
        m = [0] * 16
        for j in range(16):
            m[j] = int.from_bytes(chunk[j*4:j*4+4], byteorder='little')
        
        # تهيئة قيم الجولة
        a, b, c, d = a0, b0, c0, d0
        
        # الجولات الرئيسية
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16
            
            temp = d
            d = c
            c = b
            b = (b + _left_rotate((a + f + k[j] + m[g]) & 0xffffffff, r[j])) & 0xffffffff
            a = temp
        
        # إضافة نتائج هذه الكتلة
        a0 = (a0 + a) & 0xffffffff
        b0 = (b0 + b) & 0xffffffff
        c0 = (c0 + c) & 0xffffffff
        d0 = (d0 + d) & 0xffffffff
    
    # تجميع النتيجة النهائية
    result = a0.to_bytes(4, byteorder='little') + \
             b0.to_bytes(4, byteorder='little') + \
             c0.to_bytes(4, byteorder='little') + \
             d0.to_bytes(4, byteorder='little')
    
    return ''.join('%02x' % b for b in result)

# دالة تجزئة بسيطة للتعليم
def simple_hash(message, bits=32):
    """
    دالة تجزئة بسيطة للأغراض التعليمية فقط
    لا تستخدم هذه الدالة في التطبيقات الحقيقية
    """
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # قيمة أولية
    h = 0x5A3C
    
    # معالجة كل بايت في الرسالة
    for byte in message:
        h = ((h << 5) + h) ^ byte
        h &= ((1 << bits) - 1)  # الاحتفاظ بعدد البتات المطلوب
    
    # تحويل النتيجة إلى سلسلة سداسية عشرية
    hex_length = bits // 4
    format_str = '%0' + str(hex_length) + 'x'
    return format_str % h

# مثال على الاستخدام
if __name__ == "__main__":
    test_message = "Hello, World!"
    print(f"الرسالة: {test_message}")
    print(f"SHA-1: {sha1(test_message)}")
    print(f"MD5: {md5(test_message)}")
    print(f"Simple Hash: {simple_hash(test_message)}")