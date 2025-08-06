# -*- coding: utf-8 -*-
"""
CRTY PUBG Mobile Tool V2.0.0 - Animation System
Modern animasyon sistemi ile gelişmiş kullanıcı deneyimi
"""

try:
    from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtSignal, QObject
    from PyQt5.QtWidgets import QGraphicsOpacityEffect
    from PyQt5.QtGui import QColor
except ImportError:
    from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QTimer, Signal as pyqtSignal, QObject
    from PySide6.QtWidgets import QGraphicsOpacityEffect
    from PySide6.QtGui import QColor


class AnimationManager(QObject):
    """Animasyon yöneticisi sınıfı"""
    
    animation_finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations = []
        self.fade_effects = {}
        
    def fade_in(self, widget, duration=500):
        """Widget'ı fade in animasyonu ile göster"""
        try:
            if not widget or not widget.isVisible():
                return None
                
            if widget not in self.fade_effects:
                effect = QGraphicsOpacityEffect()
                widget.setGraphicsEffect(effect)
                self.fade_effects[widget] = effect
            
            effect = self.fade_effects[widget]
            
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            self.animations.append(animation)
            animation.start()
            
            return animation
        except Exception:
            return None
    
    def fade_out(self, widget, duration=500):
        """Widget'ı fade out animasyonu ile gizle"""
        try:
            if not widget:
                return None
                
            if widget not in self.fade_effects:
                effect = QGraphicsOpacityEffect()
                widget.setGraphicsEffect(effect)
                self.fade_effects[widget] = effect
            
            effect = self.fade_effects[widget]
            
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            self.animations.append(animation)
            animation.start()
            
            return animation
        except Exception:
            return None
    
    def slide_in_from_left(self, widget, duration=600):
        """Widget'ı soldan slide in animasyonu ile göster"""
        start_rect = widget.geometry()
        end_rect = QRect(start_rect)
        start_rect.moveLeft(-start_rect.width())
        
        widget.setGeometry(start_rect)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def slide_in_from_right(self, widget, duration=600):
        """Widget'ı sağdan slide in animasyonu ile göster"""
        start_rect = widget.geometry()
        end_rect = QRect(start_rect)
        start_rect.moveLeft(widget.parent().width())
        
        widget.setGeometry(start_rect)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def bounce_effect(self, widget, duration=400):
        """Widget'a bounce efekti uygula"""
        original_rect = widget.geometry()
        
        # Küçült
        small_rect = QRect(original_rect)
        small_rect.setWidth(int(original_rect.width() * 0.95))
        small_rect.setHeight(int(original_rect.height() * 0.95))
        small_rect.moveCenter(original_rect.center())
        
        # İlk animasyon - küçültme
        animation1 = QPropertyAnimation(widget, b"geometry")
        animation1.setDuration(duration // 2)
        animation1.setStartValue(original_rect)
        animation1.setEndValue(small_rect)
        animation1.setEasingCurve(QEasingCurve.OutCubic)
        
        # İkinci animasyon - büyütme
        animation2 = QPropertyAnimation(widget, b"geometry")
        animation2.setDuration(duration // 2)
        animation2.setStartValue(small_rect)
        animation2.setEndValue(original_rect)
        animation2.setEasingCurve(QEasingCurve.OutBounce)
        
        # Animasyonları sırayla çalıştır
        animation1.finished.connect(animation2.start)
        
        self.animations.extend([animation1, animation2])
        animation1.start()
        
        return animation1, animation2
    
    def pulse_effect(self, widget, duration=1000, repeat=3):
        """Widget'a pulse efekti uygula"""
        if widget not in self.fade_effects:
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)
            self.fade_effects[widget] = effect
        
        effect = self.fade_effects[widget]
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 0.3)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setLoopCount(repeat)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def shake_effect(self, widget, duration=500):
        """Widget'a shake efekti uygula"""
        original_pos = widget.pos()
        shake_distance = 10
        
        positions = []
        steps = 10
        
        for i in range(steps):
            if i % 2 == 0:
                pos = original_pos
                pos.setX(pos.x() + shake_distance)
            else:
                pos = original_pos
                pos.setX(pos.x() - shake_distance)
            positions.append(pos)
        
        positions.append(original_pos)
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        
        for i, pos in enumerate(positions):
            animation.setKeyValueAt(i / len(positions), pos)
        
        animation.setEasingCurve(QEasingCurve.OutBounce)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def smooth_page_transition(self, stacked_widget, new_page, direction="left"):
        """Sayfa geçişi için smooth animasyon"""
        current_page = stacked_widget.currentWidget()
        
        if direction == "left":
            # Mevcut sayfayı sola kaydır
            self.slide_out_to_left(current_page)
            # Yeni sayfayı sağdan getir
            QTimer.singleShot(100, lambda: self._show_new_page(stacked_widget, new_page, "right"))
        else:
            # Mevcut sayfayı sağa kaydır
            self.slide_out_to_right(current_page)
            # Yeni sayfayı soldan getir
            QTimer.singleShot(100, lambda: self._show_new_page(stacked_widget, new_page, "left"))
    
    def _show_new_page(self, stacked_widget, new_page, from_direction):
        """Yeni sayfayı göster"""
        stacked_widget.setCurrentWidget(new_page)
        
        if from_direction == "right":
            self.slide_in_from_right(new_page)
        else:
            self.slide_in_from_left(new_page)
    
    def slide_out_to_left(self, widget, duration=400):
        """Widget'ı sola kaydırarak gizle"""
        start_rect = widget.geometry()
        end_rect = QRect(start_rect)
        end_rect.moveLeft(-start_rect.width())
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.InCubic)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def slide_out_to_right(self, widget, duration=400):
        """Widget'ı sağa kaydırarak gizle"""
        start_rect = widget.geometry()
        end_rect = QRect(start_rect)
        end_rect.moveLeft(widget.parent().width())
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.InCubic)
        
        self.animations.append(animation)
        animation.start()
        
        return animation
    
    def clear_animations(self):
        """Tüm animasyonları temizle"""
        for animation in self.animations:
            if animation.state() == QPropertyAnimation.Running:
                animation.stop()
        self.animations.clear()


