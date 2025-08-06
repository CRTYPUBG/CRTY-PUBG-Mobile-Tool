import ping3
try:
    from PyQt5.QtCore import QThread, pyqtSignal, QObject
except ImportError:
    from PySide6.QtCore import QThread, Signal as pyqtSignal, QObject
import re
from . import setup_logger


class IPADWorkerThread(QThread):
    task_completed = pyqtSignal()

    def __init__(self, window, ui, gfx):
        super(IPADWorkerThread, self).__init__()
        self.app = window
        self.ui = ui
        self.gfx = gfx

    def run(self):
        width, height = self.extract_dimensions(self.ui.ipad_dropdown.currentText())
        self.app.ipad_settings(width, height)
        self.task_completed.emit()

    @staticmethod
    def extract_dimensions(string):
        pattern = r'(\d+)\s*x\s*(\d+)'
        match = re.search(pattern, string)

        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
        else:
            return None


class Other(QObject):
    def __init__(self, window):
        super(Other, self).__init__()
        from .ui import Ui_MainWindow
        from .ui_functions import Window
        self.ui: Ui_MainWindow = window.ui
        self.app: Window = window
        self.dns_servers = {
            "Google DNS - 8.8.8.8": ['8.8.8.8', '8.8.4.4'],
            "Cloudflare DNS - 1.1.1.1": ['1.1.1.1', '1.0.0.1'],
            "Quad9 DNS - 9.9.9.9": ['9.9.9.9', '149.112.112.112'],
            "Cisco Umbrella - 208.67.222.222": ['208.67.222.222', '208.67.220.220'],
            "Yandex DNS - 77.88.8.1": ['77.88.8.1', '77.88.8.8']
        }
        
        # Dil seçenekleri
        self.languages = {
            'tr': 'Türkçe 🇹🇷',
            'en': 'English 🇺🇸',
            'ar': 'العربية 🇸🇦'
        }
        self.function()
        self.logger = setup_logger('error_logger', 'error.log')

    def function(self):
        ui = self.ui

        ui.tempcleaner_other_btn.clicked.connect(self.temp_cleaner_button_click)
        ui.glsmartsettings_other_btn.clicked.connect(self.gameloop_smart_settings_button_click)
        ui.gloptimizer_other_btn.clicked.connect(self.gameloop_optimizer_button_click)
        ui.all_other_btn.clicked.connect(self.all_recommended_button_click)
        ui.forceclosegl_other_btn.clicked.connect(self.kill_gameloop_processes_button_click)
        ui.shortcut_other_btn.clicked.connect(self.shortcut_submit_button_click)
        ui.dns_dropdown.currentTextChanged.connect(self.dns_dropdown)
        ui.dns_other_btn.clicked.connect(self.dns_submit_button_click)
        ui.ipad_other_btn.clicked.connect(self.ipad_submit_button_click)
        ui.ipad_rest_btn.clicked.connect(self.ipad_reset_button_click)
        
        # Dil değiştirme butonları - V2.0.0
        self.setup_language_buttons()

        ui.ipad_code.hide()
        ui.ipad_code_label.hide()

        _width = self.app.settings.value("VMResWidth")
        _height = self.app.settings.value("VMResHeight")

        if _width is None or _height is None:
            ui.ipad_rest_btn.hide()

    def temp_cleaner_button_click(self, e):
        """ Temp Cleaner Button On Click Function - V2.0.0 """
        try:
            self.app.show_status_message("Cleaning system...", 2)
            self.app.temp_cleaner()
            self.app.show_status_message("System performance improved! 🚀", 3)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            self.app.show_status_message("Error occurred! Check error.log for details.", 4)

    def gameloop_smart_settings_button_click(self, e):
        """ Gameloop Smart Settings Button On Click Function - V2.0.0 """
        try:
            self.app.show_status_message("Applying smart settings...", 2)
            self.app.gameloop_settings()
            self.app.show_status_message("Smart settings applied successfully! 🎯", 3)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            self.app.show_status_message("Error occurred! Check error.log for details.", 4)
    def gameloop_optimizer_button_click(self, e):
        """ Gameloop Optimizer Button On Click Function - V2.0.0 """
        try:
            self.app.show_status_message("Optimizing GameLoop...", 2)
            self.app.add_to_windows_defender_exclusion()
            self.app.optimize_gameloop_registry()
            self.app.optimize_for_nvidia()
            self.app.show_status_message("GameLoop optimization completed! ⚡", 3)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            self.app.show_status_message("Error occurred! Check error.log for details.", 4)
    def all_recommended_button_click(self, e):
        """ All Recommended Button On Click Function - V2.0.0 """
        try:
            self.app.show_status_message("Applying all recommended settings...", 2)
            self.app.gameloop_settings()
            self.app.add_to_windows_defender_exclusion()
            self.app.optimize_gameloop_registry()
            self.app.optimize_for_nvidia()
            self.app.temp_cleaner()
            self.app.show_status_message("All recommended settings applied successfully! 🌟", 3)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            self.app.show_status_message("Error occurred! Check error.log for details.", 4)

    def kill_gameloop_processes_button_click(self, e):
        """Terminates Gameloop processes when the button is clicked - V2.0.0"""
        self.app.show_status_message("Terminating GameLoop processes...", 2)
        
        if self.app.kill_gameloop():
            message = "All GameLoop processes terminated! 🔴"
            self.app.show_status_message(message, 3)
        else:
            message = "No processes found to terminate! ℹ️"
            self.app.show_status_message(message, 3)

    def shortcut_submit_button_click(self, e):
        """ Shortcut Submit Button On Click Function - V2.0.0 """
        version_value = self.ui.shortcut_dropdown.currentText()
        self.app.show_status_message("Creating shortcut...", 2)
        self.app.gen_game_icon(version_value)
        self.app.show_status_message("Shortcut created successfully! 🔗", 3)

    def dns_submit_button_click(self, e):
        """ DNS Submit Button On Click Function - V2.0.0 """
        dns_key = self.ui.dns_dropdown.currentText()
        dns_server = self.dns_servers.get(dns_key)
        
        self.app.show_status_message("Changing DNS server...", 2)

        if self.app.change_dns_servers(dns_server):
            self.dns_dropdown(dns_key)
            self.app.show_status_message("DNS server changed successfully! 🌐", 3)
        else:
            self.app.show_status_message("Failed to change DNS server! ❌", 4)

    def dns_dropdown(self, value):
        server, _ = self.dns_servers[value]
        pings = [ping3.ping(server, timeout=1, unit='ms', size=56) or float('inf') for _ in range(5)]
        lowest_ping = min(pings)
        if lowest_ping != float('inf'):
            ping_result = f"{str(value).split(' -')[0]} Ping: {int(lowest_ping)}ms"
        else:
            ping_result = "No response from DNS servers"
        self.ui.dns_status_label.setText(ping_result)

    def ipad_submit_button_click(self, e):
        """ iPad Submit Button On Click Function - V2.0.0 """
        try:
            if self.app.is_gameloop_running():
                self.app.show_status_message("Close GameLoop first! (Use Force Close GameLoop)", 5)
                return
            
            # Get selected resolution
            resolution_text = self.ui.ipad_dropdown.currentText()
            if not resolution_text:
                self.app.show_status_message("Please select a resolution!", 3)
                return
            
            self.app.show_status_message("Applying iPad settings...", 2)
            self.ui.ipad_other_btn.setEnabled(False)
            self.ui.ipad_rest_btn.setEnabled(False)
            
            try:
                self.worker_ipad_submit = IPADWorkerThread(self.app, self.ui, self)
                self.worker_ipad_submit.task_completed.connect(self.submit_ipad_done)
                self.worker_ipad_submit.start()
            except Exception as e:
                self.logger.error(f"iPad worker thread failed: {str(e)}")
                self.app.show_status_message("Failed to start iPad configuration!", 4)
                self.ui.ipad_other_btn.setEnabled(True)
                self.ui.ipad_rest_btn.setEnabled(True)
                
        except Exception as e:
            self.logger.error(f"iPad submit failed: {str(e)}")
            self.app.show_status_message("iPad configuration failed!", 4)

    def submit_ipad_done(self):
        """ iPad Submit Done - V2.0.0 """
        self.ui.ipad_other_btn.setEnabled(True)
        self.ui.ipad_rest_btn.setEnabled(True)
        self.ui.ipad_rest_btn.show()
        
        gameloop_status = "Restart" if self.app.is_gameloop_running() else "Start"
        self.app.show_status_message(f"{gameloop_status} GameLoop and enjoy iPad settings! 📱", 7)

    def ipad_reset_button_click(self, e):
        """ iPad Reset Button On Click Function - V2.0.0 """
        if self.app.is_gameloop_running():
            self.app.show_status_message("Close GameLoop! (Force Close GameLoop)", 5)
            return

        self.app.show_status_message("Resetting iPad settings...", 2)
        width, height = self.app.reset_ipad()
        
        self.ui.ipad_rest_btn.hide()
        
        message = f"Start GameLoop - Resolution: ({width} x {height}) 🔄"
        self.app.show_status_message(message, 7)

    def setup_language_buttons(self):
        """Dil değiştirme butonlarını ayarla - V2.0.0"""
        # Language page'i için dil seçimi UI'si oluştur
        self.create_language_page_content()

    def create_language_page_content(self):
        """Language page için içerik oluştur - V2.0.0"""
        try:
            from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QFont
        except ImportError:
            from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QFont
        
        # Language page content frame'ini temizle ve yeniden oluştur
        content_frame = self.ui.language_content_frame
        
        # Main layout
        main_layout = QVBoxLayout(content_frame)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)
        
        # Title
        title_label = QLabel("🌍 Language Selection / Dil Seçimi / اختيار اللغة")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Choose your preferred language for the application interface:")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 30px;
            }
        """)
        main_layout.addWidget(desc_label)
        
        # Language buttons container
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(20)
        
        # Language options
        languages = [
            ('en', 'English', '🇺🇸', 'English - Default language'),
            ('tr', 'Türkçe', '🇹🇷', 'Türkçe - Turkish language'),
            ('ar', 'العربية', '🇸🇦', 'العربية - Arabic language')
        ]
        
        for lang_code, lang_name, flag, description in languages:
            # Language button container
            lang_container = QFrame()
            lang_container.setFixedHeight(80)
            lang_container.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                }
                QFrame:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    border-color: rgba(255, 255, 255, 0.4);
                }
            """)
            
            lang_layout = QHBoxLayout(lang_container)
            lang_layout.setContentsMargins(20, 10, 20, 10)
            
            # Flag and language name
            flag_label = QLabel(f"{flag} {lang_name}")
            flag_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            lang_layout.addWidget(flag_label)
            
            # Description
            desc_lang_label = QLabel(description)
            desc_lang_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 12px;
                }
            """)
            lang_layout.addWidget(desc_lang_label)
            
            lang_layout.addStretch()
            
            # Select button
            select_btn = QPushButton("Select")
            select_btn.setFixedSize(100, 40)
            select_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 150, 255, 0.8);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(0, 150, 255, 1.0);
                }
                QPushButton:pressed {
                    background-color: rgba(0, 120, 200, 1.0);
                }
            """)
            select_btn.clicked.connect(lambda checked, code=lang_code: self.change_language(code))
            lang_layout.addWidget(select_btn)
            
            buttons_layout.addWidget(lang_container)
        
        main_layout.addWidget(buttons_frame)
        main_layout.addStretch()
        
        # Current language info
        current_lang_label = QLabel(f"Current Language: {self.app.language_manager.current_language.upper()}")
        current_lang_label.setAlignment(Qt.AlignCenter)
        current_lang_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                margin-top: 20px;
            }
        """)
        main_layout.addWidget(current_lang_label)

    def create_language_selection_UI(self):
        """Dil seçimi UI'sini oluştur - V2.0.0"""
        try:
            from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QLabel, QFrame, QVBoxLayout
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QFont
        except ImportError:
            from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QFrame, QVBoxLayout
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QFont
        
        # About sayfasında dil seçimi için frame oluştur
        language_frame = QFrame(self.ui.about_page)
        language_frame.setGeometry(50, 400, 400, 100)
        language_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(language_frame)
        
        # Dil etiketi
        lang_label = QLabel(self.app.language_manager.get_text('language'))
        lang_label.setAlignment(Qt.AlignCenter)
        lang_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(lang_label)
        
        # Dil butonları için horizontal layout
        button_layout = QHBoxLayout()
        
        # Her dil için buton oluştur
        for lang_code, lang_name in self.languages.items():
            btn = QPushButton(lang_name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 5px;
                    padding: 8px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.4);
                }
            """)
            btn.clicked.connect(lambda checked, code=lang_code: self.change_language(code))
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        language_frame.show()
        
        # Animasyonla göster (geçici olarak devre dışı)
        # self.app.animation_manager.fade_in(language_frame, 500)

    def change_language(self, lang_code):
        """Dil değiştir - V2.0.0"""
        # Buton animasyonu (geçici olarak devre dışı)
        # self.app.animation_manager.pulse_effect(self.ui.about_page, 300)
        
        # Dil değiştir
        self.app.change_language(lang_code)

    def update_language_display(self, current_lang):
        """Mevcut dil gösterimini güncelle - V2.0.0"""
        # Mevcut dili vurgula veya göster
        pass