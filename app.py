from flask import Flask, render_template, request, jsonify
import base64
import binascii
import random

# استيراد خوارزميات التشفير
from crypto.aes import AES
from crypto.rsa_impl import RSA
from crypto.hash_impl import sha1, md5, simple_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # قم بتغيير هذا في الإنتاج

# إنشاء كائنات التشفير
rsa = RSA(key_size=512)  # استخدام مفاتيح أصغر للعرض

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/aes', methods=['GET', 'POST'])
def aes_page():
    """صفحة تشفير AES"""
    result = None
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            text = request.form.get('text', '')
            key_hex = request.form.get('key', '2b7e151628aed2a6abf7158809cf4f3c')
            
            # تحويل المفتاح إلى صيغة عددية
            key = int(key_hex, 16)
            
            # تحويل النص إلى صيغة مناسبة
            if action == 'encrypt':
                # تحويل النص إلى عدد صحيح
                padded_text = text.ljust(16)  # تبطين النص ليصبح 16 بايت
                plaintext = int.from_bytes(padded_text.encode('utf-8'), byteorder='big')
                
                # إنشاء كائن AES وتشفير النص
                aes = AES(key)
                encrypted = aes.encrypt(plaintext)
                
                result = {
                    'original': text,
                    'encrypted_hex': hex(encrypted),
                    'encrypted_base64': base64.b64encode(encrypted.to_bytes((encrypted.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')
                }
            
            elif action == 'decrypt':
                try:
                    # محاولة تفسير النص كقيمة سداسية عشرية
                    if text.startswith('0x'):
                        ciphertext = int(text, 16)
                    else:
                        # محاولة تفسير النص كقيمة Base64
                        ciphertext = int.from_bytes(base64.b64decode(text), byteorder='big')
                    
                    # فك تشفير النص
                    aes = AES(key)
                    decrypted = aes.decrypt(ciphertext)
                    
                    # تحويل النتيجة إلى نص
                    decrypted_text = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big').decode('utf-8', errors='ignore').rstrip('\x00')
                    
                    result = {
                        'original': text,
                        'decrypted': decrypted_text
                    }
                except Exception as e:
                    result = {
                        'error': f'خطأ في فك التشفير: {str(e)}'
                    }
        
        except Exception as e:
            result = {
                'error': f'خطأ: {str(e)}'
            }
    
    return render_template('aes.html', result=result)

@app.route('/rsa', methods=['GET', 'POST'])
def rsa_page():
    """صفحة تشفير RSA"""
    global rsa
    result = None
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            text = request.form.get('text', '')
            
            if action == 'encrypt':
                # تشفير النص باستخدام RSA
                encrypted = rsa.encrypt(text)
                
                result = {
                    'original': text,
                    'encrypted': str(encrypted),
                    'public_key': str(rsa.get_public_key())
                }
            
            elif action == 'decrypt':
                try:
                    # فك تشفير النص
                    ciphertext = int(text)
                    decrypted = rsa.decrypt(ciphertext)
                    
                    result = {
                        'original': text,
                        'decrypted': decrypted,
                        'private_key': str(rsa.get_private_key())
                    }
                except Exception as e:
                    result = {
                        'error': f'خطأ في فك التشفير: {str(e)}'
                    }
            
            elif action == 'generate':
                # توليد مفاتيح جديدة
                rsa = RSA(key_size=512)
                
                result = {
                    'message': 'تم توليد مفاتيح جديدة بنجاح',
                    'public_key': str(rsa.get_public_key()),
                    'private_key': str(rsa.get_private_key())
                }
        
        except Exception as e:
            result = {
                'error': f'خطأ: {str(e)}'
            }
    
    return render_template('rsa.html', result=result, 
                          public_key=str(rsa.get_public_key()),
                          private_key=str(rsa.get_private_key()))

@app.route('/hash', methods=['GET', 'POST'])
def hash_page():
    """صفحة دوال التجزئة"""
    result = None
    if request.method == 'POST':
        try:
            text = request.form.get('text', '')
            
            # حساب قيم التجزئة المختلفة
            sha1_hash = sha1(text)
            md5_hash = md5(text)
            simple_hash_16 = simple_hash(text, bits=16)
            simple_hash_32 = simple_hash(text, bits=32)
            
            result = {
                'original': text,
                'sha1': sha1_hash,
                'md5': md5_hash,
                'simple_hash_16': simple_hash_16,
                'simple_hash_32': simple_hash_32
            }
        
        except Exception as e:
            result = {
                'error': f'خطأ: {str(e)}'
            }
    
    return render_template('hash.html', result=result)

@app.route('/learn', methods=['GET'])
def learn_page():
    """صفحة الشرح المفصل للخوارزميات"""
    return render_template('learn.html')

@app.route('/api/generate_key', methods=['GET'])
def generate_key():
    """توليد مفتاح AES عشوائي"""
    key = random.getrandbits(128)
    return jsonify({
        'key_hex': hex(key)[2:],
        'key_int': key
    })

if __name__ == '__main__':
    app.run(debug=True)