class LoadingAnimation(QObject):
    """Yükleme animasyonu sınıfı"""
    
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.loading_text = "Yükleniyor"
        self.dots = 0
        
    def start_loading(self, text="İşlem yapılıyor"):
        """Yükleme animasyonunu başlat"""
        self.loading_text = text
        self.dots = 0
        self.timer.start(500)  # Her 500ms'de bir güncelle
        
    def stop_loading(self):
        """Yükleme animasyonunu durdur"""
        self.timer.stop()
        
    def update_loading(self):
        """Yükleme metnini güncelle"""
        self.dots = (self.dots + 1) % 4
        dots_text = "." * self.dots
        self.widget.setText(f"{self.loading_text}{dots_text}")


class ProgressAnimation(QObject):
    """İlerleme çubuğu animasyonu"""
    
    progress_updated = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.current_value = 0
        self.target_value = 0
        self.step = 1
        
    def animate_to_value(self, target, duration=1000):
        """Belirtilen değere animasyonlu geçiş"""
        self.target_value = target
        steps = duration // 50  # 50ms aralıklarla güncelle
        self.step = max(1, abs(target - self.current_value) // steps)
        
        self.timer.start(50)
        
    def update_progress(self):
        """İlerleme değerini güncelle"""
        if self.current_value < self.target_value:
            self.current_value = min(self.current_value + self.step, self.target_value)
        elif self.current_value > self.target_value:
            self.current_value = max(self.current_value - self.step, self.target_value)
        
        self.progress_updated.emit(self.current_value)
        
        if self.current_value == self.target_value:
            self.timer.stop()