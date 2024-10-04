from PyQt5.QtWidgets import QMenuBar, QFileDialog, QMessageBox


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_menus()

    def create_menus(self):
        # File menu
        file_menu = self.addMenu("File")

        new_action = file_menu.addAction("New")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)  # Ensure method exists

        open_action = file_menu.addAction("Open")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)  # Ensure method exists

        save_action = file_menu.addAction("Save")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)  # Ensure method exists

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.parent.close)

        # Theme menu
        theme_menu = self.addMenu("Theme")

        light_theme = theme_menu.addAction("Light")
        light_theme.triggered.connect(lambda: self.apply_theme("light"))

        dark_theme = theme_menu.addAction("Dark")
        dark_theme.triggered.connect(lambda: self.apply_theme("dark"))

    def new_file(self):
        if self.parent.text_editor.document().isModified():
            reply = QMessageBox.question(
                self.parent, 'Save Changes?',
                'Do you want to save your changes before creating a new file?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return

        self.parent.text_editor.clear()
        self.parent.edit_tree.clear()

    def open_file(self):
        if self.parent.text_editor.document().isModified():
            reply = QMessageBox.question(
                self.parent, 'Save Changes?',
                'Do you want to save your changes before opening another file?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                return

        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as file:
                self.parent.text_editor.setPlainText(file.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.parent.text_editor.toPlainText())
            self.parent.text_editor.document().setModified(False)

    def apply_theme(self, theme_name):
        """Apply theme to MenuBar and other widgets."""
        self.parent.theme_manager.apply_theme(theme_name)
