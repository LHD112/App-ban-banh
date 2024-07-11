from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt6 import uic
import re
import json
import os
import sys
from PyQt6.QtWidgets import QMainWindow
#đăng nhập
class Login(QMainWindow):
    if not os.path.exists("data.json"):
                with open("data.json", "w") as file:
                    json.dump([], file)
    with open("AccountInUse.json" ,"w") as file:
        json.dump([] ,file)
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("dang_nhap.ui", self)
        self.dangnhap.clicked.connect(self.check_login)
        self.dangky.clicked.connect(self.showRegister)

    def showRegister(self):
        registerPage.show()
        self.close()
    
    def check_login(self):
        email = self.tk.text()
        password = self.mk.text()

        if not email: 
            inf_box.setText("Vui lòng nhập tên đăng nhập!")
            inf_box.exec()
            return

        if not password:
            inf_box.setText("Vui lòng nhập mật khẩu!")
            inf_box.exec()
            return
        with open("data.json", "r") as file:
            data = json.load(file)
            for user in data:
                self.s = user["tk"]
                self.s2 = user["mk"]
                if self.s == email and self.s2 == password:
                    self.dtuser = {
                        "ttk" : user["ttk"],
                        "tk" : user["tk"],
                        "mk" : user["mk"]
                    }
                    with open("AccountInUse.json" , "w") as file:
                        json.dump(self.dtuser ,file ,indent = 4)
                    self.close()
                    mainPage.show()  
                    return 
            inf_box.setText("tên đăng nhập hoặc mật khẩu không đúng!")
            inf_box.exec()   
#pt tk
class account:
    def __init__(self ,ttk ,ten ,mk):
        self.ttk = ttk
        self.ten = ten
        self.mk = mk
    def to_dict(self):
        return {
            "ttk" : self.ttk,
            "tk" : self.ten,
            "mk" : self.mk
        }
#hàm kiểm tra mật khẩu mạnh
def ihpass(password):
    t = False
    h = False
    db = False
    bd = False
    for i in password:
        if 'a'<=i<='z':
            t = True
        elif 'A'<=i<='Z':
            h = True
        elif '0'<=i<='9':
            db = True
        elif i!=' ':
            bd = True
    return t == h == db == bd == True
#kt tao ten dang nhap
def check_name(name):
    for i in name:
        if not('a'<=i<='z'):
            if not('A' <= i <= 'Z'):
                if not('0' <= i <= '9'):
                    return False
    return True
