try:
    from PyQt5 import QtCore, QtWidgets
except ImportError:
    from PySide6 import QtCore, QtWidgets
from .app_functions import Game
from .gfx import GFX
from .other import Other
from .ui import Ui_MainWindow
from .animations import AnimationManager, LoadingAnimation
from .languages import LanguageManager


class Window(QtWidgets.QMainWindow, Game):
    def __init__(self, app_name, app_version):
        # Remove the default title bar
        super(Window, self).__init__()
        self.app_name = app_name
        self.app_version = app_version

        # Initialize language manager - V2.0.0
        self.language_manager = LanguageManager()

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Apply language to UI
        self.apply_language_to_ui()
        
        self.timer = None

        # Initialize animation system - V2.0.0 (Geçici olarak devre dışı - timer sorunları)
        # self.animation_manager = AnimationManager(self)
        # self.loading_animation = LoadingAnimation(self.ui.appstatus_text_lable, self)
        self.animation_manager = None
        self.loading_animation = None

        # Set up the GFX and Other objects
        self.GFX = GFX(self)
        self.Other = Other(self)
        
        # Initialize variables for dragging
        self.draggable = True
        self.drag_start_position = None
        
        # Başlangıç animasyonları - Widget'lar hazır olduktan sonra çalıştır
        QtCore.QTimer.singleShot(100, self.init_startup_animations)

        # Connect the button signals
        self.ui.gfx_button.clicked.connect(lambda: self.buttonClicked(self.ui.gfx_button, self.ui.gfx_page))
        self.ui.other_button.clicked.connect(lambda: self.buttonClicked(self.ui.other_button, self.ui.other_page))
        self.ui.about_button.clicked.connect(lambda: self.buttonClicked(self.ui.about_button, self.ui.about_page))
        self.ui.language_button.clicked.connect(lambda: self.buttonClicked(self.ui.language_button, self.ui.language_page))
        self.ui.close_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_btn.clicked.connect(lambda: self.setWindowState(QtCore.Qt.WindowMinimized))

    def init_startup_animations(self):
        """Başlangıç animasyonlarını başlat - V2.0.0 (Geçici olarak devre dışı)"""
        # Animasyonlar geçici olarak devre dışı - QPainter hatalarını önlemek için
        # Ana pencereyi fade in ile göster
        # self.animation_manager.fade_in(self, 800)
        
        # Butonları sırayla animasyonlu göster
        # QtCore.QTimer.singleShot(200, lambda: self.animation_manager.slide_in_from_left(self.ui.gfx_button, 600))
        # QtCore.QTimer.singleShot(400, lambda: self.animation_manager.slide_in_from_left(self.ui.other_button, 600))
        # QtCore.QTimer.singleShot(600, lambda: self.animation_manager.slide_in_from_left(self.ui.about_button, 600))
        
        # Başlık animasyonu
        # QtCore.QTimer.singleShot(800, lambda: self.animation_manager.pulse_effect(self.ui.appname_label, 1000, 1))
        
        # Welcome message
        QtCore.QTimer.singleShot(500, lambda: self.show_status_message("CRTY PUBG Mobile Tool V2.0.0 - Welcome! 🎮", 3))

    def buttonClicked(self, button, page):
        """Gelişmiş buton tıklama animasyonları - V2.0.0 (Geçici olarak devre dışı)"""
        # Buton bounce efekti (geçici olarak devre dışı)
        # self.animation_manager.bounce_effect(button, 300)
        
        # Buton durumlarını güncelle
        self.ui.gfx_button.setChecked(button == self.ui.gfx_button)
        self.ui.other_button.setChecked(button == self.ui.other_button)
        self.ui.about_button.setChecked(button == self.ui.about_button)
        self.ui.language_button.setChecked(button == self.ui.language_button)

        # Sayfa geçişi (animasyonsuz)
        self.ui.stackedWidget.setCurrentWidget(page)

    def _switch_to_page(self, page):
        """Sayfa geçişini tamamla"""
        self.ui.stackedWidget.setCurrentWidget(page)
        self.animation_manager.fade_in(page, 300)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.draggable:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.drag_start_position is not None:
            if event.buttons() & QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_start_position)
                self.drag_start_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = None

    def show_status_message(self, message, duration=5):
        """Status mesajı fonksiyonu - Thread-safe"""
        try:
            if hasattr(self, 'timer') and self.timer and self.timer.isActive():
                self.timer.stop()
                self.timer.deleteLater()
        except:
            pass
        
        self.ui.appstatus_text_lable.setText(message)
        
        if duration > 0:
            self.timer = QtCore.QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(lambda: self.ui.appstatus_text_lable.setText(""))
            self.timer.start(duration * 1000)
    
    def show_animated_status(self, message, duration=5):
        """Animasyonlu status mesajı - V2.0.0 (Animation manager devre dışı)"""
        # Animation manager devre dışı olduğu için basit mesaj göster
        self.show_status_message(message, duration)
    
    def _set_status_and_fade_in(self, message, duration):
        """Status mesajını ayarla ve fade in yap (Animation manager devre dışı)"""
        # Animation manager devre dışı olduğu için basit mesaj göster
        self.show_status_message(message, duration)
    
    def _clear_status_animated(self):
        """Status mesajını animasyonlu temizle (Animation manager devre dışı)"""
        # Animation manager devre dışı olduğu için basit temizleme
        self.ui.appstatus_text_lable.setText("")
    
    def show_loading_status(self, message="Processing..."):
        """Show loading animation status - V2.0.0 (Animation manager devre dışı)"""
        # Animation manager devre dışı olduğu için basit mesaj göster
        self.show_status_message(message, 2)
    
    def hide_loading_status(self):
        """Stop loading animation - V2.0.0 (Animation manager devre dışı)"""
        # Animation manager devre dışı olduğu için basit temizleme
        self.ui.appstatus_text_lable.setText("")
    
    def show_success_animation(self, message="Operation successful! ✅"):
        """Show success animation - V2.0.0"""
        self.hide_loading_status()
        self.show_animated_status(message, 3)
        
        # Green color effect for success
        original_style = self.ui.appstatus_text_lable.styleSheet()
        self.ui.appstatus_text_lable.setStyleSheet("color: #00ff00; font-weight: bold;")
        QtCore.QTimer.singleShot(3000, lambda: self.ui.appstatus_text_lable.setStyleSheet(original_style))
    
    def show_error_animation(self, message="Error occurred! ❌"):
        """Show error animation - V2.0.0 (Animation manager devre dışı)"""
        self.hide_loading_status()
        
        # Show error message
        self.show_animated_status(message, 4)
        
        # Red color effect for error
        original_style = self.ui.appstatus_text_lable.styleSheet()
        self.ui.appstatus_text_lable.setStyleSheet("color: #ff0000; font-weight: bold;")
        QtCore.QTimer.singleShot(4000, lambda: self.ui.appstatus_text_lable.setStyleSheet(original_style))

    def apply_language_to_ui(self):
        """UI elementlerine dil desteği uygula - V2.0.0"""
        # Ana başlık
        self.ui.appname_label.setText(f"{self.language_manager.get_text('app_title')} {self.app_version}")
        
        # Ana butonlar
        self.ui.gfx_button.setText(self.language_manager.get_text('graphics_settings'))
        self.ui.other_button.setText(self.language_manager.get_text('optimization'))
        self.ui.about_button.setText(self.language_manager.get_text('about'))
        self.ui.language_button.setText(self.language_manager.get_text('language'))
        
        # Grafik ayarları sayfası
        self.ui.graphics_label.setText(self.language_manager.get_text('graphics'))
        self.ui.fps_label.setText(self.language_manager.get_text('framerate'))
        self.ui.style_label.setText(self.language_manager.get_text('style'))
        self.ui.shadow_label.setText(self.language_manager.get_text('shadow'))
        self.ui.submit_gfx_btn.setText(self.language_manager.get_text('submit'))
        self.ui.connect_gameloop_btn.setText(self.language_manager.get_text('connect_gameloop'))
        self.ui.pubgchoose_label.setText(self.language_manager.get_text('choose_pubg_version'))
        
        # Grafik butonları
        self.ui.smooth_graphics_btn.setText(self.language_manager.get_text('smooth'))
        self.ui.balanced_graphics_btn.setText(self.language_manager.get_text('balanced'))
        self.ui.hd_graphics_btn.setText(self.language_manager.get_text('hd'))
        self.ui.hdr_graphics_btn.setText(self.language_manager.get_text('hdr'))
        self.ui.ultrahd_graphics_btn.setText(self.language_manager.get_text('ultra_hd'))
        self.ui.uhd_graphics_btn.setText(self.language_manager.get_text('uhd'))
        
        # FPS butonları
        self.ui.low_fps_btn.setText(self.language_manager.get_text('low'))
        self.ui.medium_fps_btn.setText(self.language_manager.get_text('medium'))
        self.ui.high_fps_btn.setText(self.language_manager.get_text('high'))
        self.ui.ultra_fps_btn.setText(self.language_manager.get_text('ultra'))
        self.ui.extreme_fps_btn.setText(self.language_manager.get_text('extreme'))
        self.ui.fps90_fps_btn.setText(self.language_manager.get_text('90fps'))
        self.ui.fps120_fps_btn.setText(self.language_manager.get_text('120fps'))
        
        # Gölge butonları
        self.ui.disable_shadow_btn.setText(self.language_manager.get_text('disable_shadow'))
        self.ui.enable_shadow_btn.setText(self.language_manager.get_text('enable_shadow'))

    def change_language(self, lang_code):
        """Dil değiştir ve UI'yi güncelle - V2.0.0"""
        self.language_manager.set_language(lang_code)
        self.apply_language_to_ui()
        
        # Dil değişikliği mesajı (animasyonsuz)
        restart_msg = self.language_manager.get_text('restart_for_language')
        self.show_status_message(restart_msg, 3)
        
        # 3 saniye sonra uygulamayı yeniden başlat
        QtCore.QTimer.singleShot(3000, self.restart_application)

    def restart_application(self):
        """Uygulamayı yeniden başlat - V2.0.0"""
        import sys
        import os
        
        # Animasyonsuz yeniden başlatma
        QtWidgets.QApplication.quit()
        os.execl(sys.executable, sys.executable, *sys.argv)