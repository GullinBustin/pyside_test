import sys
from PySide2.QtWidgets import QApplication

from views.main_window import MainView
from models.main_window import MainModel
from controllers.main_window import MainController


def main():
    app = QApplication(sys.argv)
    main_model = MainModel()
    main_controller = MainController(main_model)
    win = MainView(main_model, main_controller)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
