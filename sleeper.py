import sys
import os
import datetime
import platform
from PyQt6 import QtCore, QtGui, QtWidgets
from ui_file import Ui_MainWindow

os_type: str

def CheckOsType() -> str:
    if platform.system() == "Linux":
        os_type = "lin"
    elif platform.system() == "Darwin":
        os_type = "mac"
    elif platform.system() == "Windows":
        os_type = "win"
    else:
        os_type = "unknown"
    return os_type

def MakeTime(time_rn, time_entered) -> int:
    if application.ui.RB_rn.isChecked():
        time = 0
    elif application.ui.RB_in_time.isChecked():
        if time_rn == time_entered:
            time = 86400
        elif time_rn < time_entered:
            time = time_entered - time_rn
        else:
            time = (86400 - time_rn) + time_entered
    elif application.ui.RB_after_time.isChecked():
        time = time_entered
    return time

def WhatToDo(os_type) -> str:
    if application.ui.RB_reboot.isChecked():
        wtd = "-r"
    elif application.ui.RB_turn_off.isChecked():
        wtd = "-s"
    elif application.ui.RB_logout.isChecked():
        if os_type == "win":
            wtd = "-l"
        else:
            wtd = "exit"
    return wtd

def DoMainThing() -> None:
    os_type = CheckOsType()
    wtd = WhatToDo(os_type)
    time = MakeTime(CurrentTime(), TimeRequired())
    if os_type == "win":
        if wtd != "-l":
            os.system(f"shutdown {wtd} /t {time}")
        else:
            os.system(f"timeout {time} & shutdown {wtd}")
        
    elif os_type == "mac" or os_type == "lin":
        if wtd != "exit":
            os.system(f"sudo sleep {time} && shutdown {wtd}")
        else:
            os.system(f"sudo sleep {time} && {wtd}")

def CancelShutdown():
    os_type = CheckOsType()
    if os_type == "mac" or os_type == "lin":
        os.system("sudo shutdown -c")
    elif os_type == "win":
        os.system('shutdown -a')

def CurrentTime() -> int:
    now = datetime.datetime.now()
    current_time = now.hour * 3600 + now.minute * 60 + now.second
    return current_time

def TimeRequired() -> int:
    time_edit = application.ui.Time.time()
    required_time = time_edit.hour() * 3600 + time_edit.minute() * 60
    return required_time

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Button_apply.clicked.connect(DoMainThing)
        self.ui.Button_cancel.clicked.connect(CancelShutdown)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(100)
        self.update_current_time()

    def update_current_time(self):
        now = datetime.datetime.now()
        self.ui.Time_rn.setDateTime(now)

app = QtWidgets.QApplication(sys.argv)
application = MyWindow()
application.show()
sys.exit(app.exec())
