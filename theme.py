from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PyQt5.QtGui import QPalette, QColor, QBrush, QPixmap


class ThemeManager:
    def __init__(self, parent):
        self.parent = parent
        self.themes = {
            "light": {
                "window": "#FFFFFF",
                "text": "#000000",
                "base": "#FFFFFF",
                "button": "#F0F0F0",
                "button_text": "#000000",
                "highlight": "#0078D7",
                "highlight_text": "#FFFFFF"
            },
            "dark": {
                "window": "#1E1E1E",
                "text": "#FFFFFF",  # Ensures all text is white in dark mode
                "base": "#2D2D2D",
                "button": "#333333",
                "button_text": "#FFFFFF",  # Button text in white for dark mode
                "highlight": "#0078D7",
                "highlight_text": "#FFFFFF"  # Highlighted text in white
            }
        }
        self.current_theme = "light"
        self.background_image = None

    def apply_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            theme = self.themes[theme_name]

            # Update the color palette based on the chosen theme
            palette = self.parent.palette()
            palette.setColor(QPalette.Window, QColor(theme["window"]))
            palette.setColor(QPalette.WindowText, QColor(theme["text"]))
            palette.setColor(QPalette.Base, QColor(theme["base"]))
            palette.setColor(QPalette.AlternateBase, QColor(theme["base"]))
            palette.setColor(QPalette.ToolTipBase, QColor(theme["window"]))
            palette.setColor(QPalette.ToolTipText, QColor(theme["text"]))
            palette.setColor(QPalette.Text, QColor(theme["text"]))
            palette.setColor(QPalette.Button, QColor(theme["button"]))
            palette.setColor(QPalette.ButtonText, QColor(theme["button_text"]))
            palette.setColor(QPalette.Highlight, QColor(theme["highlight"]))
            palette.setColor(QPalette.HighlightedText, QColor(theme["highlight_text"]))

            # Apply background image if set
            if self.background_image:
                brush = QBrush(self.background_image)
                palette.setBrush(QPalette.Window, brush)

            self.parent.setPalette(palette)

    def customize_theme(self):
        theme = self.themes[self.current_theme].copy()
        color_dialog = QColorDialog(self.parent)

        # Customize each color in the theme
        for key in theme:
            color = color_dialog.getColor(QColor(theme[key]), self.parent, f"Choose {key} color")
            if color.isValid():
                theme[key] = color.name()

        self.themes["custom"] = theme
        self.apply_theme("custom")

    def set_background_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Choose Background Image", "",
                                                   "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.background_image = QPixmap(file_name)
            self.apply_theme(self.current_theme)
