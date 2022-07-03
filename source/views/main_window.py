from PySide2.QtCore import Qt, QObject, QThread, Signal as pyqtSignal, Slot as pyqtSlot
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainView(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.count_btn = None
        self.step_label = None
        self.clicks_label = None
        self.central_widget = None
        self.long_running_btn = None

        self._model = model
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # Create and connect widgets
        self.clicks_label = QLabel("Counting: 0 clicks", self)
        self.clicks_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.step_label = QLabel("Long-Running Step: 0")
        self.step_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.count_btn = QPushButton("Click me!", self)
        self._model.clicks_count_signal.connect(self.clicks_count_update)

        self.long_running_btn = QPushButton("Long-Running Task!", self)
        self._model.long_task_step_signal.connect(self.long_task_step_update)
        self._model.long_task_is_running_signal.connect(self.disable_button)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicks_label)
        layout.addWidget(self.count_btn)
        layout.addStretch()
        layout.addWidget(self.step_label)
        layout.addWidget(self.long_running_btn)
        self.central_widget.setLayout(layout)

    @pyqtSlot(int)
    def clicks_count_update(self):
        self.clicks_label.setText(f"Counting: {self._model.clicks_count} clicks")

    @pyqtSlot(int)
    def long_task_step_update(self):
        self.step_label.setText(f"Long-Running Step: {self._model.long_task_step}")

    @pyqtSlot(bool)
    def disable_button(self):
        self.long_running_btn.setEnabled(not self._model.long_task_is_running)
