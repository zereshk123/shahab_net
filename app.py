import sys
import re
import sqlite3
import json
import datetime
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

# read config file
try:
    with open("./config/config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("خطا در بارگذاری فایل config:", e)

def db(query, params=()):
    with sqlite3.connect("./config/database.db") as conn:
        crs = conn.cursor()
        crs.execute(query, params)
        res = crs.fetchall()
        conn.commit()

    return res

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("شهاب نت | ورود و ثبت نام")
        self.setWindowIcon(QIcon("./assets/tab_icon.png"))
        self.move(500, 150)
        self.setMinimumWidth(400)
        self.adjustSize()

        file = QFile("./style.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            text_stram = QTextStream(file)
            stylesheet = text_stram.readAll()
        self.setStyleSheet(stylesheet)


        self.lyt = QVBoxLayout(self)
        self.stacked_lyt = QStackedLayout()

        self.login_widget = self.create_login_form()
        self.register_widget = self.create_register_form()

        self.stacked_lyt.addWidget(self.login_widget)
        self.stacked_lyt.addWidget(self.register_widget)

        self.lyt.addLayout(self.stacked_lyt)

    def create_login_form(self):
        widget = QWidget()
        lyt = QVBoxLayout()

        label = QLabel("ورود به حساب کاربری")
        label.setObjectName("auth_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        self.login_username = QLineEdit()
        self.login_username.setObjectName("auth_inp") 
        self.login_username.setPlaceholderText("نام کاربری")
        lyt.addWidget(self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setObjectName("auth_inp")
        self.login_password.setPlaceholderText("رمز عبور")
        self.login_password.setEchoMode(QLineEdit.Password)
        lyt.addWidget(self.login_password)

        login_btn = QPushButton("ورود")
        login_btn.setObjectName("auth_btn")
        login_btn.clicked.connect(self.__login)
        lyt.addWidget(login_btn)

        switch_to_register = QPushButton("حساب ندارید؟ ثبت نام کنید")
        switch_to_register.setObjectName("auth_btn")
        switch_to_register.clicked.connect(self.show_register)
        lyt.addWidget(switch_to_register)


        widget.setLayout(lyt)
        return widget

    def create_register_form(self):
        widget = QWidget()
        lyt = QVBoxLayout()

        label = QLabel("ساخت حساب جدید")
        label.setObjectName("auth_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        name_lyt = QHBoxLayout()
        self.register_name = QLineEdit()
        self.register_name.setObjectName("auth_inp")
        self.register_name.setPlaceholderText("نام")
        self.register_family = QLineEdit()
        self.register_family.setObjectName("auth_inp")
        self.register_family.setPlaceholderText("نام خانوادگی")
        name_lyt.addWidget(self.register_name, 1)
        name_lyt.addWidget(self.register_family, 1)
        lyt.addLayout(name_lyt)

        self.register_username = QLineEdit()
        self.register_username.setObjectName("auth_inp")
        self.register_username.setPlaceholderText("نام کاربری")
        lyt.addWidget(self.register_username, 1)

        self.register_city = QComboBox()
        self.register_city.setObjectName("auth_inp")
        for city in data["cities"]:
            self.register_city.addItem(city)
        lyt.addWidget(self.register_city, 1)

        self.register_date = QLineEdit()
        self.register_date.setObjectName("auth_inp")
        self.register_date.setPlaceholderText("تاریخ تولد  |  yyyy/MM/dd")
        lyt.addWidget(self.register_date, 1)

        self.register_gender = QComboBox()
        self.register_gender.setObjectName("auth_inp")
        self.register_gender.addItem("مرد")
        self.register_gender.addItem("زن")
        lyt.addWidget(self.register_gender, 1)

        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setObjectName("auth_inp")
        self.register_password.setPlaceholderText("رمز عبور")
        lyt.addWidget(self.register_password)

        register_button = QPushButton("ثبت نام")
        register_button.setObjectName("auth_btn")
        register_button.clicked.connect(self.__register)
        lyt.addWidget(register_button)

        switch_to_login = QPushButton("حساب دارید؟ وارد شوید")
        switch_to_login.setObjectName("auth_btn")
        switch_to_login.clicked.connect(self.show_login)
        lyt.addWidget(switch_to_login)

        widget.setLayout(lyt)
        return widget

    def show_register(self):
        self.stacked_lyt.setCurrentWidget(self.register_widget)

    def show_login(self):
            self.stacked_lyt.setCurrentWidget(self.login_widget)

    def __login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        if len(username) == 0 or len(password) == 0:
                    user_id = 1
                    self.hide()
                    self.main_window = MainWindow(user_id)
                    self.main_window.show()
                    return

        if len(username) < 3:
            QMessageBox.critical(self, "خطا در نام کاربری", "لطفا یک نام کاربری معتبر وارد کنید.")
            return
        
        if len(password) < 5:
            QMessageBox.critical(self, "خطا در رمز عبور", "حداقل تعداد کارکتر های رمز عبور 5 حرف می باشد!")
            return
        
        with sqlite3.connect("./config/database.db") as conn:
            crs = conn.cursor()
            crs.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = crs.fetchone()
            if not user:
                QMessageBox.critical(self, "خطا در ورود", "اطلاعات وارد شده اشتباه می باشد!")
                return
            user_id = user[0]

        self.hide()
        self.main_window = MainWindow(user_id)
        self.main_window.show()
        
    def __register(self):
        name = self.register_name.text()
        family = self.register_family.text()
        username = self.register_username.text()
        city = self.register_city.currentText()
        date = self.register_date.text()
        gender = self.register_gender.currentText()
        password = self.register_password.text()
        
        pattern = r"^\d{4}/\d{2}/\d{2}$"

        if len(name) < 3 or len(family) < 3:
            QMessageBox.critical(self, "خطا در اطلاعات", "نام و نام خانوادگی باید حداقل 3 کاراکتر باشند.")
            return

        if len(username) < 3:
            QMessageBox.critical(self, "خطا در اطلاعات", "نام کاربری باید حداقل 3 کاراکتر باشد.")
            return

        with sqlite3.connect("./config/database.db") as conn:
            crs = conn.cursor()
            crs.execute("SELECT username FROM users")
            old_username = [row[0] for row in crs.fetchall()]
            conn.commit()

        for use_username in old_username:
            if use_username == username:
                QMessageBox.critical(self, "خطا در اطلاعات", "نام کاربری وارد شده قبلا استفاده شده است!")
                return
            
        if not bool(re.match(pattern, date)) or not self.validate_date(date):
            QMessageBox.critical(self, "خطا در اطلاعات", "فیلد تاریخ تولد معتبر نمی باشد!")
            return

        if len(password) < 5:
            QMessageBox.critical(self, "خطا در رمز عبور", "رمز عبور باید حداقل 5 کاراکتر باشد.")
            return

        with sqlite3.connect("./config/database.db") as conn:
            crs = conn.cursor()

            crs.execute("INSERT INTO users (name, family, username, gender, city, date_of_birth, password) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, family, username, gender, city, date, password))
            conn.commit()

            user_id = crs.lastrowid

        QMessageBox.information(self, "ثبت‌ نام موفق", "ثبت‌ نام با موفقیت انجام شد!")
        self.hide()
        self.main_window = MainWindow(user_id)
        self.main_window.show()

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y/%m/%d")
            return True
        except ValueError:
            return False

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("شهاب نت | صفحه اصلی")
        self.setWindowIcon(QIcon("./assets/tab_icon.png"))
        self.move(500, 150)
        self.adjustSize()
        
        self.user_id = user_id
        self.reply_to_msg_id = None
        self.reply_to_msg_txt = None

        file = QFile("./style.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            text_stream = QTextStream(file)
            stylesheet = text_stream.readAll()
            self.setStyleSheet(stylesheet)
    
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("toolbar")
        self.addToolBar(self.toolbar)
        action_home = QAction(QIcon(), "🏠 صفحه اصلی", self)
        action_logout = QAction(QIcon(), "🚪 خروج از حساب", self)
        action_home.triggered.connect(lambda: self.go_home())
        action_logout.triggered.connect(lambda: self.__logout())
        self.toolbar.addAction(action_home)
        self.toolbar.addAction(action_logout)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = self.home()
        self.stack.addWidget(self.home)

        self.show_friend = self.create_friend_list()
        self.stack.addWidget(self.show_friend)

        self.request_list = self.create_request_list()
        self.stack.addWidget(self.request_list)

        self.add_friend_widget = self.create_add_friend()
        self.stack.addWidget(self.add_friend_widget)
        
        self.chat_list = self.create_chat_list()
        self.stack.addWidget(self.chat_list)

        self.chat_page = self.create_chat_page()
        self.stack.addWidget(self.chat_page)

        self.my_post = self.create_my_post()
        self.stack.addWidget(self.my_post)

        self.new_post = self.create_new_post()
        self.stack.addWidget(self.new_post)

    def home(self):
        user = db("SELECT * FROM users WHERE id = ?", (self.user_id,))
        name = user[0][1]

        widget = QWidget()
        lyt = QVBoxLayout()

        welcome_label = QLabel(f"{name} عزیز، خوش آمدی👋")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("titr_label")
        lyt.addWidget(welcome_label, stretch=1)

        btn_lyt_1 = QHBoxLayout()
        btn_1 = QPushButton("👥 دوستان من")
        btn_1.setObjectName("home_btn")
        btn_1.clicked.connect(self.go_show_friend)
        btn_lyt_1.addWidget(btn_1, stretch=1)
        btn_2 = QPushButton("📩 درخواست های من")
        btn_2.clicked.connect(self.go_request_list)
        btn_2.setObjectName("home_btn")
        btn_lyt_1.addWidget(btn_2, stretch=1)
        lyt.addLayout(btn_lyt_1)
        
        btn_lyt_2 = QHBoxLayout()
        btn_1 = QPushButton("🤝 ارسال درخواست دوستی")
        btn_1.clicked.connect(self.go_create_add_friend)
        btn_1.setObjectName("home_btn")
        btn_lyt_2.addWidget(btn_1, stretch=1)
        btn_2 = QPushButton("📤 ارسال پیام")
        btn_2.clicked.connect(lambda: self.go_send_msg())
        btn_2.setObjectName("home_btn")
        btn_lyt_2.addWidget(btn_2, stretch=1)
        lyt.addLayout(btn_lyt_2)

        btn_lyt_3 = QHBoxLayout()
        btn_1 = QPushButton("📝 پست های من")
        btn_1.setObjectName("home_btn")
        btn_1.clicked.connect(lambda: self.go_my_post())
        btn_lyt_3.addWidget(btn_1, stretch=1)
        btn_2 = QPushButton("➕ پست جدید")
        btn_2.setObjectName("home_btn")
        btn_2.clicked.connect(lambda: self.go_new_post())
        btn_lyt_3.addWidget(btn_2, stretch=1)
        lyt.addLayout(btn_lyt_3)

        btn_lyt_4 = QHBoxLayout()
        btn_1 = QPushButton("🔍 اکسپلور")
        btn_1.setObjectName("home_btn")
        btn_lyt_4.addWidget(btn_1, stretch=1)
        lyt.addLayout(btn_lyt_4)

        widget.setLayout(lyt)
        return widget


    def create_friend_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        lyt = QVBoxLayout(content_widget)

        friend_relations = db("SELECT * FROM friends WHERE user_id_1 = ? OR user_id_2 = ?", (self.user_id, self.user_id))

        friend_list = []
        for relation in friend_relations:
            friend_id = relation[1] if relation[1] != self.user_id else relation[2]
            friend = db("SELECT * FROM users WHERE id = ?", (friend_id,))
            if friend and friend[0] != self.user_id:
                friend_list.append(friend[0])

        friend_label = QLabel("👥 دوستان من")
        friend_label.setObjectName("titr_label")
        friend_label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(friend_label)

        if friend_list:
            for friend in friend_list:
                frame = QFrame()
                frame.setObjectName("friend_box")
                frame_lyt = QHBoxLayout(frame)

                info = QLabel(f"نام: {friend[1]} {friend[2]} | نام کاربری: {friend[3]} | جنسیت: {friend[4]} | شهر: {friend[5]}")
                info.setObjectName("info_label")
                frame_lyt.addWidget(info, stretch=1)

                remove_btn = QPushButton("🗑️ حذف")
                remove_btn.clicked.connect(lambda _, fid=friend[0]: self.__remove_friend(fid))
                remove_btn.setObjectName("remove_btn")
                frame_lyt.addWidget(remove_btn)

                frame.setLayout(frame_lyt)
                lyt.addWidget(frame)
        else:
            img_label = QLabel()
            pixmap = QPixmap("./assets/empty.png")
            img_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setStyleSheet("margin-top: 50px;")
            img_label.setAlignment(Qt.AlignCenter)

            none_label = QLabel("شما هیچ دوستی ندارید...")
            none_label.setAlignment(Qt.AlignCenter)
            none_label.setObjectName("label")

            lyt.addWidget(img_label)
            lyt.addWidget(none_label)

        lyt.addStretch()
        scroll.setWidget(content_widget)
        return scroll
    
    def __remove_friend(self, friend_id):
        reply = QMessageBox.question(self, "حذف دوست", "آیا از حذف این دوست اطمینان دارید؟", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            db("DELETE FROM friends WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)", (self.user_id, friend_id, friend_id, self.user_id))
            db("DELETE FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)", (self.user_id, friend_id, friend_id, self.user_id))

            self.refe_app(1)


    def create_request_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        lyt = QVBoxLayout(content_widget)

        label = QLabel("📩 درخواست های من")
        label.setObjectName("titr_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        requests = db("SELECT * FROM friend_requests WHERE receiver_id = ?", (self.user_id,))

        if requests:
            for request in requests:
                frame = QFrame()
                frame.setObjectName("frame")
                frame_lyt = QHBoxLayout(frame)

                user_data = db("SELECT id, name FROM users WHERE id = ?", (request[1],))
                if user_data and len(user_data) > 0:
                    user = user_data[0]

                info = QLabel(f"کاربر '{user[1]}' به شما درخواست دوستی داده است")
                info.setObjectName("info_label")
                frame_lyt.addWidget(info)

                accept_btn = QPushButton("👍 قبول")
                accept_btn.setObjectName("accept_btn")
                accept_btn.clicked.connect(lambda: self.__accept_request(user[0]))
                frame_lyt.addWidget(accept_btn)

                reject_btn = QPushButton("👎 رد")
                reject_btn.setObjectName("reject_btn")
                reject_btn.clicked.connect(lambda: self.__reject_request(user[0]))
                frame_lyt.addWidget(reject_btn)

                frame.setLayout(frame_lyt)
                lyt.addWidget(frame)
        else:
            img_label = QLabel()
            pixmap = QPixmap("./assets/empty.png")
            img_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setStyleSheet("margin-top: 50px;")
            img_label.setAlignment(Qt.AlignCenter)

            none_label = QLabel("هیچ درخواستی برای شما ارسال نشده است...")
            none_label.setAlignment(Qt.AlignCenter)
            none_label.setObjectName("label")

            lyt.addWidget(img_label)
            lyt.addWidget(none_label)

        lyt.addStretch()
        scroll.setWidget(content_widget)
        return scroll

    def __accept_request(self, sender_id):
        request = db("SELECT * FROM friend_requests WHERE sender_id = ? AND receiver_id = ?", (sender_id, self.user_id))

        if request:
            if self.user_id > sender_id:
                id_1 = self.user_id
                id_2 = sender_id
            else:
                id_1 = sender_id
                id_2 = self.user_id

            db("INSERT INTO friends (user_id_1, user_id_2) VALUES (?, ?)", (id_1, id_2))
            db("DELETE FROM friend_requests WHERE sender_id = ? AND receiver_id = ?", (sender_id, self.user_id))
        else:
            QMessageBox.critical(self, "خطا", "چنین درخواستی ثبت نشده است.")
            return
        
        QMessageBox.information(self, "✅", "درخواست دوستی با موفقیت قبول شد.")
        self.refe_app(2)

    def __reject_request(self, sender_id):
        db("DELETE FROM friend_requests WHERE sender_id = ? AND receiver_id = ?", (sender_id, self.user_id))

        QMessageBox.information(self, "✅", "درخواست دوستی با موفقیت رد شد.")
        self.refe_app(2)


    def create_add_friend(self):
        widget = QWidget()
        lyt = QVBoxLayout()

        current_user = db("SELECT * FROM users WHERE id = ?", (self.user_id,))
        if current_user and len(current_user) > 0:
            current_user = current_user[0]

        users = db("SELECT * FROM users WHERE id != ? AND id NOT IN (SELECT CASE WHEN user_id_1 = ? THEN user_id_2 ELSE user_id_1 END FROM friends WHERE user_id_1 = ? OR user_id_2 = ?) AND id NOT IN (SELECT receiver_id FROM friend_requests WHERE sender_id = ?)", (self.user_id, self.user_id, self.user_id, self.user_id, self.user_id))

        current_user_year = int(current_user[6].split("/")[0])
        like_list = []

        for user in users:
            if len(like_list) < 5:
                user_year = int(user[6].split("/")[0])

                if user[5] == current_user[5] or user_year - current_user_year <= 5 or current_user[5] == user[5]:
                    like_list.append(user)


        send_re_lyt = QHBoxLayout()
        create_add_friend_label = QLabel("💠 نام کاربری کاربر مد نظر خود را وارد کنید:")
        create_add_friend_label.setObjectName("label")
        lyt.addWidget(create_add_friend_label)

        username_inp = QLineEdit()
        username_inp.setObjectName("inp")
        username_inp.setPlaceholderText("نام کاربری:")
        send_re_lyt.addWidget(username_inp)
        
        send_re_btn = QPushButton("ارسال درخواست")
        send_re_btn.setObjectName("send_re_btn")
        send_re_btn.clicked.connect(lambda: self.__send_friend_request(username_inp.text()))
        send_re_lyt.addWidget(send_re_btn)
        lyt.addLayout(send_re_lyt)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        lyt.addSpacing(20)
        lyt.addWidget(separator)
        lyt.addSpacing(20)


        like_user_label = QLabel("👥 کاربران با مشخصات مشابه با شما:")
        like_user_label.setObjectName("label")
        lyt.addWidget(like_user_label)
        for user in like_list:
            frame = QFrame()
            frame.setObjectName("user_box")
            user_lyt = QHBoxLayout(frame)

            info = QLabel(f"{user[1]} {user[2]} | نام کاربری: {user[3]} | شهر: {user[5]}")
            user_lyt.addWidget(info)

            request_btn = QPushButton("ارسال درخواست")
            request_btn.setObjectName("send_re_btn")
            request_btn.clicked.connect(lambda: self.__send_friend_request(user[3]))
            user_lyt.addWidget(request_btn)

            lyt.addWidget(frame)

        widget.setLayout(lyt)
        return widget

    def __send_friend_request(self, username):
        if len(username) < 3:
            QMessageBox.critical(self, "خطا در اطلاعات", "نام کاربری باید حداقل 3 کاراکتر باشد.")
            return

        with sqlite3.connect("./config/database.db") as conn:
            crs = conn.cursor()
            crs.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = crs.fetchone()
            if not user:
                QMessageBox.critical(self, "خطا در اطلاعات", "کاربری با این نام کاربری یافت نشد.")
                return
            conn.commit()

            crs.execute("SELECT * FROM friend_requests WHERE sender_id = ? AND receiver_id = ?", (self.user_id, user[0]))
            request = crs.fetchone()
            if request:
                QMessageBox.critical(self, "خطا در اطلاعات", "درخواست قبلا ارسال شده است.")
                return
            
            crs.execute("SELECT * FROM friends WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)", (self.user_id, user[0], user[0], self.user_id))
            friend = crs.fetchone()
            if friend:
                QMessageBox.critical(self, "خطا در اطلاعات", "این کاربر قبلا دوست شما است.")
                return
            
            crs.execute("INSERT INTO friend_requests (sender_id, receiver_id, status, created_at) VALUES (?, ?, ?, ?)", (self.user_id, user[0], "pending", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

        QMessageBox.information(self, "ارسال درخواست موفق", "درخواست شما ارسال شد، در صورت قبول کردن درخواست این کاربر در بخش دوستان قابل مشاهده است.")
        self.refe_app(3)


    def create_chat_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        lyt = QVBoxLayout(content_widget)

        label = QLabel("💬 گفتگو با دوستان")
        label.setObjectName("titr_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        friend_relations = db("SELECT * FROM friends WHERE user_id_1 = ? OR user_id_2 = ?", (self.user_id, self.user_id))

        if not friend_relations:
            img_label = QLabel()
            pixmap = QPixmap("./assets/empty.png")
            img_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setStyleSheet("margin-top: 50px;")
            img_label.setAlignment(Qt.AlignCenter)

            none_label = QLabel("شما هنوز دوستی ندارید...")
            none_label.setObjectName("label")
            none_label.setAlignment(Qt.AlignCenter)
            
            lyt.addWidget(img_label)
            lyt.addWidget(none_label)
        else:
            for relation in friend_relations:
                friend_id = relation[1] if relation[1] != self.user_id else relation[2]
                friend = db("SELECT * FROM users WHERE id = ?", (friend_id,))
                
                if friend:
                    friend = friend[0]
                    frame = QFrame()
                    frame.setObjectName("friend_box")
                    frame_lyt = QHBoxLayout(frame)

                    info = QLabel(f"{friend[1]} {friend[2]}")
                    info.setObjectName("info_label")
                    frame_lyt.addWidget(info, stretch=1)

                    chat_btn = QPushButton("💬 چت کردن")
                    chat_btn.setObjectName("send_re_btn")
                    chat_btn.clicked.connect(lambda checked, f_id=friend[0]: self.open_chat(f_id))
                    frame_lyt.addWidget(chat_btn)

                    frame.setLayout(frame_lyt)
                    lyt.addWidget(frame)

        lyt.addStretch()
        scroll.setWidget(content_widget)
        return scroll

    def create_chat_page(self):
        widget = QWidget()
        self.chat_layout = QVBoxLayout(widget)

        # --- Header ---
        header = QWidget()
        header_layout = QHBoxLayout(header)
        self.chat_user_label = QLabel()
        self.chat_user_label.setObjectName("titr_label")
        header_layout.addWidget(self.chat_user_label)

        back_btn = QPushButton("🔙 بازگشت")
        back_btn.setObjectName("send_re_btn")
        back_btn.clicked.connect(lambda: self.go_chat_list())
        header_layout.addWidget(back_btn)

        self.chat_layout.addWidget(header)

        # --- Messages Area ---
        self.messages_area = QScrollArea()
        self.messages_area.setWidgetResizable(True)
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.addStretch()
        self.messages_area.setWidget(self.messages_widget)

        # --- Reply Widget ---
        self.reply_widget = QWidget()
        self.reply_widget.hide()
        reply_layout = QHBoxLayout(self.reply_widget)
        reply_layout.setContentsMargins(5, 5, 5, 5)

        self.reply_label = QLabel()
        self.reply_label.setObjectName("reply_label")
        reply_layout.addWidget(self.reply_label)

        self.cancel_btn = QPushButton("❌")
        self.cancel_btn.setFixedSize(24, 24)
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setStyleSheet("background-color: transparent; border: none;")
        self.cancel_btn.clicked.connect(self.__cancel_reply)
        reply_layout.addWidget(self.cancel_btn)
        reply_layout.addStretch()

        # --- Middle Layout (messages + reply) ---
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.addWidget(self.messages_area)
        middle_layout.addWidget(self.reply_widget)
        self.chat_layout.addWidget(middle_widget)

        # --- Input Area ---
        input_layout = QHBoxLayout()
        self.message_input = QTextEdit()
        self.message_input.setObjectName("inp")
        self.message_input.setPlaceholderText("پیام خود را بنویسید...")
        self.message_input.setMaximumHeight(70)
        input_layout.addWidget(self.message_input)

        send_btn = QPushButton("📤 ارسال")
        send_btn.setObjectName("send_re_btn")
        send_btn.clicked.connect(self.__send_message)
        input_layout.addWidget(send_btn)

        self.chat_layout.addLayout(input_layout)

        return widget

    def open_chat(self, friend_id):
        self.current_chat_friend = friend_id
        friend = db("SELECT * FROM users WHERE id = ?", (friend_id,))[0]
        self.chat_user_label.setText(f"{friend[1]} {friend[2]}")
        
        self.load_messages()
        self.stack.setCurrentIndex(5)

    def load_messages(self):
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        messages = db("SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY timestamp", (self.user_id, self.current_chat_friend, self.current_chat_friend, self.user_id))

        for msg in messages:
            is_mine = msg[1] == self.user_id

            outer_frame = QFrame()
            outer_layout = QHBoxLayout(outer_frame)
            outer_layout.setContentsMargins(0, 0, 0, 0)
            outer_layout.setAlignment(Qt.AlignLeft if is_mine else Qt.AlignRight)

            message_frame = QFrame()
            message_frame.setObjectName("msg_box")
            message_layout = QVBoxLayout(message_frame)
            message_layout.setContentsMargins(8, 4, 8, 4)

            if msg[5]:
                reply_result = db("SELECT msg FROM messages WHERE id = ?", (msg[5],))
                if reply_result:
                    reply_text = reply_result[0][0]
                    reply_lbl = QLabel(f"🔁 {reply_text[:40]}...")
                    reply_lbl.setObjectName("reply_label_msg")
                    message_layout.addWidget(reply_lbl)

            message_btn = QPushButton(msg[3])
            message_btn.setFlat(True)
            message_btn.setCursor(Qt.PointingHandCursor)
            message_btn.setStyleSheet("text-align: left;")

            if is_mine:
                message_btn.clicked.connect(lambda checked, m_id=msg[0]: self.__del_msg(m_id))
            
            if not is_mine:
                message_btn.clicked.connect(lambda checked, m_id=msg[0], m_text=msg[3]: self.__prepare_reply(m_id, m_text))

            message_layout.addWidget(message_btn)
            message_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

            outer_layout.addWidget(message_frame)
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, outer_frame)

    def __prepare_reply(self, msg_id, msg_txt):
        self.reply_to_msg_id = msg_id
        self.reply_to_msg_txt = msg_txt
        self.reply_label.setText(f"🔁 پاسخ به: {msg_txt[:40]}...")
        self.reply_widget.show()

    def __cancel_reply(self):
        self.reply_to_msg_id = None
        self.reply_to_text = None
        self.message_input.setPlaceholderText("پیام خود را بنویسید...")
        self.reply_widget.hide()
        self.refe_app(5)
   
    def __del_msg(self, msg_id):
        que_res = QMessageBox.question(self, "حذف پیام", "آیا شما مطمئن هستید میخواید این پیام را حذف کنید؟", QMessageBox.Yes | QMessageBox.No)

        if que_res == QMessageBox.Yes:
            db("DELETE FROM messages WHERE id = ?", (msg_id,))
            self.load_messages()

    def __send_message(self):
        message = self.message_input.toPlainText().strip()
        if self.reply_to_msg_id:
            reply_id = self.reply_to_msg_id
        else:
            reply_id = None

        if message:
            db("INSERT INTO messages (sender_id, receiver_id, msg, timestamp, reply_to) VALUES (?, ?, ?, ?, ?)", (self.user_id, self.current_chat_friend, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reply_id))

            self.reply_to_msg_id = None
            self.reply_to_msg_txt = None
            self.reply_widget.hide()
            self.message_input.clear()
            self.load_messages()


    def create_my_post(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        lyt = QVBoxLayout(content_widget)

        label = QLabel("📝 پست های من")
        label.setObjectName("titr_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        posts = db("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at", (self.user_id,))

        if posts:
            for post in posts:
                frame = QFrame()
                frame_lyt = QVBoxLayout(frame)

                conte = QLabel(post[2])
                conte.setObjectName("label")
                conte.setWordWrap(True)
                frame_lyt.addWidget(conte)

                timestamp = QLabel(post[3])
                timestamp.setObjectName("date_label")
                frame_lyt.addWidget(timestamp)

                delete_btn = QPushButton("🗑️ حذف پست")
                delete_btn.setObjectName("remove_btn")
                delete_btn.clicked.connect(lambda checked, p_id=post[0]: self.__delete_post(p_id))
                frame_lyt.addWidget(delete_btn)

                frame.setObjectName("frame")
                lyt.addWidget(frame)
        else:
            img_label = QLabel()
            pixmap = QPixmap("./assets/empty.png")
            img_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img_label.setStyleSheet("margin-top: 50px;")
            img_label.setAlignment(Qt.AlignCenter)

            none_label = QLabel("شما هنوز هیچ پستی ندارید...")
            none_label.setAlignment(Qt.AlignCenter)
            none_label.setObjectName("label")
            
            lyt.addWidget(img_label)
            lyt.addWidget(none_label)

        lyt.addStretch()
        scroll.setWidget(content_widget)
        return scroll

    def __delete_post(self, post_id):
        res = QMessageBox.question(self, "ℹ", "آیا شما مطمئن هستید میخواهید این پست را حذف کنید؟", QMessageBox.Yes | QMessageBox.No)
        
        if res == QMessageBox.Yes:
            db("DELETE FROM posts WHERE id = ?", (post_id,))

            self.refe_app(6)


    def create_new_post(self):
        widget = QWidget()
        lyt = QVBoxLayout(widget)

        label = QLabel("➕ پست جدید")
        label.setObjectName("titr_label")
        label.setAlignment(Qt.AlignCenter)
        lyt.addWidget(label)

        self.post_conte = QTextEdit()
        self.post_conte.setObjectName("inp")
        self.post_conte.setPlaceholderText("متن پست را وارد کنید...")
        lyt.addWidget(self.post_conte)

        btn = QPushButton("➕ ارسال پست")
        btn.setObjectName("send_re_btn")
        btn.clicked.connect(lambda: self.__send_post())
        lyt.addWidget(btn)

        widget.setLayout(lyt)
        return widget

    def __send_post(self):
        post_conte = self.post_conte.toPlainText().strip()

        if len(post_conte) < 5:
            QMessageBox.critical(self, "خطا", "شما باید حداقل 5 حرف برای متن پست خود وارد کنید.")
            return
        
        db("INSERT INTO posts (user_id, content, created_at) VALUES(?, ?, ?)", (self.user_id, post_conte, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        QMessageBox.information(self, "✅", "پست شما با موفقیت ارسال شد.")
        self.refe_app(7)


    def refe_app(self, current_page):
        old_widget = self.stack.widget(1)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_friend_list()
        self.stack.insertWidget(1, new_widget)

        old_widget = self.stack.widget(2)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_request_list()
        self.stack.insertWidget(2, new_widget)

        old_widget = self.stack.widget(3)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_add_friend()
        self.stack.insertWidget(3, new_widget)

        old_widget = self.stack.widget(4)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_chat_list()
        self.stack.insertWidget(4, new_widget)

        old_widget = self.stack.widget(6)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_my_post()
        self.stack.insertWidget(6, new_widget)

        old_widget = self.stack.widget(7)
        self.stack.removeWidget(old_widget)
        old_widget.deleteLater()
        new_widget = self.create_new_post()
        self.stack.insertWidget(7, new_widget)

        self.stack.setCurrentIndex(current_page)

    def go_home(self):
        self.stack.setCurrentIndex(0)

    def go_show_friend(self):
        self.stack.setCurrentIndex(1)

    def go_request_list(self):
        self.stack.setCurrentIndex(2)

    def go_create_add_friend(self):
        self.stack.setCurrentIndex(3)
        
    def go_send_msg(self):
        self.stack.setCurrentIndex(4)

    def go_chat_list(self):
        self.stack.setCurrentIndex(4)

    def go_my_post(self):
        self.stack.setCurrentIndex(6)

    def go_new_post(self):
        self.stack.setCurrentIndex(7)


    def __logout(self):
                    self.hide()
                    self.auth_window = AuthWindow()
                    self.auth_window.show()
                    return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())