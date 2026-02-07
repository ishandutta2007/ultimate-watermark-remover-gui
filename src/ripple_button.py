from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Property, QParallelAnimationGroup


class RippleButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ripple_animations = []

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        ripple = RippleAnimation(self, event.pos())
        self._ripple_animations.append(ripple)
        ripple.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for ripple in self._ripple_animations:
            painter.setOpacity(ripple.opacity)
            painter.setBrush(ripple.color)
            painter.setPen(QColor(0, 0, 0, 0))
            painter.drawEllipse(ripple.center, ripple.radius, ripple.radius)

        # Cleanup finished animations
        self._ripple_animations = [r for r in self._ripple_animations if r.state() == QPropertyAnimation.Running]


class RippleAnimation(QPropertyAnimation):
    def __init__(self, parent, center):
        super().__init__(parent, b"radius")
        self._parent = parent
        self.center = center
        self.radius = 0
        self.opacity = 0.8
        self.color = QColor(200, 255, 200, 150) # Light transparent green

        self.setDuration(800)
        self.setEasingCurve(QEasingCurve.OutCubic)
        self.setEndValue(self._parent.width() * 2)

        self._opacity_animation = QPropertyAnimation(self, b"opacity")
        self._opacity_animation.setDuration(800)
        self._opacity_animation.setEndValue(0.0)

        self._animation_group = QParallelAnimationGroup()
        self._animation_group.addAnimation(self)
        self._animation_group.addAnimation(self._opacity_animation)
        self._animation_group.finished.connect(self.deleteLater)

    def start(self):
        self._animation_group.start()

    def _set_radius(self, radius):
        self.radius = radius
        self._parent.update()

    def _get_radius(self):
        return self.radius

    def _set_opacity(self, opacity):
        self.opacity = opacity
        self._parent.update()

    def _get_opacity(self):
        return self.opacity
    
    radius = Property(float, _get_radius, _set_radius)
    opacity = Property(float, _get_opacity, _set_opacity)
