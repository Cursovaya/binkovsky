import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
from pathlib import Path
import io

# Функция для получения относительного пути к ресурсам
def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\USER\PycharmProjects\pythonProject12\frame0")
    return ASSETS_PATH / Path(path)

# Создание базы данных
def create_db():
    conn = sqlite3.connect('hotel_booking.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, middle_name TEXT,
                  phone TEXT, email TEXT, login TEXT, password TEXT)''')

    # Таблица для администраторов
    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (id INTEGER PRIMARY KEY, login TEXT, password TEXT)''')

    # Таблица для отелей
    c.execute('''CREATE TABLE IF NOT EXISTS hotels
                 (id INTEGER PRIMARY KEY, name TEXT, address TEXT, description TEXT)''')

    # Таблица для фотографий отелей
    c.execute('''CREATE TABLE IF NOT EXISTS hotel_images
                 (id INTEGER PRIMARY KEY, hotel_id INTEGER, image BLOB,
                  FOREIGN KEY(hotel_id) REFERENCES hotels(id))''')

    # Таблица для номеров
    c.execute('''CREATE TABLE IF NOT EXISTS rooms
                 (id INTEGER PRIMARY KEY, hotel_id INTEGER, number TEXT, description TEXT,
                  price REAL, FOREIGN KEY(hotel_id) REFERENCES hotels(id))''')

    # Таблица для фотографий номеров
    c.execute('''CREATE TABLE IF NOT EXISTS room_images
                 (id INTEGER PRIMARY KEY, room_id INTEGER, image BLOB,
                  FOREIGN KEY(room_id) REFERENCES rooms(id))''')

    # Таблица для броней
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY, user_id INTEGER, room_id INTEGER, check_in DATE, check_out DATE,
                  FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(room_id) REFERENCES rooms(id))''')

    # Добавляем администратора
    c.execute("INSERT OR IGNORE INTO admin (login, password) VALUES ('admin', '12345')")

    conn.commit()
    conn.close()

# Проверка существования базы данных
def check_db_exists():
    if not Path('hotel_booking.db').exists():
        create_db()

check_db_exists()

# Функции для работы с базой данных
def get_db_connection():
    return sqlite3.connect('hotel_booking.db')

def register_user(first_name, last_name, middle_name, phone, email, login, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (first_name, last_name, middle_name, phone, email, login, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (first_name, last_name, middle_name, phone, email, login, password))
    conn.commit()
    conn.close()

def check_user(login, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    user = c.fetchone()
    conn.close()
    return user

def check_admin(login, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM admin WHERE login = ? AND password = ?", (login, password))
    admin = c.fetchone()
    conn.close()
    return admin

def get_hotels():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM hotels")
    hotels = c.fetchall()
    conn.close()
    return hotels

def add_hotel(name, address, description):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO hotels (name, address, description) VALUES (?, ?, ?)",
              (name, address, description))
    hotel_id = c.lastrowid
    conn.commit()
    conn.close()
    return hotel_id

def add_hotel_image(hotel_id, image_data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO hotel_images (hotel_id, image) VALUES (?, ?)",
              (hotel_id, image_data))
    conn.commit()
    conn.close()

def get_hotel_images(hotel_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT image FROM hotel_images WHERE hotel_id = ?", (hotel_id,))
    images = c.fetchall()
    conn.close()
    return images

def delete_hotel(hotel_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))
    c.execute("DELETE FROM hotel_images WHERE hotel_id = ?", (hotel_id,))
    conn.commit()
    conn.close()

def get_rooms(hotel_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM rooms WHERE hotel_id = ?", (hotel_id,))
    rooms = c.fetchall()
    conn.close()
    return rooms

def add_room(hotel_id, number, description, price):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO rooms (hotel_id, number, description, price) VALUES (?, ?, ?, ?)",
              (hotel_id, number, description, price))
    room_id = c.lastrowid
    conn.commit()
    conn.close()
    return room_id

def add_room_image(room_id, image_data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO room_images (room_id, image) VALUES (?, ?)",
              (room_id, image_data))
    conn.commit()
    conn.close()

def get_room_images(room_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT image FROM room_images WHERE room_id = ?", (room_id,))
    images = c.fetchall()
    conn.close()
    return images

def delete_room(room_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
    c.execute("DELETE FROM room_images WHERE room_id = ?", (room_id,))
    conn.commit()
    conn.close()

def book_room(user_id, room_id, check_in, check_out):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO bookings (user_id, room_id, check_in, check_out) VALUES (?, ?, ?, ?)",
              (user_id, room_id, check_in, check_out))
    conn.commit()
    conn.close()

def get_booking_by_user(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
    bookings = c.fetchall()
    conn.close()
    return bookings

def cancel_booking(booking_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

def get_all_bookings():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT b.id, u.first_name, u.last_name, u.middle_name, h.name, r.number, b.check_in, b.check_out, r.price FROM bookings b JOIN users u ON b.user_id = u.id JOIN rooms r ON b.room_id = r.id JOIN hotels h ON r.hotel_id = h.id")
    bookings = c.fetchall()
    conn.close()
    return bookings

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система бронирования отелей")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#FFFFFF")

        self.canvas = tk.Canvas(
            self.root,
            bg="#FFFFFF",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(960.0, 540.0, image=self.image_image_1)

        self.canvas.create_rectangle(514.0, 121.0, 1424.0, 1004.0, fill="#FFFFFF", outline="")

        self.canvas.create_text(
            683.0,
            250.0,
            anchor="nw",
            text="Добро пожаловать в систему бронирования отелей!\n",
            fill="#000000",
            font=("Gugi Regular", 24 * -1)
        )

        # Текст "Логин"
        self.canvas.create_text(
            580.0,
            396.0,
            anchor="nw",
            text="Логин:",
            fill="#000000",
            font=("Gugi Regular", 64 * -1)
        )

        # Текст "Пароль"
        self.canvas.create_text(
            560.0,
            555.0,
            anchor="nw",
            text="Пароль:",
            fill="#000000",
            font=("Gugi Regular", 64 * -1)
        )

        # Поле ввода для логина
        self.entry_image_1 = tk.PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(1082.0, 449.5, image=self.entry_image_1)
        self.login_entry = tk.Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.login_entry.place(x=862.0, y=424.0, width=440.0, height=49.0)

        # Поле ввода для пароля
        self.entry_image_2 = tk.PhotoImage(file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(1087.5, 596.0, image=self.entry_image_2)
        self.password_entry = tk.Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            show="*"
        )
        self.password_entry.place(x=862.0, y=572.0, width=451.0, height=46.0)

        # Кнопка "Вход как клиент"
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login_user,
            relief="flat"
        )
        self.button_1.place(x=560.0, y=677.0, width=352.0, height=142.0)

        # Кнопка "Вход как администратор"
        self.button_image_2 = tk.PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = tk.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.login_admin,
            relief="flat"
        )
        self.button_2.place(x=1054.0, y=677.0, width=314.0, height=143.0)

        # Кнопка "Регистрация"
        self.button_image_3 = tk.PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.register,
            relief="flat"
        )
        self.button_3.place(x=723.0, y=853.0, width=463.0, height=105.0)

        # Дополнительный текст
        self.canvas.create_text(
            704.0,
            321.0,
            anchor="nw",
            text="Мы рады вас видеть! Спасибо, что выбрали нас!",
            fill="#000000",
            font=("LexendZetta Regular", 24 * -1)
        )

        # Белый прямоугольник для оформления
        self.canvas.create_rectangle(922.0, 142.0, 1054.0, 235.0, fill="#FFFFFF", outline="")

    def login_user(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        if user := check_user(login, password):
            self.user_id = user[0]  # Сохраняем ID пользователя
            self.user_dashboard(user[1], user[2])  # Передаем имя и фамилию пользователя
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def login_admin(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        if check_admin(login, password):
            self.admin_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def register(self):

        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Регистрация")
        self.register_window.geometry("400x400")

        tk.Label(self.register_window, text="Имя:").grid(row=0, column=0, padx=10, pady=10)
        self.first_name_entry = tk.Entry(self.register_window)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Фамилия:").grid(row=1, column=0, padx=10, pady=10)
        self.last_name_entry = tk.Entry(self.register_window)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Отчество:").grid(row=2, column=0, padx=10, pady=10)
        self.middle_name_entry = tk.Entry(self.register_window)
        self.middle_name_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Телефон:").grid(row=3, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.register_window)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Email:").grid(row=4, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.register_window)
        self.email_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Логин:").grid(row=5, column=0, padx=10, pady=10)
        self.new_login_entry = tk.Entry(self.register_window)
        self.new_login_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self.register_window, text="Пароль:").grid(row=6, column=0, padx=10, pady=10)
        self.new_password_entry = tk.Entry(self.register_window, show="*")
        self.new_password_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(self.register_window, text="Зарегистрироваться", command=self.register_user).grid(row=7, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=20)

    def register_user(self):
        """Обрабатывает регистрацию пользователя."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        middle_name = self.middle_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        login = self.new_login_entry.get()
        password = self.new_password_entry.get()

        if not (first_name and last_name and login and password):
            messagebox.showerror("Ошибка", "Заполните обязательные поля")
            return

        register_user(first_name, last_name, middle_name, phone, email, login, password)
        messagebox.showinfo("Успех", "Вы успешно зарегистрировались")
        self.register_window.destroy()

    def user_dashboard(self, first_name, last_name):
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack(fill='both', expand=True)

        tk.Label(self.user_frame, text=f"Добро пожаловать, {first_name} {last_name}", font=("Arial", 29)).pack(pady=20)

        button_frame = tk.Frame(self.user_frame)
        button_frame.pack(expand=True)

        tk.Button(button_frame, text="Забронировать номер", command=self.book_room, font=("Arial", 29)).pack(pady=10,
                                                                                                             padx=20,
                                                                                                             side='left')
        tk.Button(button_frame, text="Проверить бронь", command=self.check_booking, font=("Arial", 29)).pack(pady=10,
                                                                                                             padx=20,
                                                                                                             side='left')

    def admin_dashboard(self):
        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack(fill='both', expand=True)

        tk.Label(self.admin_frame, text="Добро пожаловать, администратор", font=("Arial", 29)).pack(pady=20)

        button_frame = tk.Frame(self.admin_frame)
        button_frame.pack(expand=True)

        tk.Button(button_frame, text="Список отелей", command=self.manage_hotels, font=("Arial", 29)).pack(pady=10,
                                                                                                           padx=20,
                                                                                                           side='left')
        tk.Button(button_frame, text="Список пользователей", command=self.manage_users, font=("Arial", 29)).pack(
            pady=10, padx=20, side='left')
        tk.Button(button_frame, text="Проверить бронь", command=self.check_all_bookings, font=("Arial", 29)).pack(
            pady=10, padx=20, side='left')

    def logout(self):
        self.user_frame.pack_forget()
        self.admin_frame.pack_forget()
        self.login_frame.pack()
        messagebox.showinfo("Выход", "Вы вышли из системы")

    def book_room(self):
        hotel_frame = tk.Toplevel(self.root)
        hotel_frame.title("Выбор отеля")
        hotel_frame.geometry("400x300")

        hotels = get_hotels()
        for i, hotel in enumerate(hotels):
            tk.Button(hotel_frame, text=hotel[1], command=lambda h=hotel: self.show_hotel_details(h)).grid(row=i,
                                                                                                           column=0,
                                                                                                           pady=10)

        tk.Button(hotel_frame, text="Назад", command=hotel_frame.destroy).grid(row=len(hotels), column=0, pady=10)

    def show_hotel_details(self, hotel):
        details_frame = tk.Toplevel(self.root)
        details_frame.title(f"Отель: {hotel[1]}")
        details_frame.geometry("800x600")

        # Создаем пустые колонки для отступов слева и справа
        details_frame.grid_columnconfigure(0, weight=1)  # Левая пустая колонка
        details_frame.grid_columnconfigure(4, weight=1)  # Правая пустая колонка

        # Отображение фотографий отеля
        images = get_hotel_images(hotel[0])
        image_frame = tk.Frame(details_frame)
        image_frame.grid(row=0, column=1, columnspan=3, pady=20)  # Используем grid для image_frame

        # Центрирование изображения
        if images:
            try:
                image_data = images[0][0]  # Берем первое изображение
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((400, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=photo)
                image_label.image = photo
                image_label.grid(row=0, column=0, sticky="nsew")  # Используем grid для image_label
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

        # Отображение описания отеля
        description_frame = tk.Frame(details_frame)
        description_frame.grid(row=1, column=1, columnspan=3, pady=20)  # Используем grid для description_frame

        # Адрес сверху
        tk.Label(description_frame, text=f"Адрес: {hotel[2]}", font=("Arial", 14)).grid(row=0, column=0, sticky='w')

        # Описание внизу
        description_label = tk.Label(description_frame, text=f"Описание: {hotel[3]}", font=("Arial", 14),
                                     wraplength=400, justify='left')
        description_label.grid(row=3, column=0, sticky='w')

        # Кнопка "Номера" слева от текста
        tk.Button(description_frame, text="Номера", command=lambda: self.show_rooms(hotel[0]), font=("Arial", 14)).grid(
            row=1, column=1, padx=10)

        # Отображение суммы правее описания
        total_price = self.calculate_total_price(hotel[0])  # Пример функции для расчета суммы
        tk.Label(description_frame, text=f"Сумма: {total_price} руб.", font=("Arial", 14)).grid(row=1, column=2,
                                                                                                padx=10)

        # Кнопка "Назад" внизу окна
        tk.Button(details_frame, text="Назад", command=details_frame.destroy, font=("Arial", 14)).grid(row=2, column=1,
                                                                                                       columnspan=3,
                                                                                                       pady=20)

    def show_rooms(self, hotel_id):
        """Функция для отображения номеров отеля."""
        rooms_frame = tk.Toplevel(self.root)
        rooms_frame.title("Номера отеля")
        rooms_frame.geometry("600x400")

        rooms = get_rooms(hotel_id)
        for i, room in enumerate(rooms):
            tk.Button(rooms_frame, text=f"Номер: {room[2]}", command=lambda r=room: self.room_details(r),
                      font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=10)
            tk.Label(rooms_frame, text=f"Цена: {room[4]} руб.", font=("Arial", 14)).grid(row=i, column=1, padx=10,
                                                                                         pady=10)

        # Кнопка "Назад" внизу окна
        tk.Button(rooms_frame, text="Назад", command=rooms_frame.destroy, font=("Arial", 14)).grid(row=len(rooms),
                                                                                                   column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=20)

    def calculate_total_price(self, hotel_id):
        """Пример функции для расчета общей суммы."""
        rooms = get_rooms(hotel_id)
        total_price = sum(room[4] for room in rooms)
        return total_price

    def room_details(self, room):
        details_frame = tk.Toplevel(self.root)
        details_frame.title("Подробности номера")
        details_frame.geometry("400x400")

        tk.Label(details_frame, text=f"Номер: {room[2]}").grid(row=0, column=0, pady=10)
        tk.Label(details_frame, text=f"Описание: {room[3]}").grid(row=1, column=0, pady=10)
        tk.Label(details_frame, text=f"Цена за сутки: {room[4]} руб.").grid(row=2, column=0, pady=10)

        # Отображение фотографий номера
        images = get_room_images(room[0])
        for i, image_data in enumerate(images):
            try:
                image = Image.open(io.BytesIO(image_data[0]))
                image = image.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(details_frame, image=photo)
                image_label.image = photo
                image_label.grid(row=3 + i, column=0, pady=10)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

        tk.Label(details_frame, text="Дата заезда (YYYY-MM-DD):").grid(row=len(images) + 4, column=0, pady=10)
        check_in_entry = tk.Entry(details_frame)
        check_in_entry.grid(row=len(images) + 4, column=1, pady=10)

        tk.Label(details_frame, text="Дата выезда (YYYY-MM-DD):").grid(row=len(images) + 5, column=0, pady=10)
        check_out_entry = tk.Entry(details_frame)
        check_out_entry.grid(row=len(images) + 5, column=1, pady=10)

        def calculate_total():
            check_in_date = check_in_entry.get()
            check_out_date = check_out_entry.get()
            if not check_in_date or not check_out_date:
                messagebox.showerror("Ошибка", "Введите даты заезда и выезда")
                return

            total_days = (datetime.strptime(check_out_date, '%Y-%m-%d') - datetime.strptime(check_in_date,
                                                                                            '%Y-%m-%d')).days
            total_price = room[4] * total_days
            messagebox.showinfo("Итоговая сумма", f"Итоговая сумма за {total_days} дней: {total_price} руб.")

        tk.Button(details_frame, text="Рассчитать итог", command=calculate_total).grid(row=len(images) + 6, column=0,
                                                                                       pady=10)

        def book():
            check_in_date = check_in_entry.get()
            check_out_date = check_out_entry.get()
            if not check_in_date or not check_out_date:
                messagebox.showerror("Ошибка", "Введите даты заезда и выезда")
                return

            book_room(self.user_id, room[0], check_in_date, check_out_date)
            messagebox.showinfo("Успех", "Номер успешно забронирован")
            details_frame.destroy()

        tk.Button(details_frame, text="Забронировать", command=book).grid(row=len(images) + 6, column=1, pady=10)
        tk.Button(details_frame, text="Назад", command=details_frame.destroy).grid(row=len(images) + 7, column=0,
                                                                                   columnspan=2, pady=10)

    def check_booking(self):
        check_booking_frame = tk.Toplevel(self.root)
        check_booking_frame.title("Проверка брони")
        check_booking_frame.geometry("400x300")

        bookings = get_booking_by_user(self.user_id)
        if not bookings:
            messagebox.showinfo("Бронь", "У вас нет активных броней")
            return

        booking = bookings[0]
        room_id = booking[2]
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        room = c.fetchone()
        conn.close()

        total_days = (datetime.strptime(booking[4], '%Y-%m-%d') - datetime.strptime(booking[3], '%Y-%m-%d')).days
        total_price = room[4] * total_days

        tk.Label(check_booking_frame, text=f"Номер: {room[2]}").grid(row=0, column=0, pady=10)
        tk.Label(check_booking_frame, text=f"Дата заезда: {booking[3]}").grid(row=1, column=0, pady=10)
        tk.Label(check_booking_frame, text=f"Дата выезда: {booking[4]}").grid(row=2, column=0, pady=10)
        tk.Label(check_booking_frame, text=f"Итоговая сумма: {total_price} руб.").grid(row=3, column=0, pady=10)
        tk.Button(check_booking_frame, text="Отменить бронь", command=lambda b=booking[0]: self.cancel_booking(b)).grid(
            row=4, column=0, pady=10)
        tk.Button(check_booking_frame, text="Назад", command=check_booking_frame.destroy).grid(row=5, column=0, pady=10)

    def cancel_booking(self, booking_id):
        cancel_booking(booking_id)
        messagebox.showinfo("Успех", "Бронь успешно отменена")
        self.check_booking()

    def check_all_bookings(self):
        check_booking_frame = tk.Toplevel(self.root)
        check_booking_frame.title("Проверка всех броней")
        check_booking_frame.geometry("600x400")

        bookings = get_all_bookings()
        if not bookings:
            messagebox.showinfo("Бронь", "Нет активных броней")
            return

        for i, booking in enumerate(bookings):
            total_days = (datetime.strptime(booking[6], '%Y-%m-%d') - datetime.strptime(booking[7], '%Y-%m-%d')).days
            total_price = booking[8] * total_days

            tk.Label(check_booking_frame, text=f"Фамилия: {booking[1]}").grid(row=i * 5, column=0, pady=10)
            tk.Label(check_booking_frame, text=f"Имя: {booking[2]}").grid(row=i * 5 + 1, column=0, pady=10)
            tk.Label(check_booking_frame, text=f"Отель: {booking[4]}").grid(row=i * 5 + 2, column=0, pady=10)
            tk.Label(check_booking_frame, text=f"Номер: {booking[5]}").grid(row=i * 5 + 3, column=0, pady=10)
            tk.Label(check_booking_frame, text=f"Итоговая сумма: {total_price} руб.").grid(row=i * 5 + 4, column=0,
                                                                                           pady=10)

        tk.Button(check_booking_frame, text="Назад", command=check_booking_frame.destroy).grid(
            row=len(bookings) * 5 + 1, column=0, pady=10)

    def manage_hotels(self):
        hotel_frame = tk.Toplevel(self.root)
        hotel_frame.title("Управление отелями")
        hotel_frame.geometry("600x400")

        tk.Button(hotel_frame, text="Добавить отель", command=self.add_hotel).grid(row=0, column=0, pady=10)

        hotels = get_hotels()
        for i, hotel in enumerate(hotels):
            tk.Label(hotel_frame, text=f"{hotel[1]} - {hotel[2]}").grid(row=i + 1, column=0, pady=10)
            tk.Button(hotel_frame, text="Редактировать", command=lambda h=hotel[0]: self.edit_hotel(h)).grid(row=i + 1,
                                                                                                             column=1,
                                                                                                             pady=10)
            tk.Button(hotel_frame, text="Удалить", command=lambda h=hotel[0]: self.delete_hotel(h)).grid(row=i + 1,
                                                                                                         column=2,
                                                                                                         pady=10)
            tk.Button(hotel_frame, text="Управление номерами", command=lambda h=hotel[0]: self.manage_rooms(h)).grid(
                row=i + 1, column=3, pady=10)

        tk.Button(hotel_frame, text="Назад", command=hotel_frame.destroy).grid(row=len(hotels) + 1, column=0,
                                                                               columnspan=4, pady=10)

    def add_hotel(self):
        add_hotel_frame = tk.Toplevel(self.root)
        add_hotel_frame.title("Добавить отель")
        add_hotel_frame.geometry("400x300")

        tk.Label(add_hotel_frame, text="Название:").grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(add_hotel_frame)
        name_entry.grid(row=0, column=1, pady=10)

        tk.Label(add_hotel_frame, text="Адрес:").grid(row=1, column=0, pady=10)
        address_entry = tk.Entry(add_hotel_frame)
        address_entry.grid(row=1, column=1, pady=10)

        tk.Label(add_hotel_frame, text="Описание:").grid(row=2, column=0, pady=10)
        description_entry = tk.Entry(add_hotel_frame)
        description_entry.grid(row=2, column=1, pady=10)

        tk.Label(add_hotel_frame, text="Фото:").grid(row=3, column=0, pady=10)
        image_path_var = tk.StringVar()
        image_path_entry = tk.Entry(add_hotel_frame, textvariable=image_path_var)
        image_path_entry.grid(row=3, column=1, pady=10)

        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        tk.Button(add_hotel_frame, text="Загрузить фото", command=upload_image).grid(row=3, column=2, pady=10)

        tk.Button(add_hotel_frame, text="Сохранить",
                  command=lambda: self.save_hotel(name_entry.get(), address_entry.get(), description_entry.get(),
                                                  image_path_var.get(), add_hotel_frame)).grid(row=4, column=0,
                                                                                               columnspan=3, pady=10)

    def save_hotel(self, name, address, description, image_path, frame):
        if not name or not address:
            messagebox.showerror("Ошибка", "Заполните обязательные поля")
            return

        hotel_id = add_hotel(name, address, description)
        if image_path:
            # Читаем изображение и сохраняем его в базе данных
            with open(image_path, 'rb') as file:
                image_data = file.read()
                add_hotel_image(hotel_id, image_data)
        messagebox.showinfo("Успех", "Отель успешно добавлен")
        frame.destroy()

    def edit_hotel(self, hotel_id):
        edit_hotel_frame = tk.Toplevel(self.root)
        edit_hotel_frame.title("Редактировать отель")
        edit_hotel_frame.geometry("400x300")

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM hotels WHERE id = ?", (hotel_id,))
        hotel = c.fetchone()
        conn.close()

        tk.Label(edit_hotel_frame, text="Название:").grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(edit_hotel_frame)
        name_entry.insert(0, hotel[1])
        name_entry.grid(row=0, column=1, pady=10)

        tk.Label(edit_hotel_frame, text="Адрес:").grid(row=1, column=0, pady=10)
        address_entry = tk.Entry(edit_hotel_frame)
        address_entry.insert(0, hotel[2])
        address_entry.grid(row=1, column=1, pady=10)

        tk.Label(edit_hotel_frame, text="Описание:").grid(row=2, column=0, pady=10)
        description_entry = tk.Entry(edit_hotel_frame)
        description_entry.insert(0, hotel[3])
        description_entry.grid(row=2, column=1, pady=10)

        tk.Label(edit_hotel_frame, text="Фото:").grid(row=3, column=0, pady=10)
        image_path_var = tk.StringVar()
        image_path_entry = tk.Entry(edit_hotel_frame, textvariable=image_path_var)
        image_path_entry.grid(row=3, column=1, pady=10)

        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        tk.Button(edit_hotel_frame, text="Загрузить фото", command=upload_image).grid(row=3, column=2, pady=10)

        def save_changes():
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE hotels SET name = ?, address = ?, description = ? WHERE id = ?",
                      (name_entry.get(), address_entry.get(), description_entry.get(), hotel_id))

            # Удаляем старые фотографии и добавляем новую, если она была загружена
            if image_path_var.get():
                # Удаляем старые фотографии
                c.execute("DELETE FROM hotel_images WHERE hotel_id = ?", (hotel_id,))

                # Читаем новое изображение и сохраняем его в базе данных
                with open(image_path_var.get(), 'rb') as file:
                    image_data = file.read()
                    add_hotel_image(hotel_id, image_data)

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Отель успешно обновлен")
            edit_hotel_frame.destroy()

        tk.Button(edit_hotel_frame, text="Сохранить изменения", command=save_changes).grid(row=4, column=0,
                                                                                           columnspan=3, pady=10)

    def delete_hotel(self, hotel_id):
        if messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить отель?"):
            delete_hotel(hotel_id)
            messagebox.showinfo("Успех", "Отель успешно удален")

    def manage_rooms(self, hotel_id):
        room_frame = tk.Toplevel(self.root)
        room_frame.title("Управление номерами")
        room_frame.geometry("600x400")

        tk.Button(room_frame, text="Добавить номер", command=lambda: self.add_room(hotel_id)).grid(row=0, column=0,
                                                                                                   pady=10)

        rooms = get_rooms(hotel_id)
        for i, room in enumerate(rooms):
            tk.Label(room_frame, text=f"Номер: {room[2]}").grid(row=i + 1, column=0, pady=10)
            tk.Button(room_frame, text="Редактировать", command=lambda r=room: self.edit_room(r)).grid(row=i + 1,
                                                                                                       column=1,
                                                                                                       pady=10)
            tk.Button(room_frame, text="Удалить", command=lambda r=room[0]: self.delete_room(r)).grid(row=i + 1,
                                                                                                      column=2, pady=10)

        tk.Button(room_frame, text="Назад", command=room_frame.destroy).grid(row=len(rooms) + 1, column=0, columnspan=3,
                                                                             pady=10)

    def add_room(self, hotel_id):
        add_room_frame = tk.Toplevel(self.root)
        add_room_frame.title("Добавить номер")
        add_room_frame.geometry("400x300")

        tk.Label(add_room_frame, text="Номер:").grid(row=0, column=0, pady=10)
        number_entry = tk.Entry(add_room_frame)
        number_entry.grid(row=0, column=1, pady=10)

        tk.Label(add_room_frame, text="Описание:").grid(row=1, column=0, pady=10)
        description_entry = tk.Entry(add_room_frame)
        description_entry.grid(row=1, column=1, pady=10)

        tk.Label(add_room_frame, text="Цена за сутки:").grid(row=2, column=0, pady=10)
        price_entry = tk.Entry(add_room_frame)
        price_entry.grid(row=2, column=1, pady=10)

        tk.Label(add_room_frame, text="Фото:").grid(row=3, column=0, pady=10)
        image_path_var = tk.StringVar()
        image_path_entry = tk.Entry(add_room_frame, textvariable=image_path_var)
        image_path_entry.grid(row=3, column=1, pady=10)

        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        tk.Button(add_room_frame, text="Загрузить фото", command=upload_image).grid(row=3, column=2, pady=10)

        tk.Button(add_room_frame, text="Сохранить",
                  command=lambda: self.save_room(hotel_id, number_entry.get(), description_entry.get(),
                                                 price_entry.get(), image_path_var.get(), add_room_frame)).grid(row=4,
                                                                                                                column=0,
                                                                                                                columnspan=3,
                                                                                                                pady=10)

    def save_room(self, hotel_id, number, description, price, image_path, frame):
        if not number or not price:
            messagebox.showerror("Ошибка", "Заполните обязательные поля")
            return

        room_id = add_room(hotel_id, number, description, float(price))
        if image_path:
            # Читаем изображение и сохраняем его в базе данных
            with open(image_path, 'rb') as file:
                image_data = file.read()
                add_room_image(room_id, image_data)
        messagebox.showinfo("Успех", "Номер успешно добавлен")
        frame.destroy()

    def edit_room(self, room):
        edit_room_frame = tk.Toplevel(self.root)
        edit_room_frame.title("Редактировать номер")
        edit_room_frame.geometry("400x300")

        tk.Label(edit_room_frame, text="Номер:").grid(row=0, column=0, pady=10)
        number_entry = tk.Entry(edit_room_frame)
        number_entry.insert(0, room[2])
        number_entry.grid(row=0, column=1, pady=10)

        tk.Label(edit_room_frame, text="Описание:").grid(row=1, column=0, pady=10)
        description_entry = tk.Entry(edit_room_frame)
        description_entry.insert(0, room[3])
        description_entry.grid(row=1, column=1, pady=10)

        tk.Label(edit_room_frame, text="Цена за сутки:").grid(row=2, column=0, pady=10)
        price_entry = tk.Entry(edit_room_frame)
        price_entry.insert(0, room[4])
        price_entry.grid(row=2, column=1, pady=10)

        tk.Label(edit_room_frame, text="Фото:").grid(row=3, column=0, pady=10)
        image_path_var = tk.StringVar()
        image_path_entry = tk.Entry(edit_room_frame, textvariable=image_path_var)
        image_path_entry.grid(row=3, column=1, pady=10)

        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        tk.Button(edit_room_frame, text="Загрузить фото", command=upload_image).grid(row=3, column=2, pady=10)

        def save_changes():
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE rooms SET number = ?, description = ?, price = ? WHERE id = ?",
                      (number_entry.get(), description_entry.get(), float(price_entry.get()), room[0]))

            # Удаляем старые фотографии и добавляем новую, если она была загружена
            if image_path_var.get():
                # Удаляем старые фотографии
                c.execute("DELETE FROM room_images WHERE room_id = ?", (room[0],))

                # Читаем новое изображение и сохраняем его в базе данных
                with open(image_path_var.get(), 'rb') as file:
                    image_data = file.read()
                    add_room_image(room[0], image_data)

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Номер успешно обновлен")
            edit_room_frame.destroy()

        tk.Button(edit_room_frame, text="Сохранить изменения", command=save_changes).grid(row=4, column=0, columnspan=3,
                                                                                          pady=10)

    def delete_room(self, room_id):
        if messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить номер?"):
            delete_room(room_id)
            messagebox.showinfo("Успех", "Номер успешно удален")

    def manage_users(self):
        user_frame = tk.Toplevel(self.root)
        user_frame.title("Управление пользователями")
        user_frame.geometry("600x400")

        tk.Button(user_frame, text="Добавить пользователя", command=self.add_user).grid(row=0, column=0, pady=10)

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()

        for i, user in enumerate(users):
            tk.Label(user_frame, text=f"{user[1]} {user[2]}").grid(row=i + 1, column=0, pady=10)
            tk.Button(user_frame, text="Просмотреть", command=lambda u=user: self.view_user(u)).grid(row=i + 1,
                                                                                                     column=1, pady=10)
            tk.Button(user_frame, text="Удалить", command=lambda u=user[0]: self.delete_user(u)).grid(row=i + 1,
                                                                                                      column=2, pady=10)

        tk.Button(user_frame, text="Назад", command=user_frame.destroy).grid(row=len(users) + 1, column=0, columnspan=3,
                                                                             pady=10)

    def add_user(self):
        add_user_frame = tk.Toplevel(self.root)
        add_user_frame.title("Добавить пользователя")
        add_user_frame.geometry("400x300")

        tk.Label(add_user_frame, text="Имя:").grid(row=0, column=0, pady=10)
        first_name_entry = tk.Entry(add_user_frame)
        first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Фамилия:").grid(row=1, column=0, padx=10, pady=10)
        last_name_entry = tk.Entry(add_user_frame)
        last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Отчество:").grid(row=2, column=0, padx=10, pady=10)
        middle_name_entry = tk.Entry(add_user_frame)
        middle_name_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Телефон:").grid(row=3, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(add_user_frame)
        phone_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Email:").grid(row=4, column=0, padx=10, pady=10)
        email_entry = tk.Entry(add_user_frame)
        email_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Логин:").grid(row=5, column=0, padx=10, pady=10)
        login_entry = tk.Entry(add_user_frame)
        login_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(add_user_frame, text="Пароль:").grid(row=6, column=0, padx=10, pady=10)
        password_entry = tk.Entry(add_user_frame, show="*")
        password_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(add_user_frame, text="Сохранить",
                  command=lambda: self.save_user(first_name_entry.get(), last_name_entry.get(), middle_name_entry.get(),
                                                 phone_entry.get(), email_entry.get(), login_entry.get(),
                                                 password_entry.get(), add_user_frame)).grid(row=7, column=0,
                                                                                             columnspan=2, pady=10)

    def save_user(self, first_name, last_name, middle_name, phone, email, login, password, frame):
        if not (first_name and last_name and login and password):
            messagebox.showerror("Ошибка", "Заполните обязательные поля")
            return

        register_user(first_name, last_name, middle_name, phone, email, login, password)
        messagebox.showinfo("Успех", "Пользователь успешно добавлен")
        frame.destroy()

    def view_user(self, user):
        view_user_frame = tk.Toplevel(self.root)
        view_user_frame.title("Информация о пользователе")
        view_user_frame.geometry("400x300")

        tk.Label(view_user_frame, text=f"Имя: {user[1]}").grid(row=0, column=0, pady=10)
        tk.Label(view_user_frame, text=f"Фамилия: {user[2]}").grid(row=1, column=0, pady=10)
        tk.Label(view_user_frame, text=f"Отчество: {user[3]}").grid(row=2, column=0, pady=10)
        tk.Label(view_user_frame, text=f"Телефон: {user[4]}").grid(row=3, column=0, pady=10)
        tk.Label(view_user_frame, text=f"Email: {user[5]}").grid(row=4, column=0, pady=10)

        tk.Button(view_user_frame, text="Закрыть", command=view_user_frame.destroy).grid(row=5, column=0, pady=10)

    def delete_user(self, user_id):
        if messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить пользователя?"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Пользователь успешно удален")


# Основной код программы
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    root.mainloop()