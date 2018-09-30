import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import atexit

from cGUI import *
from devs import *
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

ble = Adafruit_BluefruitLE.get_provider()

class MainWindow(Ui_MainWindow):

    def __init__(self, dialog):
        super(MainWindow,self).__init__()

        self.BTDev = ''
        self.setupUi(dialog)
        self.dev_btn.clicked.connect(self.run_picker)

    def run_picker(self):
        self.p = QDialog()
        self.pick = Picker(self.p)
        self.p.show()
        #self.pick.ble.run_mainloop_with(self.pick.scan_dev)
        #self.pick.dev_signal.connect(self.set_device)
        #self.pick.scanUART()

    def set_device(self, list):
        self.BTDev = list[0]


class Picker(Ui_Dialog):
    #dev_signal = pyqtSignal(list)
    def __init__(self, dialog):
        super(Picker, self).__init__()
        self.d = dialog
        self.setupUi(dialog)
        self.dev = ''
        #self.ble = Adafruit_BluefruitLE.get_provider()
        #self.ble.initialize()
        self.cancel_btn.clicked.connect(self.shutdown)
        self.accept_btn.clicked.connect(self.pick_dev)
        #self.ble.run_mainloop_with(self.scan_dev)
        #elf.scan_thread = Scanner()
        #self.scan_thread.RTSender.connect(self.add_dev)
        #self.scan_thread.start()
        self.scan_thread = Unthreaded_scanner()
        self.scan_thread.RTSender.connect(self.add_dev)
        self.scan_thread.ble.run_mainloop_with(self.scan_thread.loopy)

    def shutdown(self):
        #self.scan_thread.adapter.stop_scan()
        self.scan_thread.__del__()
        self.d.close()

    def add_dev(self, item):
        self.listWidget.addItem(item)
        QApplication.processEvents()

    def pick_dev(self):
        print('device picked')

    def scan_dev(self):
        known = ''
        found = ''
        to_send = ''
        self.ble.clear_cached_data()
        adapter = self.ble.get_default_adapter()
        print(adapter)
        adapter.power_on()
        adapter.start_scan()
        known = set()
        for i in range(5):
            found = set(UART.find_devices())
            new = found - known
            for device in new:
                self.add_dev(QWidgetItem("%i" % device.name))
                known.update(device)
                print(device.name)


class Unthreaded_scanner(QObject):
    RTSender = pyqtSignal()
    def __init__(self):
        super(Unthreaded_scanner, self).__init__()
        self.prev = ''
        self.cur = ''
        self.to_send = ''
        self.interrupt = False
        self.adapter = ''
        self.ble = Adafruit_BluefruitLE.get_provider()
        # self.ble.initialize()
        # self.ble.run_mainloop_with(self.run)

    def __del__(self):
        self.interrupt = True
        self.quit()
        self.wait()

    def loopy(self):
        self.ble.initialize()
        self.ble.clear_cached_data()

        self.adapter = ble.get_default_adapter()
        self.adapter.power_on()
        print('Active adapter: {0}'.format(self.adapter.name))

        self.adapter.start_scan()
        atexit.register(self.adapter.stop_scan)

        known_uarts = set()
        for i in range(5):
            # while not self.interrupt:
            self.found = set(UART.find_devices())
            self.new = self.found - known_uarts
            for device in self.new:
                print(device.name)
                self.RTSender(QListWidgetItem(device))
            '''if self.prev == self.cur:
                continue
            else:
                self.to_send = self.cur
                self.RTSender.emit(QListWidgetItem(self.to_send))
                self.prev = self.cur'''

    def run(self):
        self.ble.run_mainloop_with(self.loopy)


class Scanner(QThread):
    RTSender = pyqtSignal()

    def __init__(self):

        super(Scanner, self).__init__()
        self.prev = ''
        self.cur = ''
        self.to_send = ''
        self.interrupt = False
        self.adapter = ''
        self.ble = Adafruit_BluefruitLE.get_provider()
        #self.ble.initialize()
        #self.ble.run_mainloop_with(self.run)

    def __del__(self):
        self.interrupt = True
        self.quit()
        self.wait()

    def loopy(self):
        self.ble.initialize()
        self.ble.clear_cached_data()

        self.adapter = ble.get_default_adapter()
        self.adapter.power_on()
        print('Active adapter: {0}'.format(self.adapter.name))

        self.adapter.start_scan()
        atexit.register(self.adapter.stop_scan)

        known_uarts = set()
        for i in range(5):
        #while not self.interrupt:
            self.found = set(UART.find_devices())
            self.new = self.found - known_uarts
            for device in self.new:
                print(device.name)
                self.RTSender(QListWidgetItem(device))
            '''if self.prev == self.cur:
                continue
            else:
                self.to_send = self.cur
                self.RTSender.emit(QListWidgetItem(self.to_send))
                self.prev = self.cur'''

    def run(self):
        self.ble.run_mainloop_with(self.loopy)




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

