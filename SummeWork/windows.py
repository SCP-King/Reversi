import random

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
import sys
from PyQt5.QtWidgets import QFrame

qss='''

/* 设置按钮背景色为透明 */
QPushButton {
  background-color: transparent;
}

/* 设置按钮边框为无 */
QPushButton {
  border: none;
}


/* 设置按钮字体为白色，粗体，20像素 */
QPushButton {
  color: white;
  font-weight: bold;
  font-size: 40px;
}

/* 设置按钮在鼠标悬停时的背景色为渐变色，从左上角的绿色到右下角的紫色 */
QPushButton:hover {
  background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
    stop: 0 green, stop: 1 purple);
}

/* 设置按钮在鼠标按下时的背景色为红色 */
QPushButton:pressed {
  background-color: red;
}'''

class Menu(QWidget):
    def __init__(self):
        super(Menu,self).__init__()
        self.setWindowIcon(QIcon("./img/logo.jpg"))
        self.setWindowTitle("黑白棋游戏")
        self.setStyleSheet(qss)
        self.mode=None
        self.setFixedSize(1040,840)
        self.setup_ui()

    def setup_ui(self):
        Hbox=QVBoxLayout(self)
        Hbox.setSpacing(20)

        start=QPushButton(self)
        start.setText("开始游戏")
        end=QPushButton(self)
        end.setText("退出游戏")

        Hbox.addWidget(start)
        Hbox.addWidget(end)

        start.clicked.connect(self.b_start)
        end.clicked.connect(self.b_end)
        self.set_background_image()
        self.setLayout(Hbox)
    def b_start(self):
        self.mode=Mode()
        self.mode.show()
        self.close()
    def b_end(self):
        self.close()
    def set_background_image(self):
        pix = QPixmap("./img/menu.png").scaled(self.size())
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

class Mode(QWidget):
    def __init__(self):
        super(Mode,self).__init__()
        self.setWindowIcon(QIcon("./img/logo.jpg"))
        self.setWindowTitle("黑白棋游戏")
        self.setStyleSheet(qss)
        self.chessboard=None
        self.setFixedSize(1040,840)
        self.setup_ui()

    def setup_ui(self):
        Hbox = QVBoxLayout(self)
        Hbox.setSpacing(20)

        h_m=QPushButton(self)
        h_m.setText("人机对战")
        h_h=QPushButton(self)
        h_h.setText("人人对战")

        Hbox.addWidget(h_m)
        Hbox.addWidget(h_h)

        self.set_background_image()
        h_m.clicked.connect(self.start_h_m)
        h_h.clicked.connect(self.start_h_h)

        self.setLayout(Hbox)
    def start_h_m(self):
        self.chessboard=ChessBoard()
        self.chessboard.com=True
        self.chessboard.show()
        self.close()
    def start_h_h(self):
        self.chessboard=ChessBoard()
        self.chessboard.com=False
        self.chessboard.show()
        self.close()
    def set_background_image(self):
        pix = QPixmap("./img/menu.png").scaled(self.size())
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

class Chessman(QLabel):
    clicked = pyqtSignal(object)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(50,50)

    def setup_pixmap(self,user):
        if user == 0:
            pixmap = QPixmap('./img/whitepawns.png').scaled(self.size())
            self.setPixmap(pixmap)
            self.setScaledContents(True)
        elif user == 1:
            pixmap = QPixmap('./img/blackpawns.png').scaled(self.size())
            self.setPixmap(pixmap)
            self.setScaledContents(True)
        else:
            self.setPixmap(None)
            self.setScaledContents(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self)
        super().mousePressEvent(event)

