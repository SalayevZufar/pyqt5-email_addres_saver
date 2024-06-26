import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        # self.setGeometry(500,500,460,85)
        self.setFixedSize(460,85)
        self.setWindowTitle("Email address saver")
        self.setWindowIcon(QIcon("icons/icon.jpg"))
        self.initUI()
        

    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my first label")
        self.label.move(50,50)
        
        

        self.line = QLineEdit(self)
        font = self.line.font()      
        font.setPointSize(10)         
        self.line.setFont(font)      
        self.line.move(0,0)
        self.line.resize(200,40)

        self.line2 = QLineEdit(self)
        self.line2.setFont(font)
        self.line2.move(0,42)
        self.line2.resize(200,40)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("@gmail.com")
        self.b1.clicked.connect(self.add_mail)
        self.b1.move(205,0)
        self.b1.resize(80,40)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Clear")
        self.b2.clicked.connect(self.clear_b3)
        self.b2.move(205,42)
        self.b2.resize(80,40)

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setText("Clear")
        self.b3.clicked.connect(self.clear_b2)
        self.b3.move(290,0)
        self.b3.resize(80,40)
        
        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setText("Save")
        self.b4.clicked.connect(self.add_db)
        self.b4.move(380, 0)
        self.b4.resize(80,40)

        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setText("Open DB")
        self.b5.clicked.connect(self.new_window)
        self.b5.move(380, 42)
        self.b5.resize(80,40)

    def add_mail(self):
        self.line.setText(self.line.text() + "@gmail.com")
          
    def add_db(self):
        con = sqlite3.connect('data.db')  
        cur = con.cursor()
        if self.line.text()==  '':
            return False
        else:  
            cur.execute(f'''INSERT INTO user(
                ADRESS,PASSWORD) VALUES 
                ('{self.line.text()}','{self.line2.text()}')''')
        con.commit()
        cur.close()
    def clear_b2(self):
        self.line.clear()
    def clear_b3(self):
        self.line2.clear()
    def new_window(self):
        self.w = Window2()
        self.w.show()
        self.hide()
    def open_db(self):
        pass

class Window2(QMainWindow):
    def __init__(self):
        super(Window2,self).__init__()
        self.setFixedSize(500,500)
        
        self.setWindowIcon(QIcon("icons/icon_db.png"))
        self.setWindowTitle("Data Base")
        self.table()
    def table(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM user")
        users = cur.fetchall()

        table = QTableWidget(self)
        table.setRowCount(len(users))
        table.setColumnCount(4)
        table.setMinimumWidth(500)
        table.setMinimumHeight(450)
        
        count = 0  
        table.setHorizontalHeaderItem(0, QTableWidgetItem('Email'))
        table.setHorizontalHeaderItem(1, QTableWidgetItem('Password'))
        table.setHorizontalHeaderItem(2, QTableWidgetItem('Edit column'))
        table.setHorizontalHeaderItem(3, QTableWidgetItem('Delate row'))
        for column_1 in users:
            
            table.setItem(count,0, QTableWidgetItem(column_1[1]))
            count +=1
        count = 0
        
        for column_2 in users:
            
            table.setItem(count,1, QTableWidgetItem(column_2[2]))
            
            edit_btn = QtWidgets.QPushButton()
            table.setCellWidget(count, 2, edit_btn)

            edit_btn.setText("Edit")
            
            del_btn = QtWidgets.QPushButton()
          
            del_btn.pressed.connect(lambda: self.del_button(column_2[0]))
            

            table.setCellWidget(count, 3, del_btn)
            del_btn.setText("Delate")
            count +=1
        


        table.resizeColumnsToContents()
        table.resizeRowsToContents()
       
        table.show()
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Back")
        self.b1.clicked.connect(self.new_window)
        self.b1.move(420, 460)
        self.b1.resize(80,40)

        win = self.frameGeometry()
        pos = QDesktopWidget().availableGeometry().center()
        win.moveCenter(pos)
        self.move(win.topLeft())
        self.show()

    def del_button(self,id):
        con = sqlite3.connect('data.db')  
        cur = con.cursor()
        delete_column = f"DELETE from user where ID={id}"
        cur.execute(delete_column)


        con.commit()
        cur.close()
        self.new_window_2()
    def new_window(self):
        self.w = MainWindow()
        self.w.show()
        self.hide()
    def new_window_2(self):
        self.w = Window2()
        self.w.show()
        self.hide()
        
def window():  
    app = QApplication(sys.argv)
    win = MainWindow()
    win.add_db()
    win.show()
    sys.exit(app.exec_())
window()
