import time
from PySide2.QtCore import Qt, QObject, QThread, Signal as pyqtSignal


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            time.sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()


class MainController(QObject):

    def __init__(self, model):
        super().__init__()
        self._model = model

    def add_click(self):
        self._model.clicks_count += 1

    def add_long_task(self):
        self.run_long_task()

    def update_long_task_step(self, step):
        self._model.long_task_step = step

    def update_long_task_running(self, is_running):
        self._model.long_task_is_running = is_running

    def run_long_task(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_long_task_step)
        # Step 6: Start the thread
        self.update_long_task_step(0)
        self.update_long_task_running(True)
        self.thread.start()

        # Final resets
        self.thread.finished.connect(
            lambda: self.update_long_task_running(False)
        )
