import sys
import json
from typing import List
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import Qt


DATA_FILE = "data.json"
LABELS = ["Produto", "Marca", "Tamanho", "Especificação"]

LABEL_COLORS = [
    QColor(200, 200, 200),  # Light Gray
    QColor(144, 238, 144),  # Light Green
    QColor(173, 216, 230),  # Light Blue
    QColor(255, 255, 204),  # Light Yellow
]


class NERLabelingApp(QMainWindow):
    def __init__(self, data_list: List):
        super().__init__()
        self.data_list = data_list
        self.selected_tags = []
        self.current_text_index = 0
        self.current_label_index = 0

        # Widgtes
        self.text_view = None
        self.tags_view = None
        self.labels_combo_box = None
        self.save_button = None
        self.clear_button = None
        self.next_button = None
        self.previous_button = None
        self.current_index_label = None

        self._load_widgets()
        self._load_layout()
        self.update_all()

    def update_all(self):
        self._update_text()
        self._update_labels()
        self._update_index()

    def reset_all(self):
        self.selected_tags = []
        self.labels_combo_box.setCurrentIndex(0)
        self.update_all()

    def _update_text(self):
        self.text_view.setTextBackgroundColor(QColor("White"))
        self.text_view.setPlainText(self.data_list[self.current_text_index])

    def _update_labels(self):
        text = ""
        for tag in self.selected_tags:
            tag_name = tag[0]
            name = self.text_view.toPlainText()[tag[1] : tag[2]]
            text += f"{tag_name} : {name}\n"
        self.tags_view.setText(text)

    def _update_index(self):
        self.current_index_label.setText(str(self.current_text_index))

    def on_mouse_release(self, event):
        selected_text = self.text_view.textCursor().selectedText()
        start = self.text_view.textCursor().selectionStart()
        end = self.text_view.textCursor().selectionEnd()
        if selected_text:
            tag = [LABELS[self.current_label_index], start, end]
            if tag not in self.selected_tags:
                self.selected_tags.append(tag)
                self._update_labels()

        # Highlight the selected text
        self.highlight_selected_text(LABEL_COLORS[self.current_label_index])

    def highlight_selected_text(self, color):
        cursor = self.text_view.textCursor()
        format = QTextCharFormat()
        format.setBackground(color)
        cursor.mergeCharFormat(format)

    def save_data_action(self):  # TODO
        selected_text = self.text_view.textCursor().selectedText()
        selected_tags = [
            self.labels_combo_box.itemText(i)
            for i in range(self.labels_combo_box.count())
            if self.labels_combo_box.itemText(i) in self.selected_tags
        ]

        # Save or process the labeled data here

        self.current_text_index += 1
        self._update_text()

    def change_current_label_action(self, event):
        self.current_label_index = self.labels_combo_box.currentIndex()

    def previous_text_action(self):
        self.current_text_index -= 1
        self.current_text_index = max(self.current_text_index, 0)
        self.update_all()

    def next_text_action(self):
        self.current_text_index += 1
        self.current_text_index = min(self.current_text_index, len(self.data_list) - 1)
        self.update_all()

    def _load_widgets(self):
        self.text_view = QTextEdit(self)
        self.text_view.setFixedHeight(self.text_view.fontMetrics().height() + 10)
        self.text_view.setReadOnly(True)

        self.tags_view = QLabel(self)
        self.tags_view.setStyleSheet("background-color: lightblue;")

        self.labels_combo_box = QComboBox(self)
        self.labels_combo_box.addItems(LABELS)
        self.labels_combo_box.currentIndexChanged.connect(self.change_current_label_action)

        # Buttons
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_data_action)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.reset_all)

        self.next_button = QPushButton(">>", self)
        self.next_button.clicked.connect(self.next_text_action)

        self.previous_button = QPushButton("<<", self)
        self.previous_button.clicked.connect(self.previous_text_action)

        self.current_index_label = QLabel(self)
        self.current_index_label.setText("0")
        self.current_index_label.setAlignment(Qt.AlignCenter)

        self.text_view.mouseReleaseEvent = self.on_mouse_release

    def _load_layout(self):
        self.setWindowTitle("NER Labeling Interface")
        self.resize(500, 300)

        # The labels handler (Save, Clear)
        labels_handler_layout = QHBoxLayout()
        labels_handler_layout.addWidget(self.save_button)
        labels_handler_layout.addWidget(self.clear_button)

        labels_tools_widget = QWidget()
        labels_tools_widget.setLayout(labels_handler_layout)

        # The text handler (<<, index, >>)
        text_handler_layour = QHBoxLayout()
        text_handler_layour.addWidget(self.previous_button)
        text_handler_layour.addWidget(self.current_index_label)
        text_handler_layour.addWidget(self.next_button)

        text_tools_widget = QWidget()
        text_tools_widget.setLayout(text_handler_layour)

        # Main Layoutw
        layout = QVBoxLayout()
        layout.addWidget(self.text_view)
        layout.addWidget(self.labels_combo_box)
        layout.addWidget(self.tags_view)
        layout.addWidget(labels_tools_widget)
        layout.addWidget(text_tools_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    with open(DATA_FILE) as json_file:
        data_list = json.load(json_file)

    app = QApplication(sys.argv)
    window = NERLabelingApp(data_list)
    window.show()
    sys.exit(app.exec_())
