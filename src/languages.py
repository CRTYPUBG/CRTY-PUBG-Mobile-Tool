# -*- coding: utf-8 -*-
import locale
import os
try:
    from PyQt5.QtCore import QSettings
except ImportError:
    from PySide6.QtCore import QSettings

class LanguageManager:
    def __init__(self):
        self.settings = QSettings("CRTY Apps", "CRTY PUBG Mobile Tool")
        self.current_language = self.get_system_language()
        
    def get_system_language(self):
        """Get system language with English as default"""
        saved_lang = self.settings.value("language", None)
        if saved_lang:
            return saved_lang
            
        # Default to English instead of auto-detecting system language
        return 'en'
    
    def set_language(self, lang_code):
        """Dil ayarını kaydet"""
        self.current_language = lang_code
        self.settings.setValue("language", lang_code)
    
    def get_text(self, key):
        """Seçili dile göre metni getir"""
        return LANGUAGES.get(self.current_language, LANGUAGES['en']).get(key, key)

# Dil çevirileri
LANGUAGES = {
    'tr': {
        # Ana pencere
        'app_title': 'CRTY PUBG Mobile Tool',
        'graphics_settings': 'Grafik Ayarları',
        'optimization': 'Optimizasyon',
        'about': 'Hakkında',
        
        # Grafik ayarları
        'graphics': 'Grafik',
        'framerate': 'FPS',
        'style': 'Stil',
        'shadow': 'Gölge',
        'submit': 'Uygula',
        'connect_gameloop': 'GameLoop\'a Bağlan',
        'choose_pubg_version': 'PUBG Versiyonu Seç',
        
        # Grafik seçenekleri
        'smooth': 'Pürüzsüz',
        'balanced': 'Dengeli',
        'hd': 'HD',
        'hdr': 'HDR',
        'ultra_hd': 'Ultra HD',
        'uhd': 'UHD',
        
        # FPS seçenekleri
        'low': 'Düşük',
        'medium': 'Orta',
        'high': 'Yüksek',
        'ultra': 'Ultra',
        'extreme': 'Extreme',
        '90fps': '90 FPS',
        '120fps': '120 FPS',
        
        # Stil seçenekleri
        'classic': 'Klasik',
        'colorful': 'Renkli',
        'realistic': 'Gerçekçi',
        'soft': 'Yumuşak',
        'movie': 'Film',
        
        # Gölge seçenekleri
        'disable_shadow': 'Gölge Kapalı',
        'enable_shadow': 'Gölge Açık',
        
        # Optimizasyon
        'temp_cleaner': 'Geçici Dosya Temizleyici',
        'gameloop_settings': 'GameLoop Ayarları',
        'gameloop_optimizer': 'GameLoop Optimizasyonu',
        'kill_gameloop': 'GameLoop\'u Kapat',
        'desktop_shortcut': 'Masaüstü Kısayolu',
        'dns_changer': 'DNS Değiştirici',
        'ipad_view': 'iPad Görünümü',
        
        # Durum mesajları
        'success': 'Başarılı!',
        'error': 'Hata!',
        'warning': 'Uyarı!',
        'info': 'Bilgi',
        'connecting': 'Bağlanıyor...',
        'connected': 'Bağlandı',
        'disconnected': 'Bağlantı Kesildi',
        'applying_settings': 'Ayarlar uygulanıyor...',
        'settings_applied': 'Ayarlar başarıyla uygulandı!',
        'gameloop_not_found': 'GameLoop bulunamadı!',
        'restart_required': 'Yeniden başlatma gerekli',
        
        # Hakkında
        'version': 'Versiyon',
        'author': 'Geliştirici',
        'description': 'PUBG Mobile için profesyonel optimizasyon aracı',
        
        # Dil seçenekleri
        'language': 'Dil',
        'turkish': 'Türkçe',
        'english': 'English',
        'arabic': 'العربية',
        'restart_for_language': 'Dil değişikliği için uygulamayı yeniden başlatın'
    },
    
    'en': {
        # Main window
        'app_title': 'CRTY PUBG Mobile Tool',
        'graphics_settings': 'Graphics Settings',
        'optimization': 'Optimization',
        'about': 'About',
        
        # Graphics settings
        'graphics': 'Graphics',
        'framerate': 'Framerate',
        'style': 'Style',
        'shadow': 'Shadow',
        'submit': 'Submit',
        'connect_gameloop': 'Connect to GameLoop',
        'choose_pubg_version': 'Choose PUBG Version',
        
        # Graphics options
        'smooth': 'Smooth',
        'balanced': 'Balanced',
        'hd': 'HD',
        'hdr': 'HDR',
        'ultra_hd': 'Ultra HD',
        'uhd': 'UHD',
        
        # FPS options
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'ultra': 'Ultra',
        'extreme': 'Extreme',
        '90fps': '90 FPS',
        '120fps': '120 FPS',
        
        # Style options
        'classic': 'Classic',
        'colorful': 'Colorful',
        'realistic': 'Realistic',
        'soft': 'Soft',
        'movie': 'Movie',
        
        # Shadow options
        'disable_shadow': 'Disable Shadow',
        'enable_shadow': 'Enable Shadow',
        
        # Optimization
        'temp_cleaner': 'Temp Cleaner',
        'gameloop_settings': 'GameLoop Settings',
        'gameloop_optimizer': 'GameLoop Optimizer',
        'kill_gameloop': 'Kill GameLoop',
        'desktop_shortcut': 'Desktop Shortcut',
        'dns_changer': 'DNS Changer',
        'ipad_view': 'iPad View',
        
        # Status messages
        'success': 'Success!',
        'error': 'Error!',
        'warning': 'Warning!',
        'info': 'Info',
        'connecting': 'Connecting...',
        'connected': 'Connected',
        'disconnected': 'Disconnected',
        'applying_settings': 'Applying settings...',
        'settings_applied': 'Settings applied successfully!',
        'gameloop_not_found': 'GameLoop not found!',
        'restart_required': 'Restart required',
        
        # About
        'version': 'Version',
        'author': 'Author',
        'description': 'Professional optimization tool for PUBG Mobile',
        
        # Language options
        'language': 'Language',
        'turkish': 'Türkçe',
        'english': 'English',
        'arabic': 'العربية',
        'restart_for_language': 'Please restart the application for language change'
    },
    
    'ar': {
        # النافذة الرئيسية
        'app_title': 'أداة CRTY PUBG Mobile',
        'graphics_settings': 'إعدادات الرسومات',
        'optimization': 'التحسين',
        'about': 'حول',
        
        # إعدادات الرسومات
        'graphics': 'الرسومات',
        'framerate': 'معدل الإطارات',
        'style': 'النمط',
        'shadow': 'الظل',
        'submit': 'تطبيق',
        'connect_gameloop': 'الاتصال بـ GameLoop',
        'choose_pubg_version': 'اختر إصدار PUBG',
        
        # خيارات الرسومات
        'smooth': 'سلس',
        'balanced': 'متوازن',
        'hd': 'عالي الدقة',
        'hdr': 'HDR',
        'ultra_hd': 'فائق الدقة',
        'uhd': 'UHD',
        
        # خيارات FPS
        'low': 'منخفض',
        'medium': 'متوسط',
        'high': 'عالي',
        'ultra': 'فائق',
        'extreme': 'متطرف',
        '90fps': '90 إطار',
        '120fps': '120 إطار',
        
        # خيارات النمط
        'classic': 'كلاسيكي',
        'colorful': 'ملون',
        'realistic': 'واقعي',
        'soft': 'ناعم',
        'movie': 'فيلم',
        
        # خيارات الظل
        'disable_shadow': 'إيقاف الظل',
        'enable_shadow': 'تشغيل الظل',
        
        # التحسين
        'temp_cleaner': 'منظف الملفات المؤقتة',
        'gameloop_settings': 'إعدادات GameLoop',
        'gameloop_optimizer': 'محسن GameLoop',
        'kill_gameloop': 'إغلاق GameLoop',
        'desktop_shortcut': 'اختصار سطح المكتب',
        'dns_changer': 'مغير DNS',
        'ipad_view': 'عرض iPad',
        
        # رسائل الحالة
        'success': 'نجح!',
        'error': 'خطأ!',
        'warning': 'تحذير!',
        'info': 'معلومات',
        'connecting': 'جاري الاتصال...',
        'connected': 'متصل',
        'disconnected': 'منقطع',
        'applying_settings': 'جاري تطبيق الإعدادات...',
        'settings_applied': 'تم تطبيق الإعدادات بنجاح!',
        'gameloop_not_found': 'لم يتم العثور على GameLoop!',
        'restart_required': 'إعادة التشغيل مطلوبة',
        
        # حول
        'version': 'الإصدار',
        'author': 'المطور',
        'description': 'أداة تحسين احترافية لـ PUBG Mobile',
        
        # خيارات اللغة
        'language': 'اللغة',
        'turkish': 'Türkçe',
        'english': 'English',
        'arabic': 'العربية',
        'restart_for_language': 'يرجى إعادة تشغيل التطبيق لتغيير اللغة'
    }
}