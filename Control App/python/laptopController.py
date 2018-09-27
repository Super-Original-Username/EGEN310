import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cGUI import *
from devs import *
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

ble = Adafruit_BluefruitLE.get_provider()

class MainWindow(Ui_MainWindow):

    def __init__(self, dialog):
        super(MainWindow,self).__init__()

        self.setupUi(dialog)
        self.dev_btn.clicked.connect(self.run_picker)

    def run_picker(self):
        print('clickety click')
        self.p = QDialog()
        self.pick = Picker(self.p)
        self.p.show()

class Picker(Ui_Dialog):

    def __init__(self, dialog):
        super(Picker, self).__init__()
        self.setupUi(dialog)
        self.cancel_btn.clicked.connect(self.closeEvent)

    def closeEvent(self):
        self.destroy()


def scanUART():

    ble.clear_cached_data()

    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Active adapter: {0}'.format(adapter.name))

    print('Disconnecting UART devices')
    UART.disconnect_devices()

    print('Searching for devices')
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find device')
    finally:
        adapter.stop_scan()

    print('Connecting to device')
    device.connect()


if __name__  == '__main__':
    app = QApplication(sys.argv)
    form = QMainWindow()
    m_gui = MainWindow(form)
    form.show()

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback): # Catches exceptions that QT likes to hide
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app.exec_()

