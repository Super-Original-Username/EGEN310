import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import atexit

from devs import *
from cGUI import *
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import inputs
from inputs import get_key

class Picker(Ui_Dialog):
    def __init__(self, dialog):
        super(Picker,self).__init__()
        self.setupUi(dialog)
        self.scan_btn.clicked.connect(self.scan)
        #self.accept_btn.clicked.connect(self.pick_dev)
        self.accept_btn.clicked.connect(self.cancel_input)
        self.ble = Adafruit_BluefruitLE.get_provider()

    def scan(self):
        self.ble.initialize()
        self.ble.run_mainloop_with(self.scan_loop)

    def scan_loop(self):
        self.ble.clear_cached_data()
        adapter = self.ble.get_default_adapter()
        adapter.power_on()
        UART.disconnect_devices()
        try:
            adapter.start_scan()

            self.device = UART.find_device()
            if self.device is None:
                raise RuntimeError("no device found")
        finally:
            adapter.stop_scan()

        self.device.connect()

        try:
            UART.discover(self.device)
            self.yurt = UART(self.device)
            #yurt.write(bytearray('hello','utf-8'))
            #received = yurt.read(timeout_sec=60)
            #for i in range(50):
                #yurt.write(bytearray('{0}'.format(i),'utf-8'))
            #self.input_reader = input_thread(yurt)
            #self.input_reader.start()
            self.read_input()
        except Exception as e:
            print(e)
        #finally:
            #device.disconnect()

    def read_input(self):
        try:
            while not False:
                events = get_key()
                for event in events:
                    self.yurt.write(bytearray('{0}'.format(event.name),'utf-8'))
        except Exception as e:
            print(e)

    def cancel_input(self):
        self.input_reader.inter = True
        self.input_reader.__del__()
        self.device.disconnect()



class Controller(Ui_MainWindow):
    data_send = pyqtSignal(bytearray)
    def __init__(self, dialog, device):
        super(Controller, self).__init__()
        self.dev = device


'''class input_thread(QThread):
    def __init__(self, tx):
        super(input_thread,self).__init__()
        self.yurt = tx
        self.inter = False

    def __del__(self):
        self.wait()
        self.quit()

    def run(self):
        try:
            while not self.inter:
                events = get_key()
                for event in events:
                    self.yurt.write(bytearray('{0}'.format(event.name),'utf-8'))
        except Exception as e:
            print(e)
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QDialog()
    m_gui = Picker(form)
    form.show()

    sys._excepthook = sys.excepthook

    def exception_hook(exctype,value, traceback):
        print(exctype,value,traceback)
        sys._excepthook(exctype,value,traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    app.exec_()