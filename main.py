from copy import copy
from PyQt5 import QtCore,QtWidgets,uic
import pytchat
import sys,time
from PyQt5.QtCore import QPoint,QThread
from PyQt5.QtGui import QImage,QPixmap,QIntValidator
from windowcap import windowCapture
from detector import preprocess
import cv2
import pyautogui as pt


cordinates=[]
cordi_vote=[]
viewers=[]

runningtime=False
bestVote=None

class main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.ui=uic.loadUi('window.ui',self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mainSet.clicked.connect(self.mainSettings)
        self.gameSet.clicked.connect(self.gameSettings)
        self.minimized.clicked.connect(self.showMinimized)
        self.done.clicked.connect(self.runchat)
        self.stop.clicked.connect(self.stopchat)
        self.Close.clicked.connect(self.close)
        self.capwin.clicked.connect(self.capboard)
        self.pass_T.setValidator(QIntValidator())
        self.pass_C.setValidator(QIntValidator())
        self.off_x.setValidator(QIntValidator())
        self.off_y.setValidator(QIntValidator())
        self.bstart_x.setValidator(QIntValidator())
        self.bstart_y.setValidator(QIntValidator())
        self.b_width.setValidator(QIntValidator())
        self.b_height.setValidator(QIntValidator())
        self.progressBar_1.setValue(0)
        self.progressBar_2.setValue(0)
        self.progressBar_3.setValue(0)
        self.offset=None
        self.show()
    
    def runchat(self):
        self.textEdit.setText("")
        self.chat=ytchat(self.yt_id.text())
        self.chat.start()
        self.done.setEnabled(False)
        self.stop.setEnabled(True)
        self.stop.setStyleSheet("QPushButton{background-color: rgb(255, 85, 0);border:0px;}")
        self.done.setStyleSheet("QPushButton{background-color: rgb(154, 154, 154);border:0px;}")
        self.chat.ytchatmessage.connect(self.chatout)
    
    def period(self,tim):
        global runningtime
        mins,secs=divmod(tim,60)
        t='{:02d}:{:02d}'.format(mins,secs)
        self.lcdNumber.display(t)
        
        if tim==0:
            runningtime=False
            self.timer.stop()
            self.RunmoveDupe()
            

    def RunmoveDupe(self):
        if ((int(self.bstart_x.text())!=0)and(int(self.bstart_y.text())!=0)):
            if self.whiteSide.isChecked():
                side=True
            elif self.BlackSide.isChecked():
                side=False
            self.moveDupe=moveDupe(self.win_cap.text(),self.off_x.text(),self.off_y.text(),self.bstart_x.text(),self.bstart_y.text(),
            self.b_width.text(),self.b_height.text(),bestVote,side)
            self.moveDupe.start()
            time.sleep(0.5)
            self.reset_()

    def reset_(self):
        global cordinates
        global cordi_vote
        global viewers
        cordinates=[]
        cordi_vote=[]
        viewers=[]
        self.progressBar_1.setValue(0)
        self.progressBar_2.setValue(0)
        self.progressBar_3.setValue(0)
        self.first_m.setText("1st")
        self.second_m.setText("2nd")
        self.third_m.setText("3rd")
        self.lcdNumber.display(self.pass_T.text())
        self.lcdNumber_2.display("0")

    def stopchat(self):
        global runningtime
        self.chat.stop()
        if runningtime==True:
            self.timer.stop()
            runningtime=False
        self.done.setStyleSheet("QPushButton{background-color: rgb(255, 85, 0);border:0px;}")
        self.stop.setStyleSheet("QPushButton{background-color: rgb(154, 154, 154);border:0px;}")
        self.stop.setEnabled(False)
        self.done.setEnabled(True)
        self.reset_()

    def capboard(self):
        self.win=wincap(self.win_cap.text())
        self.win.start()
        self.win.boardgeometry.connect(self.inprint)

    def inprint(self,winsx,winsy,borx,bory,w,h):
        self.off_x.setText(str(winsx))
        self.off_y.setText(str(winsy))
        self.bstart_x.setText(str(borx))
        self.bstart_y.setText(str(bory))
        self.b_width.setText(str(w))
        self.b_height.setText(str(h))
        
        if((w!=0)and(h!=0)):
            time.sleep(0.08)
            pixmap=QPixmap("board.png")
            self.cap_img.setScaledContents(True)
            self.cap_img.setPixmap(pixmap)
        else:
            self.cap_img.setText("Board finding Error")

    def mainSettings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.mainSet.setStyleSheet("background-color:rgb(255, 85, 0);border:0px;")
        self.ui.gameSet.setStyleSheet("QPushButton{background-color: rgb(33, 43, 51);border:0px;}QPushButton:hover{background-color: rgb(255, 85, 0);}")
    
    def gameSettings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.lcdNumber.display(self.pass_T.text())
        self.ui.gameSet.setStyleSheet("background-color:rgb(255, 85, 0);border:0px;")
        self.ui.mainSet.setStyleSheet("QPushButton{background-color: rgb(33, 43, 51);border:0px;}QPushButton:hover{background-color: rgb(255, 85, 0);}")

    def mousePressEvent(self,event):
        self.oldPosition=event.globalPos()

    def mouseMoveEvent(self,event):
        delta=QPoint(event.globalPos()-self.oldPosition)
        self.move(self.x() + delta.x(),self.y() + delta.y())
        self.oldPosition=event.globalPos()
    
    def chatout(self,message):
        global runningtime
        if (len(message)==1):
            self.textEdit.append(message[0])
            if message[0]=="Connection error!":
                self.stopchat()
                self.textEdit.append("Restarting process")
                time.sleep(1)
                self.runchat()
        else:
            self.textEdit.append(message[0])
            if self.onetimeon.isChecked():
                if not(message[2] in viewers):
                    viewers.append(message[2])
                    self.Vfilter=chatcomandpro(message[1])
                    self.Vfilter.start()
                    time.sleep(0.5)
                    self.Commndshow=votefilter()
                    self.Commndshow.start()
                else:
                    self.textEdit.append(f"{message[2]} Alread Voted!")
            elif self.onetimeoff.isChecked():
                self.Vfilter=chatcomandpro(message[1])
                self.Vfilter.start()
                time.sleep(0.5)
                self.Commndshow=votefilter()
                self.Commndshow.start()

            self.Commndshow.vote.connect(self.progressbar)
            if runningtime==False:
                if self.typetime.isChecked():
                    self.timer=timer(self.pass_T.text())
                    self.timer.start()
                    runningtime=True
                    self.timer.tim.connect(self.period) 
    
    def progressbar(self,firstname,secondname,thirdname,firstval,secondval,thirdval,votesum):
        global bestVote
        self.lcdNumber_2.display(votesum)
        if self.typecount.isChecked():
            votesum=int(self.pass_C.text())
        self.progressBar_1.setValue(int((firstval/votesum)*100))
        self.progressBar_2.setValue(int((secondval/votesum)*100))
        self.progressBar_3.setValue(int((thirdval/votesum)*100))
        self.first_m.setText((firstname).upper())
        self.second_m.setText((secondname).upper())
        self.third_m.setText((thirdname).upper())
        bestVote=firstname
        if self.typecount.isChecked():
            if (votesum==int(self.pass_C.text())):
                self.RunmoveDupe()


    def close(self):
        sys.exit()

class ytchat(QThread):
    ytchatmessage=QtCore.pyqtSignal(list)
    def __init__(self,ytid=None):
        super(ytchat,self).__init__()
        self.ytid=ytid
        self.Notrunning=False
        try:
            self.pychat=pytchat.create(video_id=self.ytid)
        except:
            self.ytchatmessage.emit(["Youtube ID invalid!"])

    def run(self):
        try:
            self.ytchatmessage.emit([">>>Strating...."])
            while self.pychat.is_alive:
                if (self.Notrunning):
                    self.ytchatmessage.emit([">>>Terminated...."])
                    break
                try:
                    for c in self.pychat.get().items:
                        arr=[]
                        if(len(c.message)<25):
                            com=c.message.replace(" ","")
                            first_c=com.find("<")
                            if (first_c!=-1):
                                last_c=com.find(">")
                                word=(com[first_c+1:last_c]).lower()
                                if ((len(word))==4):
                                    letter_1=word[0]
                                    num_1=word[1]
                                    letter_2=word[2]
                                    num_2=word[3]
                                    if (num_1.isdigit() and num_2.isdigit() and (0<int(num_1)<=8) and (0<int(num_2)<=8) 
                                    and (ord('a')<=ord(letter_1)<=ord('h')) and (ord('a')<=ord(letter_2)<=ord('h'))):
    
                                        if not c.author.name in viewers:
                                            arr.append(f"{c.datetime} [{c.author.name}] - Done")
                                            arr.append(word)
                                            arr.append(c.author.name)
                                            self.ytchatmessage.emit(arr)
                                    else:
                                        arr.append(f"{c.datetime} [{c.author.name}] - invalid")
                                        self.ytchatmessage.emit(arr)
                            else:
                                arr.append(f"[{c.author.name}] - {c.message}")
                                self.ytchatmessage.emit(arr)
                                time.sleep(0.8)
                except:
                    self.ytchatmessage.emit(["Connection error!"])
                    break
        except:
            self.ytchatmessage.emit(["Runtime Error! "])

    def stop(self):
        self.Notrunning=True
        #self.terminate()

class wincap(QThread):
    chessboard=QtCore.pyqtSignal(QImage)
    boardgeometry=QtCore.pyqtSignal(int,int,int,int,int,int)
    def __init__(self,windowname=None):
        super(wincap,self).__init__()
        self.windowname=windowname
    
    def run(self):
        try:
            self.wincap=windowCapture(self.windowname)
            image,winStartX,winStartY=self.wincap.get_screenshot()
            contours=preprocess(image).contoursfind()
            biggestContour=preprocess(contours=contours).biggestContour()

            if biggestContour.size!=0:
                bstartx,bstarty,w,h=cv2.boundingRect(biggestContour)
                cropImage=image[bstarty:bstarty+h, bstartx:bstartx+w]
            cv2.imwrite("board.png",cropImage)
            self.boardgeometry.emit(winStartX,winStartY,bstartx,bstarty,w,h)
        except:
            self.boardgeometry.emit(0,0,0,0,0,0)

class timer(QThread):
    tim=QtCore.pyqtSignal(int)
    def __init__(self,limit):
        super(timer,self).__init__()
        self.limit=int(limit)
    
    def run(self):
        self.ThreadActive=True
        coun=self.limit
        while (True):
            self.tim.emit(coun)
            time.sleep(1)
            coun-=1
            if (coun<0):
                coun=coun=int(self.limit)
    
    def stop(self):
        self.ThreadActive=False
        self.terminate()

class chatcomandpro(QThread):
    def __init__(self,command):
        super(chatcomandpro,self).__init__()
        self.command=command
            
    def run(self):
        self.ThreadActive=True
        if not self.command in cordinates:
            cordinates.append(self.command)
            cordi_vote.append(0)
        for x in range(len(cordinates)):
            if self.command==cordinates[x]:
                cordi_vote[x]=cordi_vote[x]+1
    
    def stop(self):
        self.ThreadActive=False
        self.terminate()

class votefilter(QThread):
    vote=QtCore.pyqtSignal(str,str,str,int,int,int,int)
    def __init__(self):
        super(votefilter,self).__init__()
    
    def run(self):
        time.sleep(0.6)
        arrval=copy(cordi_vote)
        arrnam=copy(cordinates)
        secondname="null"
        thirdname="null"
        secondval=0
        thirdval=0

        if 1<=len(arrval):
            for x in range(len(arrnam)):
                if arrval[x]==max(arrval):
                    firstname=arrnam[x]
                    firstval=arrval[x]
                    arrnam.remove(arrnam[x])
                    arrval.remove(arrval[x])
                    break
            for x in range(len(arrnam)):
                if arrval[x]==max(arrval):
                    secondname=arrnam[x]
                    secondval=arrval[x]
                    arrnam.remove(arrnam[x])
                    arrval.remove(arrval[x])
                    break
            for x in range(len(arrnam)):
                if arrval[x]==max(arrval):
                    thirdname=arrnam[x]
                    thirdval=arrval[x]
                    arrnam.remove(arrnam[x])
                    arrval.remove(arrval[x])
                    break
        self.vote.emit(firstname,secondname,thirdname,firstval,secondval,thirdval,sum(cordi_vote))

class moveDupe(QThread):
    def __init__(self,window=None,WstartX=0,WstartY=0,BstartX=0,BstartY=0,Bwidth=0,Bheight=0,command=None,whiteS=True):
        super(moveDupe,self).__init__()
        self.window=window
        self.WstartX=int(WstartX)
        self.WstartY=int(WstartY)
        self.BstartX=int(BstartX)
        self.BstartY=int(BstartY)
        self.Bwidth=int(Bwidth)
        self.Bheight=int(Bheight)
        self.command=command
        self.white=whiteS

    
    def run(self):
        self.win=windowCapture(self.window)

        if self.white==True:
            side="white"
        else:
            side="black"

        start_x=(self.Bwidth/16)
        start_y=(self.Bheight/16)
        x_space=(self.Bwidth/8)
        y_space=(self.Bheight/8)

        for i in range(0,6,2):
            if (i<3):
                letter=self.command[i]
                number=self.command[i+1]
            else:
                letter=self.command[0]
                number=self.command[1]

            self.win.activatewin()

            if (side=="white"):
                match letter:
                    case "a":
                        x_cordi=start_x
                    case "b":
                        x_cordi=start_x + x_space
                    case "c":
                        x_cordi=start_x + x_space*2
                    case "d":
                        x_cordi=start_x + x_space*3
                    case "e":
                        x_cordi=start_x + x_space*4
                    case "f":
                        x_cordi=start_x + x_space*5
                    case "g":
                        x_cordi=start_x + x_space*6
                    case "h":
                        x_cordi=start_x + x_space*7
            elif (side=="black"):
                match letter:
                    case "h":
                        x_cordi=start_x
                    case "g":
                        x_cordi=start_x + x_space
                    case "f":
                        x_cordi=start_x + x_space*2
                    case "e":
                        x_cordi=start_x + x_space*3
                    case "d":
                        x_cordi=start_x + x_space*4
                    case "c":
                        x_cordi=start_x + x_space*5
                    case "b":
                        x_cordi=start_x + x_space*6
                    case "a":
                        x_cordi=start_x + x_space*7
            if (side=="white"):
                match number:
                    case "8":
                        y_cordi=start_y
                    case "7":
                        y_cordi=start_y + y_space
                    case "6":
                        y_cordi=start_y + y_space*2
                    case "5":
                        y_cordi=start_y + y_space*3
                    case "4":
                        y_cordi=start_y + y_space*4
                    case "3":
                        y_cordi=start_y + y_space*5
                    case "2":
                        y_cordi=start_y + y_space*6
                    case "1":
                        y_cordi=start_y + y_space*7
            elif (side=="black"):
                match number:
                    case "1":
                        y_cordi=start_y
                    case "2":
                        y_cordi=start_y + y_space
                    case "3":
                        y_cordi=start_y + y_space*2
                    case "4":
                        y_cordi=start_y + y_space*3
                    case "5":
                        y_cordi=start_y + y_space*4
                    case "6":
                        y_cordi=start_y + y_space*5
                    case "7":
                        y_cordi=start_y + y_space*6
                    case "8":
                        y_cordi=start_y + y_space*7

            pt.moveTo(int(x_cordi)+self.WstartX+self.BstartX,int(y_cordi)+self.WstartY+self.BstartY)
            time.sleep(0.1)
            pt.click()
            time.sleep(1)

app=QtWidgets.QApplication(sys.argv)
mainWindow=main()

sys.exit(app.exec_())