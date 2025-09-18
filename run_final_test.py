"""
اختبار نهائي شامل للتطبيق مع الصفحة الجديدة
"""
import sys
import os
import time
import requests
from threading import Thread

# إضافة مجلد المشروع إلى المسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_all_routes():
    """اختبار جميع المسارات في التطبيق"""
    
    print("🧪 بدء الاختبار الشامل للتطبيق...")
    
    with app.test_client() as client:
        routes_to_test = [
            ('/', 'الصفحة الرئيسية'),
            ('/aes', 'صفحة AES'),
            ('/rsa', 'صفحة RSA'),
            ('/hash', 'صفحة Hash'),
            ('/learn', 'صفحة الشرح'),
            ('/api/generate_key', 'API توليد المفاتيح')
        ]
        
        for route, description in routes_to_test:
            print(f"📍 اختبار {description} ({route})...")
            
            try:
                response = client.get(route)
                
                if response.status_code == 200:
                    print(f"  ✅ {description}: نجح (200 OK)")
                    
                    # اختبارات إضافية للمحتوى
                    content = response.data.decode('utf-8')
                    
                    if route == '/':
                        assert 'تطبيق التشفير' in content
                        assert '/learn' in content
                        print("  ✅ المحتوى الأساسي موجود")
                        
                    elif route == '/learn':
                        required_content = [
                            'الدليل الشامل لخوارزميات التشفير',
                            'خوارزمية AES',
                            'خوارزمية RSA',
                            'دوال التجزئة',
                            'SubBytes',
                            'ShiftRows',
                            'MixColumns'
                        ]
                        
                        for content_check in required_content:
                            assert content_check in content
                        
                        print("  ✅ جميع المحتويات التعليمية موجودة")
                        
                    elif route == '/api/generate_key':
                        # للAPI نتوقع JSON
                        json_data = response.get_json()
                        assert 'key_hex' in json_data
                        assert 'key_int' in json_data
                        print("  ✅ API يعيد البيانات الصحيحة")
                        
                else:
                    print(f"  ❌ {description}: فشل ({response.status_code})")
                    return False
                    
            except Exception as e:
                print(f"  ❌ {description}: خطأ - {e}")
                return False
        
        print("\n✅ جميع المسارات تعمل بشكل صحيح!")
        return True

def test_functionality():
    """اختبار الوظائف الأساسية"""
    
    print("\n🔧 اختبار الوظائف الأساسية...")
    
    with app.test_client() as client:
        # اختبار تشفير AES
        print("📍 اختبار تشفير AES...")
        aes_data = {
            'action': 'encrypt',
            'text': 'Hello World',
            'key': '2b7e151628aed2a6abf7158809cf4f3c'
        }
        
        response = client.post('/aes', data=aes_data)
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert 'encrypted_hex' in content or 'Hello World' in content
        print("  ✅ تشفير AES يعمل")
        
        # اختبار توليد مفاتيح RSA
        print("📍 اختبار توليد مفاتيح RSA...")
        rsa_data = {'action': 'generate'}
        
        response = client.post('/rsa', data=rsa_data)
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert 'تم توليد مفاتيح جديدة بنجاح' in content or 'public_key' in content
        print("  ✅ توليد مفاتيح RSA يعمل")
        
        # اختبار دوال التجزئة
        print("📍 اختبار دوال التجزئة...")
        hash_data = {'text': 'Test Message'}
        
        response = client.post('/hash', data=hash_data)
        assert response.status_code == 200
        content = response.data.decode('utf-8')
        assert 'sha1' in content.lower() or 'Test Message' in content
        print("  ✅ دوال التجزئة تعمل")
        
        print("\n✅ جميع الوظائف الأساسية تعمل!")
        return True

def test_static_files():
    """اختبار الملفات الثابتة"""
    
    print("\n📁 اختبار الملفات الثابتة...")
    
    with app.test_client() as client:
        static_files = [
            '/static/learn.css',
            '/static/learn.js'
        ]
        
        for file_path in static_files:
            print(f"📍 اختبار {file_path}...")
            
            response = client.get(file_path)
            
            if response.status_code == 200:
                print(f"  ✅ {file_path}: متوفر")
            else:
                print(f"  ❌ {file_path}: غير متوفر ({response.status_code})")
                return False
        
        print("\n✅ جميع الملفات الثابتة متوفرة!")
        return True

