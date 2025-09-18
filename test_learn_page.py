"""
اختبار بسيط للتأكد من أن صفحة التعلم تعمل بشكل صحيح
"""
import sys
import os

# إضافة مجلد المشروع إلى المسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_learn_page():
    """اختبار أن صفحة التعلم تعمل وتعيد المحتوى المناسب"""
    with app.test_client() as client:
        # اختبار الوصول للصفحة
        response = client.get('/learn')
        
        # التحقق من أن الاستجابة ناجحة
        assert response.status_code == 200
        
        # التحقق من وجود عناصر مهمة في المحتوى
        content = response.data.decode('utf-8')
        
        # التحقق من العنوان الرئيسي
        assert 'الدليل الشامل لخوارزميات التشفير' in content
        
        # التحقق من وجود أقسام AES
        assert 'خوارزمية AES' in content
        assert 'SubBytes' in content
        assert 'ShiftRows' in content
        assert 'MixColumns' in content
        assert 'AddRoundKey' in content
        
        # التحقق من وجود أقسام RSA
        assert 'خوارزمية RSA' in content
        assert 'توليد المفاتيح' in content
        assert 'Miller-Rabin' in content
        
        # التحقق من وجود أقسام Hash
        assert 'دوال التجزئة' in content
        assert 'SHA-1' in content
        assert 'MD5' in content
        
        # التحقق من وجود الكود
        assert 'def encrypt(self, plaintext):' in content
        assert 'def __sub_bytes(self, s):' in content
        
        print("✅ جميع الاختبارات نجحت!")
        print("✅ صفحة الشرح تعمل بشكل صحيح")
        print("✅ جميع العناصر المطلوبة موجودة")

def test_navigation():
    """اختبار أن رابط التنقل موجود في الصفحة الرئيسية"""
    with app.test_client() as client:
        response = client.get('/')
        content = response.data.decode('utf-8')
        
        # التحقق من وجود رابط صفحة التعلم
        assert '/learn' in content
        assert 'شرح الخوارزميات' in content
        
        print("✅ رابط التنقل موجود في الصفحة الرئيسية")

if __name__ == '__main__':
    print("🧪 بدء اختبار صفحة التعلم...")
    
    try:
        test_learn_page()
        test_navigation()
        print("\n🎉 جميع الاختبارات نجحت! صفحة الشرح جاهزة للاستخدام.")
        
    except AssertionError as e:
        print(f"❌ فشل الاختبار: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        sys.exit(1)