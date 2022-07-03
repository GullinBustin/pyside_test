import time
from PySide2.QtCore import Qt, QObject, QThread, Signal as pyqtSignal


class LongTask(QThread):
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(5):
            time.sleep(1)
            self.progress.emit(i + 1)


class MainController(QObject):

    def __init__(self, model, view):
        super().__init__()
        self._model = model
        self._view = view
        self._view.long_running_btn.clicked.connect(self.run_long_task)
        self._view.count_btn.clicked.connect(self.add_click)
        self.thread = None

    def add_click(self):
        self._model.clicks_count += 1

    def update_long_task_step(self, step):
        self._model.long_task_step = step

    def update_long_task_running(self, is_running):
        self._model.long_task_is_running = is_running

    def run_long_task(self):
        # Step 2: Create a QThread object
        self.thread = LongTask()
        self.thread.progress.connect(self.update_long_task_step)
        self.thread.finished.connect(
            lambda: self.update_long_task_running(False)
        )
        self.update_long_task_step(0)
        self.update_long_task_running(True)
        self.thread.start()