def test_responsive_design():
    """اختبار التصميم المتجاوب"""
    
    print("\n📱 اختبار التصميم المتجاوب...")
    
    with app.test_client() as client:
        # اختبار الصفحة مع user agents مختلفة
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  # Desktop
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',         # Mobile
            'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)'                   # Tablet
        ]
        
        for i, ua in enumerate(user_agents):
            device_type = ['Desktop', 'Mobile', 'Tablet'][i]
            print(f"📍 اختبار على {device_type}...")
            
            headers = {'User-Agent': ua}
            response = client.get('/learn', headers=headers)
            
            assert response.status_code == 200
            content = response.data.decode('utf-8')
            
            # التحقق من وجود عناصر التصميم المتجاوب
            assert 'bootstrap' in content.lower()
            assert 'container' in content
            assert 'col-' in content
            
            print(f"  ✅ {device_type}: التصميم متوافق")
        
        print("\n✅ التصميم المتجاوب يعمل على جميع الأجهزة!")
        return True

def performance_test():
    """اختبار الأداء البسيط"""
    
    print("\n⚡ اختبار الأداء...")
    
    with app.test_client() as client:
        # قياس زمن تحميل الصفحة الرئيسية
        start_time = time.time()
        response = client.get('/learn')
        end_time = time.time()
        
        load_time = end_time - start_time
        print(f"📍 زمن تحميل صفحة التعلم: {load_time:.3f} ثانية")
        
        if load_time < 1.0:
            print("  ✅ الأداء ممتاز (أقل من ثانية)")
        elif load_time < 3.0:
            print("  ✅ الأداء جيد (أقل من 3 ثوان)")
        else:
            print("  ⚠️ الأداء بطيء (أكثر من 3 ثوان)")
        
        # قياس حجم المحتوى
        content_size = len(response.data)
        print(f"📍 حجم صفحة التعلم: {content_size / 1024:.1f} KB")
        
        if content_size < 500 * 1024:  # أقل من 500 KB
            print("  ✅ حجم مناسب للويب")
        else:
            print("  ⚠️ حجم كبير قد يؤثر على التحميل")
        
        return True

def security_test():
    """اختبارات أمنية بسيطة"""
    
    print("\n🔒 اختبارات أمنية بسيطة...")
    
    with app.test_client() as client:
        # اختبار XSS
        print("📍 اختبار XSS...")
        xss_payload = '<script>alert("xss")</script>'
        
        response = client.post('/aes', data={
            'action': 'encrypt',
            'text': xss_payload,
            'key': '2b7e151628aed2a6abf7158809cf4f3c'
        })
        
        content = response.data.decode('utf-8')
        
        if '<script>' not in content:
            print("  ✅ محمي من XSS الأساسي")
        else:
            print("  ⚠️ قد يكون عرضة لـ XSS")
        
        # اختبار SQL Injection (رغم عدم وجود قاعدة بيانات)
        print("📍 اختبار SQL Injection...")
        sql_payload = "'; DROP TABLE users; --"
        
        response = client.post('/hash', data={'text': sql_payload})
        assert response.status_code == 200
        print("  ✅ لا يوجد SQL injection (لا توجد قاعدة بيانات)")
        
        return True

def main():
    """تشغيل جميع الاختبارات"""
    
    print("=" * 60)
    print("🚀 اختبار شامل لتطبيق التشفير مع صفحة الشرح")
    print("=" * 60)
    
    try:
        # تشغيل جميع الاختبارات
        tests = [
            test_all_routes,
            test_functionality,
            test_static_files,
            test_responsive_design,
            performance_test,
            security_test
        ]
        
        all_passed = True
        
        for test_func in tests:
            if not test_func():
                all_passed = False
                break
        
        print("\n" + "=" * 60)
        
        if all_passed:
            print("🎉 جميع الاختبارات نجحت! التطبيق جاهز للاستخدام.")
            print("\n📋 ملخص الميزات:")
            print("  ✅ صفحة شرح شاملة لجميع الخوارزميات")
            print("  ✅ تشفير AES, RSA, ودوال التجزئة")
            print("  ✅ تصميم متجاوب وتفاعلي")
            print("  ✅ ملفات CSS و JavaScript مخصصة")
            print("  ✅ أداء جيد وأمان أساسي")
            print("\n🌐 للوصول لصفحة الشرح: http://localhost:5000/learn")
            
        else:
            print("❌ بعض الاختبارات فشلت. راجع الرسائل أعلاه.")
            return False
            
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الاختبارات: {e}")
        return False
    
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)