#đăng ký
class Register(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("dang_ky.ui", self)
        self.quaylai.clicked.connect(self.showlogin)
        self.dangkythanhcong.clicked.connect(self.check_dk)

    def showlogin(self):
        loginPage.show()
        self.close()

    def check_dk(self):
        email = self.taikhoan.text()
        password1 = self.matkhau1.text()
        password = self.matkhau.text()
        name = self.tentk.text()

        if not name:
            inf_box.setText("vui lòng nhập tên tài khoản!")
            inf_box.exec()
            return
        
        if not email:
            inf_box.setText("Vui lòng nhập tên đăng nhập!")
            inf_box.exec()
            return

        if not password:
            inf_box.setText("Vui lòng nhập mật khẩu!")
            inf_box.exec()
            return 
        #xử lý mật khẩu
        if email != "" and password != "" and password == password1:
            if check_name(email) == False:
                inf_box.setText("ten dang nhap ko chua ky tu dac biet")
                inf_box.exec()
                return
            if len(password)<8:
                inf_box.setText("mk it nha 8 ky tu")
                inf_box.exec()
                return
            if ihpass(password) == False:
                inf_box.setText("mk yếu(mk mạnh gồm ít nhất 1 chữ thường,1 chữ in hoa,1 chữ số và 1 ký tự đặc biệt khác dấu cách)")
                inf_box.exec()
                return
            #kiểm tra file data 
            if not os.path.exists("data.json"):
                with open("data.json", "w") as file:
                    json.dump([], file)
            #lưu vào json
            with open("data.json", "r") as file:
                data = json.load(file)
            self.opp = {
                "ttk" : name,
                "tk": email,                         
                "mk": password
            }
            self.checkbl = True
            for em in data:
                if(em["tk"] == email):
                    self.checkbl = False
            if self.checkbl == False:
                inf_box.setText("tk đã tồn tại!")
                inf_box.exec()
                return
            self.new = [self.opp]
            for user in data:
                if "tk" in user and "mk" in user and "ttk" in user:
                    self.tkmk = account(str(user["ttk"]) ,str(user["tk"]) ,str(user["mk"]))
                    self.new.append(self.tkmk.to_dict())
            with open("data.json", "w") as file:
                json.dump(self.new, file, indent = 4)
                msg_box.setText("dang ky thanh cong!")
                msg_box.exec()   

            self.close()
            loginPage.show()

        else:
            inf_box.setText("mật khẩu nhập lại chưa đúng!")
            inf_box.exec()   
#main
class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("chonloai.ui", self)
        self.banhbutton.clicked.connect(self.showlb)
        self.denbutton.clicked.connect(self.showld)
        self.userbutton.clicked.connect(self.showinformation)
    
    def showinformation(self):
        with open("AccountInUse.json" , "r") as file:
            self.data = json.load(file)
        self.information = (
            "ttk:" + str(self.data["ttk"]) + "\n" +
            "mat khau:" + str(self.data["mk"]) + "\n" +
            "ten dang nhap:" + str(self.data["tk"])
        )

        msg_box.setText(self.information)
        msg_box.exec()
        return
    def showlb(self):
        lbPage.show()
        self.close()

    def showld(self):
        ldPage.show()
        self.close()

#pt bánh
class banh():
    def __init__(self ,ten,gia):
        self.ten = ten
        self.gia = gia
#phần loại bánh
class lb(QtWidgets.QMainWindow):
    tt = 0
    ssl = 0
    ls = [
            banh("loai1 10k" ,"10000"),
            banh("loai2 15k" ,"15000")
        ]
    def __init__(self):
        super().__init__()
        uic.loadUi("loaibanh.ui" ,self)
        self.lt = [x.ten for x in self.ls]
        self.gc = [x.gia for x in self.ls]
        self.listWidget.addItems(self.lt)
        self.buy.clicked.connect(self.nhan)
        self.dlhang.clicked.connect(self.xoahang)
        self.clhang.clicked.connect(self.xoahet)
        self.backbutton.clicked.connect(self.ql)
        self.endbutton.clicked.connect(self.bought)

    def bought(self):
        msg_box.setText("bought")
        msg_box.exec()
        return
    
    def nhan(self):
        self.cr = self.listWidget.currentRow()
        if(self.cr!=-1):
            self.savestring = self.listWidget.item(self.cr).text()
            self.giohang.addItem(self.savestring)  
            self.ssl += 1
            for self.loop in self.ls:
                if(self.loop.ten == self.savestring):
                    self.tt += int(self.loop.gia)
            self.tongtien.setText(str(self.tt)+"đ")
            self.sl.setText(str(self.ssl))

    def xoahang(self):
        self.cr = self.giohang.currentRow()
        if(self.cr!=-1):
            self.savestring = self.giohang.item(self.cr).text()
            self.giohang.takeItem(self.cr)
            self.ssl -= 1
            for self.loop in self.ls:
                if(self.loop.ten == self.savestring):
                    self.tt -= int(self.loop.gia)
            self.tongtien.setText(str(self.tt)+"đ")
            self.sl.setText(str(self.ssl))

    def xoahet(self):
        self.giohang.clear()
        self.tt = 0
        self.ssl = 0
        self.tongtien.setText(str(self.tt)+"đ")
        self.sl.setText(str(self.ssl))

    def ql(self):
        mainPage.show()
        self.close()
#pt đèn
class den():
    def __init__(self ,ten,gia):
        self.ten = ten
        self.gia = gia
#phần loại đèn
class ld(QtWidgets.QMainWindow):
    tt = 0
    ssl = 0
    ls = [den("loai1 30k" ,"30000"),den("loai2 50k" ,"50000")]
    def __init__(self):
        super().__init__()
        uic.loadUi("loaiden.ui" ,self)
        self.lt = [x.ten for x in self.ls]
        self.gc = [x.gia for x in self.ls]
        self.listWidget.addItems(self.lt)
        self.buy.clicked.connect(self.nhan)
        self.dlhang.clicked.connect(self.xoahang)
        self.clhang.clicked.connect(self.xoahet)
        self.backbutton.clicked.connect(self.ql)
        self.endbutton.clicked.connect(self.bought)

    def bought(self):
        msg_box.setText("bought")
        msg_box.exec() 
        return
    
    def nhan(self):
        self.cr = self.listWidget.currentRow()
        if(self.cr!=-1):
            self.savestring = self.listWidget.item(self.cr).text()
            self.giohang.addItem(self.savestring)  
            self.ssl +=1
            for self.loop in self.ls:
                if(self.loop.ten == self.savestring):
                    self.tt += int(self.loop.gia)
            self.tongtien.setText(str(self.tt)+"đ")
            self.sl.setText(str(self.ssl))

    def xoahang(self):
        self.cr = self.giohang.currentRow()
        if(self.cr!=-1):
            self.savestring = self.giohang.item(self.cr).text()
            self.giohang.takeItem(self.cr)
            self.ssl -= 1                                                                                      
            for self.loop in self.ls:
                if(self.loop.ten == self.savestring):
                    self.tt -= int(self.loop.gia)
            self.tongtien.setText(str(self.tt)+"đ")
            self.sl.setText(str(self.ssl))

    def xoahet(self):
        self.giohang.clear()
        self.tt = 0
        self.ssl = 0
        self.sl.setText(str(self.ssl))
        self.tongtien.setText(str(self.tt)+"đ")

    def ql(self):
        mainPage.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginPage = Login()
    loginPage.show()                                     
    registerPage = Register()
    mainPage = Main()
    msg_box = QMessageBox()
    msg_box.setWindowTitle("tb")
    msg_box.setStyleSheet("background-color: white; color: none")
    inf_box = QMessageBox()
    inf_box.setStyleSheet("background-color: #F8F2EC; color: #356a9c")
    inf_box.setWindowTitle("error")
    inf_box.setIcon(QMessageBox.Icon.Warning)
    lbPage = lb()
    ldPage = ld()
    app.exec()