# editor.py

from PyQt5.QtWidgets import QTextEdit, QFontComboBox, QSpinBox, QToolBar, QColorDialog, QAction
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QPalette, QFont


class TextEditor(QTextEdit):
    paragraph_changed = pyqtSignal(int, str)

    def __init__(self, edit_tree):
        super().__init__()
        self.edit_tree = edit_tree
        self.setAcceptRichText(True)
        self.textChanged.connect(self.handle_text_change)
        self.current_paragraphs = []
        self.setup_toolbar()

    def setup_toolbar(self):
        self.toolbar = QToolBar()

        # Font family
        self.fontBox = QFontComboBox(self.toolbar)
        self.fontBox.setCurrentFont(QFont("Arial"))
        self.fontBox.currentFontChanged.connect(self.font_family_changed)
        self.toolbar.addWidget(self.fontBox)

        # Font size
        self.sizeBox = QSpinBox(self.toolbar)
        self.sizeBox.setValue(12)
        self.sizeBox.valueChanged.connect(self.font_size_changed)
        self.toolbar.addWidget(self.sizeBox)

        # Bold
        boldAction = QAction("B", self)
        boldAction.setCheckable(True)
        boldAction.triggered.connect(self.bold_text)
        self.toolbar.addAction(boldAction)

        # Italic
        italicAction = QAction("I", self)
        italicAction.setCheckable(True)
        italicAction.triggered.connect(self.italic_text)
        self.toolbar.addAction(italicAction)

        # Underline
        underlineAction = QAction("U", self)
        underlineAction.setCheckable(True)
        underlineAction.triggered.connect(self.underline_text)
        self.toolbar.addAction(underlineAction)

        # Text color
        colorAction = QAction("Color", self)
        colorAction.triggered.connect(self.text_color)
        self.toolbar.addAction(colorAction)

    def get_toolbar(self):
        return self.toolbar

    def font_family_changed(self, font):
        self.setFontFamily(font.family())

    def font_size_changed(self, size):
        self.setFontPointSize(size)

    def bold_text(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if checked else QFont.Normal)
        self.mergeCurrentCharFormat(fmt)

    def italic_text(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.mergeCurrentCharFormat(fmt)

    def underline_text(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.mergeCurrentCharFormat(fmt)

    def text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.mergeCurrentCharFormat(fmt)

    def handle_text_change(self):
        new_paragraphs = self.toPlainText().split('\n\n')
        for i, (old, new) in enumerate(zip(self.current_paragraphs, new_paragraphs)):
            if old != new:
                self.paragraph_changed.emit(i, new)
        if len(new_paragraphs) > len(self.current_paragraphs):
            for i in range(len(self.current_paragraphs), len(new_paragraphs)):
                self.paragraph_changed.emit(i, new_paragraphs[i])
        self.current_paragraphs = new_paragraphs[:]