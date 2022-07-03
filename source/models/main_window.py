from PySide2.QtCore import Qt, QObject, QThread, Signal as pyqtSignal


class MainModel(QObject):
    clicks_changed = pyqtSignal(int)
    long_task_changed = pyqtSignal(int)
    long_task_is_running_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._clicks_count = 0
        self._long_task_count = 0
        self._long_task_running = False

    @property
    def clicks_count(self):
        return self._clicks_count

    @clicks_count.setter
    def clicks_count(self, value):
        self._clicks_count = value
        self.clicks_changed.emit(value)

    @property
    def long_task_step(self):
        return self._long_task_count

    @long_task_step.setter
    def long_task_step(self, value):
        self._long_task_count = value
        self.long_task_changed.emit(value)

    @property
    def long_task_is_running(self):
        return self._long_task_running

    @long_task_is_running.setter
    def long_task_is_running(self, value):
        self._long_task_running = value
        self.long_task_is_running_signal.emit(value)
