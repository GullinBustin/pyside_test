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
    def __init__(self, model, controller):
        super().__init__()

        self.count_btn = None
        self.step_label = None
        self.clicks_label = None
        self.central_widget = None
        self.long_running_btn = None

        self._model = model
        self._controller = controller
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
        self.count_btn.clicked.connect(self._controller.add_click)
        self._model.clicks_changed.connect(self.click_update)

        self.long_running_btn = QPushButton("Long-Running Task!", self)
        self.long_running_btn.clicked.connect(self._controller.add_long_task)
        self._model.long_task_changed.connect(self.long_task_update)
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
    def click_update(self):
        self.clicks_label.setText(f"Counting: {self._model.clicks_count} clicks")

    @pyqtSlot(int)
    def long_task_update(self):
        self.step_label.setText(f"Long-Running Step: {self._model.long_task_step}")

    @pyqtSlot(bool)
    def disable_button(self):
        self.long_running_btn.setEnabled(not self._model.long_task_is_running)
