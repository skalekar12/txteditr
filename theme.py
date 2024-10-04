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
                "highlight_text": "#FFFFFF",
                "navbar": "#F0F0F0",  # Navbar background for light theme
                "navbar_text": "#000000",  # Navbar text for light theme
                "navbar_hover": "#D0D0D0",  # Navbar hover background for light theme
            },
            "dark": {
                "window": "#1E1E1E",
                "text": "#FFFFFF",
                "base": "#2D2D2D",
                "button": "#333333",
                "button_text": "#FFFFFF",
                "highlight": "#0078D7",
                "highlight_text": "#FFFFFF",
                "navbar": "#333333",  # Navbar background for dark theme
                "navbar_text": "#FFFFFF",  # Navbar text for dark theme
                "navbar_hover": "#555555",  # Navbar hover background for dark theme
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

            # Apply the palette to the entire application
            self.parent.setPalette(palette)

            # Update MenuBar, EditTree, and other widgets to ensure correct text and background color
            self.update_widget_styles(theme)

    def update_widget_styles(self, theme):
        """Update additional widget styles that are not covered by the QPalette."""

        # Update MenuBar colors
        self.parent.menu_bar.setStyleSheet(
            f"background-color: {theme['navbar']}; color: {theme['navbar_text']};"
            f" QMenuBar::item {{ padding: 5px; }} "  # Add some padding for menu items
            f" QMenuBar::item:hover {{ background-color: {theme['navbar_hover']}; color: {theme['navbar_text']}; }}"
        )

        # Update toolbar colors (FontBox and SizeBox)
        self.parent.text_editor.fontBox.setStyleSheet(
            f"background-color: {theme['button']}; color: {theme['button_text']};"
        )
        self.parent.text_editor.sizeBox.setStyleSheet(
            f"background-color: {theme['button']}; color: {theme['button_text']};"
        )

        # Update EditTree colors
        self.parent.edit_tree.setStyleSheet(
            f"background-color: {theme['base']}; color: {theme['text']};"
        )

