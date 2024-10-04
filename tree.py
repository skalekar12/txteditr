# tree.py

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import Qt, pyqtSignal


class EditTree(QTreeWidget):
    revert_paragraph = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setHeaderLabel("Edit History")
        self.paragraph_history = {}
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def update_tree(self, text):
        paragraphs = text.split('\n\n')
        self.clear()

        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                if i not in self.paragraph_history:
                    self.paragraph_history[i] = []

                if not self.paragraph_history[i] or self.paragraph_history[i][-1] != paragraph:
                    self.paragraph_history[i].append(paragraph)

                para_item = QTreeWidgetItem(self)
                para_item.setText(0, f"Paragraph {i + 1}")
                para_item.setData(0, Qt.UserRole, i)

                for version, text in enumerate(self.paragraph_history[i]):
                    version_item = QTreeWidgetItem(para_item)
                    preview = text[:30] + "..." if len(text) > 30 else text
                    version_item.setText(0, f"Version {version + 1}: {preview}")
                    version_item.setData(0, Qt.UserRole, (i, text))

    def show_context_menu(self, position):
        item = self.itemAt(position)
        if item and item.parent():
            menu = QMenu()
            revert_action = menu.addAction("Revert to this version")
            action = menu.exec_(self.mapToGlobal(position))

            if action == revert_action:
                paragraph_index, text = item.data(0, Qt.UserRole)
                self.revert_paragraph.emit(paragraph_index, text)
