/**
 * ملف JavaScript لتحسين تفاعل صفحة التعلم
 */

document.addEventListener('DOMContentLoaded', function() {
    // تفعيل التمرير السلس للروابط الداخلية
    initSmoothScrolling();
    
    // تفعيل أزرار النسخ للكود
    initCodeCopyButtons();
    
    // تفعيل تسليط الضوء على الكود
    initCodeHighlighting();
    
    // إضافة شريط التقدم
    initProgressBar();
    
    // تفعيل طي وفتح الأقسام
    initCollapsibleSections();
});

/**
 * تفعيل التمرير السلس للروابط الداخلية
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // إضافة تأثير بصري للقسم المستهدف
                targetElement.style.boxShadow = '0 0 20px rgba(13, 110, 253, 0.5)';
                setTimeout(() => {
                    targetElement.style.boxShadow = '';
                }, 2000);
            }
        });
    });
}

/**
 * إضافة أزرار نسخ للكود
 */
function initCodeCopyButtons() {
    document.querySelectorAll('pre code').forEach((codeBlock, index) => {
        // إنشاء زر النسخ
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-secondary copy-code-btn';
        copyButton.innerHTML = '<i class="bi bi-clipboard"></i> نسخ';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '10px';
        copyButton.style.right = '10px';
        copyButton.style.fontSize = '0.8em';
        
        // إضافة تموضع نسبي للحاوي
        const preElement = codeBlock.parentElement;
        preElement.style.position = 'relative';
        preElement.appendChild(copyButton);
        
        // تفعيل وظيفة النسخ
        copyButton.addEventListener('click', function() {
            const textToCopy = codeBlock.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                // تغيير نص الزر مؤقتاً
                const originalHtml = copyButton.innerHTML;
                copyButton.innerHTML = '<i class="bi bi-check"></i> تم النسخ';
                copyButton.className = 'btn btn-sm btn-success copy-code-btn';
                
                setTimeout(() => {
                    copyButton.innerHTML = originalHtml;
                    copyButton.className = 'btn btn-sm btn-outline-secondary copy-code-btn';
                }, 2000);
            }).catch(err => {
                console.error('فشل في نسخ النص: ', err);
                alert('فشل في نسخ النص');
            });
        });
    });
}

/**
 * تسليط الضوء على الكود عند النقر
 */
function initCodeHighlighting() {
    document.querySelectorAll('pre code').forEach(codeBlock => {
        codeBlock.addEventListener('click', function() {
            this.style.backgroundColor = '#e3f2fd';
            this.style.transition = 'background-color 0.3s';
            setTimeout(() => {
                this.style.backgroundColor = '';
            }, 1000);
        });
    });
}

/**
 * شريط التقدم أثناء القراءة
 */
function initProgressBar() {
    // إنشاء شريط التقدم
    const progressBar = document.createElement('div');
    progressBar.style.position = 'fixed';
    progressBar.style.top = '0';
    progressBar.style.left = '0';
    progressBar.style.width = '0%';
    progressBar.style.height = '4px';
    progressBar.style.backgroundColor = '#0d6efd';
    progressBar.style.zIndex = '9999';
    progressBar.style.transition = 'width 0.3s';
    document.body.appendChild(progressBar);
    
    // تحديث شريط التقدم عند التمرير
    window.addEventListener('scroll', function() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        const scrollTop = window.pageYOffset;
        const progress = (scrollTop / documentHeight) * 100;
        progressBar.style.width = progress + '%';
    });
}

/**
 * إضافة إمكانية طي وفتح الأقسام
 */
function initCollapsibleSections() {
    document.querySelectorAll('.card-header').forEach(header => {
        // إضافة مؤشر قابلية الطي
        header.style.cursor = 'pointer';
        
        // إضافة أيقونة
        const icon = document.createElement('i');
        icon.className = 'bi bi-chevron-down float-end';
        icon.style.transition = 'transform 0.3s';
        header.appendChild(icon);
        
        // تفعيل الطي والفتح
        header.addEventListener('click', function(e) {
            // تجنب التأثير على الروابط
            if (e.target.tagName === 'A') return;
            
            const card = this.closest('.card');
            const body = card.querySelector('.card-body');
            const icon = this.querySelector('.bi-chevron-down, .bi-chevron-up');
            
            if (body.style.display === 'none') {
                // فتح القسم
                body.style.display = 'block';
                icon.className = 'bi bi-chevron-down float-end';
                icon.style.transform = 'rotate(0deg)';
            } else {
                // طي القسم
                body.style.display = 'none';
                icon.className = 'bi bi-chevron-up float-end';
                icon.style.transform = 'rotate(180deg)';
            }
        });
    });
}

/**
 * دالة للبحث في محتوى الصفحة
 */
function searchContent(query) {
    const content = document.body.innerText.toLowerCase();
    const searchTerm = query.toLowerCase();
    
    if (content.includes(searchTerm)) {
        // تسليط الضوء على النتائج
        highlightSearchResults(searchTerm);
        return true;
    }
    return false;
}

/**
 * تسليط الضوء على نتائج البحث
 */
function highlightSearchResults(term) {
    // إزالة التسليط السابق
    document.querySelectorAll('.search-highlight').forEach(el => {
        el.outerHTML = el.innerHTML;
    });
    
    // البحث وتسليط الضوء
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        if (node.nodeValue.toLowerCase().includes(term)) {
            textNodes.push(node);
        }
    }
    
    textNodes.forEach(textNode => {
        const parent = textNode.parentNode;
        const text = textNode.nodeValue;
        const regex = new RegExp(`(${term})`, 'gi');
        const highlightedText = text.replace(regex, '<mark class="search-highlight">$1</mark>');
        
        const wrapper = document.createElement('span');
        wrapper.innerHTML = highlightedText;
        parent.insertBefore(wrapper, textNode);
        parent.removeChild(textNode);
    });
}

// إضافة مفاتيح اختصار مفيدة
document.addEventListener('keydown', function(e) {
    // Ctrl + F للبحث
    if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        const searchTerm = prompt('ابحث في المحتوى:');
        if (searchTerm) {
            if (searchContent(searchTerm)) {
                alert(`تم العثور على "${searchTerm}" في الصفحة`);
            } else {
                alert(`لم يتم العثور على "${searchTerm}"`);
            }
        }
    }
    
    // مفتاح الهروب لإزالة التسليط
    if (e.key === 'Escape') {
        document.querySelectorAll('.search-highlight').forEach(el => {
            el.outerHTML = el.innerHTML;
        });
    }
});

/**
 * إضافة تأثيرات تفاعلية إضافية
 */
function addInteractiveEffects() {
    // تأثير hover للبطاقات
    document.querySelectorAll('.crypto-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // تأثير loading للأزرار
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

// تشغيل التأثيرات الإضافية
document.addEventListener('DOMContentLoaded', addInteractiveEffects);