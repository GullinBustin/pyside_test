import sys
from PySide2.QtWidgets import QApplication


from controllers.main_window import MainController


def main():
    app = QApplication(sys.argv)

    main_controller = MainController()
    main_controller.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