class ChessBoard(QWidget):

    def __init__(self):
        super(ChessBoard,self).__init__()
        self.state = None
        self.file_path = None
        self.black_score = None
        self.white_score = None
        self.grid = None
        self.chess_frame = None
        self.chess_score=[]
        self.chess_label=[]
        self.note_label=None
        self.timer=None
        self.menu=None
        self.num=1
        self.numA=0
        self.numB=0
        self.A_moves=None
        self.B_moves=None
        self.com=False
        self.setWindowIcon(QIcon("./img/logo.jpg"))
        self.setWindowTitle("黑白棋游戏")
        self.setFixedSize(1040,840)
        self.set_background_image()
        self.setup_ui()

    def setup_ui(self):


        self.setup_chess_score()

        self.note_label=QLabel(self)
        self.note_label.move(900,30)
        self.note_label.setStyleSheet('''  
font-family: "Microsoft YaHei";
  font-style: italic;
  font-weight: bold;
  font-size: 30px;
  color: red;
  text-align: center;
  ''')
        self.note_label.setText("无法下棋")
        self.note_label.setVisible(False)
        self.timer=QTimer(self)

        user_frame=QFrame(self)


        chess_frame=QFrame(self)
        chess_frame.setFixedSize(556,560)
        chess_frame.move(400,185)
        grid=QGridLayout(chess_frame)
        grid.setSpacing(20)
        self.chess_frame = chess_frame
        self.grid = grid
        self.setup_chessboard()


        back=QPushButton(user_frame)
        back.setFixedSize(101,100)
        back.setIcon(QIcon("./img/back.png"))
        back.setIconSize(QSize(101,100))
        back.setStyleSheet("background-color: transparent;")
        back.clicked.connect(self.back_menu)

        self.state=QLabel(user_frame)
        self.state.setFixedSize(50,50)
        self.state.move(800,50)
        pixmap = QPixmap('./img/blackpawns.png').scaled(self.state.size())
        self.state.setPixmap(pixmap)

        user1=QLabel(user_frame)
        user2=QLabel(user_frame)
        user1.setFixedSize(66.5,97.3)
        user1.move(95,194)
        user2.setFixedSize(65.8,99.4)
        user2.move(98,474)
        pixmap = QPixmap('./img/user1.png').scaled(user1.size())
        user1.setPixmap(pixmap)
        user1.setScaledContents(True)
        pixmap = QPixmap('./img/user2.png').scaled(user2.size())
        user2.setPixmap(pixmap)
        user2.setScaledContents(True)
        black_score_label=QLabel(user_frame)
        black_score_label.setFixedSize(80,33)
        black_score_label.move(95,320)
        white_score_label = QLabel(user_frame)
        white_score_label.setFixedSize(80,33)
        white_score_label.move(95,600)
        pixmap = QPixmap('./img/score.png').scaled(black_score_label.size())
        black_score_label.setPixmap(pixmap)
        black_score_label.setScaledContents(True)
        pixmap = QPixmap('./img/score.png').scaled(white_score_label.size())
        white_score_label.setPixmap(pixmap)
        white_score_label.setScaledContents(True)
        user1_score=QLabel(user_frame)
        user2_score=QLabel(user_frame)
        user1_score.move(200,280)
        user2_score.move(200,460)
        user1_score.setFixedSize(200,100)
        user2_score.setFixedSize(200,300)
        user1_score.setStyleSheet('''  
    font-family: "Comic Sans MS";
    font-style: italic;
    font-weight: bold;
    font-size: 24px;
    color: yellow;
    text-align: center;
    background-color: transparent;''')
        user2_score.setStyleSheet('''  
    font-family: "Comic Sans MS";
    font-style: italic;
    font-weight: bold;
    font-size: 24px;
    color: yellow;
    text-align: center;
    background-color: transparent;''')

        self.black_score = user1_score
        self.white_score = user2_score


        self.A_moves=self.legal_positions(1)
        self.B_moves=self.legal_positions(0)




    def back_menu(self):
        self.menu=Menu()
        self.close()
        self.menu.show()



    def make_chess(self):
        chessman=self.sender()
        index=self.grid.indexOf(chessman)
        i=int(index/8)
        j=index%8
        if self.num % 2 !=0:
            if not (i,j) in self.A_moves:
                self.note_label.setVisible(True)
                self.timer.timeout.connect(lambda: self.note_label.setVisible(False))
                self.timer.start(2000)
                return
            self.numA=self.numA+1
            self.flip_pieces(i,j,1)
            chessman.setup_pixmap(1)
            self.chess_score[i][j]=1
        else:
            if not (i,j) in self.B_moves:
                self.note_label.setVisible(True)
                self.timer.timeout.connect(lambda: self.note_label.setVisible(False))
                self.timer.start(2000)
                return
            self.numB=self.numB+1
            self.flip_pieces(i, j, 0)
            chessman.setup_pixmap(0)
            self.chess_score[i][j]=0
        self.A_moves=self.legal_positions(1)
        self.B_moves=self.legal_positions(0)
        self.save_chess_record()
        self.check_res()
        self.num = self.num + 1
        if self.num%2 is not 0 and len(self.A_moves)<=0:
            self.num=self.num+1
        if self.num%2 is  0 and len(self.B_moves)<=0:
            self.num=self.num+1
        s1, s2 = self.calculate_score()
        self.black_score.setText(str(s1))
        self.white_score.setText(str(s2))
        if self.com and self.num%2 ==0:
            self.com_make_chess()
        if self.num%2==1:
            pixmap = QPixmap('./img/blackpawns.png').scaled(self.state.size())
            self.state.setPixmap(pixmap)
        else:
            pixmap = QPixmap('./img/whitepawns.png').scaled(self.state.size())
            self.state.setPixmap(pixmap)
    def com_make_chess(self):
        i,j=random.choice(self.B_moves)
        chessman=self.chess_label[i][j]
        self.numB = self.numB + 1
        self.flip_pieces(i, j, 0)
        chessman.setup_pixmap(0)
        self.chess_score[i][j] = 0
        self.A_moves = self.legal_positions(1)
        self.B_moves = self.legal_positions(0)
        self.save_chess_record()
        self.check_res()
        self.num = self.num + 1
        if self.num % 2 is not 0 and len(self.A_moves) <= 0:
            self.num = self.num + 1
            self.com_make_chess()
        if self.num % 2 is 0 and len(self.B_moves) <= 0:
            self.num = self.num + 1
        s1, s2 = self.calculate_score()
        self.black_score.setText(str(s1))
        self.white_score.setText(str(s2))


    def check_res(self):
        if self.check_over():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            black_score, white_score = self.calculate_score()
            if black_score > white_score:
                pixmap = QPixmap("./img/blackwin.png")
                msg_box.setIconPixmap(pixmap)
            elif black_score < white_score:
                pixmap=QPixmap("./img/whitewin.png")
                msg_box.setIconPixmap(pixmap)
            else:
                pixmap = QPixmap("./img/draw.png")
                msg_box.setIconPixmap(pixmap)
            msg_box.setWindowTitle("游戏结果")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.show()
            response = msg_box.exec_()
            if response == QMessageBox.Ok:
                self.menu=Menu()
                self.menu.show()
                self.close()
    def check_over(self):
        return len(self.A_moves)<=0 and len(self.B_moves)<=0

    def calculate_score(self):
        black_score = 0
        white_score = 0

        for i in range(8):
            for j in range(8):
                if self.chess_score[i][j] == 0:  # 白色棋子
                    white_score += 1
                elif self.chess_score[i][j] == 1:  # 黑色棋子
                    black_score += 1
        return black_score, white_score

    def setup_chess_score(self):
        self.chess_score=[]
        for i in range(8):
            a=[]
            for j in range(8):
                a.append(-1)
            self.chess_score.append(a)

    def legal_positions(self, color):
        # 定义一个空列表，用于存储合法坐标
        positions = []
        # 定义一个常量，表示棋盘的大小（假设是8*8）
        SIZE = 8
        # 定义一个列表，表示八个方向的偏移量
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # 遍历棋盘上的每个位置
        for i in range(SIZE):
            for j in range(SIZE):
                # 如果该位置为空，则判断是否为合法位置
                if self.chess_score[i][j] == -1:
                    # 对每个方向进行检查
                    for dx, dy in directions:
                        # 初始化一个变量，表示是否找到合法位置
                        found = False
                        # 初始化一个变量，表示当前检查的位置
                        x, y = i + dx, j + dy
                        # 如果当前位置在棋盘内，并且有不同颜色的棋子，则继续检查
                        while 0 <= x < SIZE and 0 <= y < SIZE and self.chess_score[x][y] != -1 and self.chess_score[x][
                            y] != color:
                            # 更新当前位置
                            x += dx
                            y += dy
                            # 如果当前位置在棋盘内，并且有相同颜色的棋子，则说明找到了合法位置
                            if 0 <= x < SIZE and 0 <= y < SIZE and self.chess_score[x][y] == color:
                                found = True
                                break
                        # 如果找到了合法位置，则将该空位的坐标加入到列表中，并跳出循环
                        if found:
                            positions.append((i, j))
                            break
        # 返回合法坐标的列表
        return positions

    def flip_pieces(self,row, column, color):
        # 检查位置是否为空
        if self.chess_score[row][column] != -1:
            return

        # 定义八个方向的偏移量
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # 棋子翻转
        for dr, dc in directions:
            r, c = row + dr, column + dc
            pieces_to_flip = []  # 可以翻转的棋子位置列表
            while 0 <= r < 8 and 0 <= c < 8:
                if self.chess_score[r][c] == -1:
                    break
                elif self.chess_score[r][c] == 1 - color:  # 对方的棋子
                    pieces_to_flip.append((r, c))
                elif self.chess_score[r][c] == color:  # 碰到自己的棋子，翻转路径上的棋子
                    for flip_row, flip_col in pieces_to_flip:
                        self.chess_score[flip_row][flip_col] = color
                        self.chess_label[flip_row][flip_col].setup_pixmap(color)
                    break
                r += dr
                c += dc

    def setup_chessboard(self):
        self.num=1
        self.numA=0
        self.numB=0
        self.setup_chess_score()
        self.chess_label = []
        for i in range(8):
            a=[]
            for j in range(8):
                if i == 3 and j == 4 or i == 4 and j == 3:
                    label = Chessman(self.chess_frame)
                    label.setup_pixmap(0)
                    self.chess_score[i][j] = 0
                elif i == 3 and j == 3 or i == 4 and j == 4:
                    label = Chessman(self.chess_frame)
                    label.setup_pixmap(1)
                    self.chess_score[i][j] = 1
                else:
                    label = Chessman(self.chess_frame)
                if self.grid.itemAtPosition(i, j) is not None:
                    widget=self.grid.itemAtPosition(i,j).widget()
                    self.grid.removeWidget(widget)
                    widget.deleteLater()
                label.clicked.connect(self.make_chess)
                a.append(label)
                self.grid.addWidget(label, i, j)
            self.chess_label.append(a)
        self.file_path = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        self.save_chess_record()
    def set_background_image(self):
        pix = QPixmap("./img/chessboard.jpg").scaled(self.size())
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    def save_chess_record(self):
        with open('./chess record/'+self.file_path+'.txt', 'a') as file:
            for row in self.chess_score:
                line = ' '.join(str(piece) for piece in row)
                file.write(line + '\n')
            file.write('\n')




if __name__ == '__main__':
    app=QApplication(sys.argv)
    m=Menu()
    m.show()
    sys.exit(app.exec_())
