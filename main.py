# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from editor import TextEditor
from tree import EditTree
from menu import MenuBar
from theme import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Text Editor")
        self.setMinimumSize(1000, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        editor_layout = QHBoxLayout()

        # Create and add edit tree
        self.edit_tree = EditTree()
        editor_layout.addWidget(self.edit_tree, 1)

        # Create and add text editor
        self.text_editor = TextEditor(self.edit_tree)
        editor_layout.addWidget(self.text_editor, 3)

        # Add toolbar to main layout
        main_layout.addWidget(self.text_editor.get_toolbar())

        # Add editor layout to main layout
        main_layout.addLayout(editor_layout)

        # Add commit button for committing changes
        self.commit_button = QPushButton("Commit Changes")
        self.commit_button.clicked.connect(self.commit_changes)
        main_layout.addWidget(self.commit_button)

        # Create menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Initialize theme manager
        self.theme_manager = ThemeManager(self)

        # Set up connections
        self.text_editor.textChanged.connect(self.on_text_changed)
        self.edit_tree.revert_paragraph.connect(self.revert_paragraph)

    def on_text_changed(self):
        pass  # No automatic update to EditTree on text change

    def commit_changes(self):
        current_text = self.text_editor.toPlainText()
        self.edit_tree.update_tree(current_text)

    def revert_paragraph(self, index, text):
        paragraphs = self.text_editor.toPlainText().split('\n\n')
        if 0 <= index < len(paragraphs):
            paragraphs[index] = text
            self.text_editor.setPlainText('\n\n'.join(paragraphs))

    def closeEvent(self, event):
        if self.text_editor.document().isModified():
            reply = QMessageBox.question(
                self, 'Save Changes?',
                'Do you want to save your changes before closing?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.menu_bar.save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
