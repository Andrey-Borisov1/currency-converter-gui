from tkinter import *
from tkinter import ttk
import requests

url = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")


def print_xml(value, find):
    url_json = url.json()
    return url_json["Valute"][value][find]


def main_window():
    url_json = url.json()
    root = Tk()
    root.title("Конвертор валют")
    root.geometry("900x600")
    root.resizable(width=False, height=False)
    icon_image = PhotoImage(file="coin.png")
    root.iconphoto(False, icon_image)
    root["bg"] = "black"
    style = ttk.Style()

    label_main_menu = Label(
        root,
        text="Конвертер валют v1.0 Выберите действие:",
        font=("Comic Sans", 40),
        bg="#DAE500",
    )
    label_main_menu.pack()

    style.theme_use("default")
    style.configure(
        "list_value.TButton",
        background="red",
        font=("Comic Sans", 30),
        foreground="white",
    )

    def open_info_value():
        root.destroy()

        # создаем второе окно
        second = Tk()
        second.title("Список валют и дополнительная информация")
        second.resizable(width=False, height=False)
        second.geometry("860x700")
        second["bg"] = "black"

        # функция "Назад"
        def go_back():
            second.destroy()
            main_window()

        # ======= Прокручиваемая область =======
        container = Frame(second, bg="black")
        container.pack(fill="both", expand=True)

        canvas = Canvas(container, bg="black", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="black")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # ======================================

        # Создание списка валют

        for value in url_json["Valute"]:
            result = f"{value} {print_xml(value, 'Name')}, ID: {print_xml(value, 'ID')}, Цифровой код: {print_xml(value, 'NumCode')}, Номинал: {print_xml(value, 'Nominal')}"
            list_label = Label(
                scrollable_frame,
                text=result,
                bg="#18E618",
                fg="white",
                font=("Comic Sans", 20),
            )
            list_label.pack(fill="x", pady=2)

        # Кнопка "Назад"
        back_btn = Button(
            second,
            text="Назад",
            font=("Comic Sans", 30),
            command=go_back,
        )
        back_btn.pack()

        second.mainloop()

    # Кнопки главного окна
    button_list = ttk.Button(
        root,
        text="[1] Вывести список и дополнительную информацию о валютах",
        style="list_value.TButton",
        command=open_info_value,
    )
    button_list.pack()

    # Создание кнопки перевода
    def open_do_value():
        root.withdraw()
        second = Toplevel(root)
        second.title("Перевод валют")
        second.resizable(width=False, height=False)
        second.geometry("700x600")
        second["bg"] = "black"
        label_offer = Label(
            second,
            text='Ввидите валюту и сумму(пример: "AUD/RUB 100")',
            font=("Comic Sans", 30),
            bg="#DAE500",
        )
        label_offer.pack()

        def do_value():
            try:
                from_value = select_from.get()
                to_value = select_to.get()
                count_from = float(entry.get())
                if from_value == "RUB":
                    label_result.config(
                        text=f'Вот перевод: {round(count_from / print_xml(to_value, "Value"), 2)}'
                    )
                elif to_value == "RUB":
                    label_result.config(
                        text=f'Вот перевод: {round(count_from * print_xml(from_value, "Value"), 2)}'
                    )
                else:
                    to_rub = print_xml(from_value, "Value") * count_from
                    label_result.config(
                        text=f'Вот перевод: {round(to_rub / print_xml(to_value, "Value"), 2)}'
                    )
            except ValueError:
                label_result.config(text="Неправильный формат ввода")

        list_value = [print_xml(i, "CharCode") for i in url_json["Valute"]]
        list_value.append("RUB")
        # Поле выбора из какой валюты
        select_from = StringVar(
            value="Выберите валюту, из которой вы хотите получить перевод"
        )
        select_from_menu = OptionMenu(second, select_from, *list_value)
        select_from_menu.pack(pady=5, padx=20)
        # Поле выбора в какую валюту
        select_to = StringVar(
            value="Выберите валюту, в которую вы хотите получить перевод"
        )
        select_to_menu = OptionMenu(second, select_to, *list_value)
        select_to_menu.pack(pady=5, padx=40)
        # Поле ввода количества валют
        entry = Entry(second, width=60)
        entry.pack(pady=10)
        # Кнопка перевода
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "result_value.TButton",
            background="#BFF806",
            font=("Comic Sans", 20),
            foreground="white",
        )
        button_do = ttk.Button(
            second, text="Перевод", command=do_value, style="result_value.TButton"
        )
        button_do.pack(pady=5)
        # Вывод результата
        label_result = Label(second, text="", bg="green")
        label_result.pack(pady=10)

        def go_back():
            second.destroy()
            root.deiconify()

        back_btn = Button(
            second,
            text="Назад",
            font=("Comic Sans", 25),
            command=go_back,
        )
        back_btn.pack(pady=10)

    style.configure(
        "do_value.TButton",
        background="green",
        font=("Comic Sans", 30),
        foreground="white",
    )
    button_value = ttk.Button(
        root,
        text="[2] Перевести валюту",
        style="do_value.TButton",
        command=open_do_value,
    )
    button_value.pack()

    # Создаем функцию для выхода
    def open_sure():
        root.destroy()

        # создаем второе окно
        second = Tk()
        second.title("Выход?")
        second.resizable(width=False, height=False)
        second.geometry("500x500")
        second["bg"] = "black"

        # функция при нет
        def go_back():
            second.destroy()
            main_window()

        # Создаем надпись
        are_sure = ttk.Label(
            text="Вы точно хотите выйти?",
            background="#DAE500",
            font=("Comic Sans", 40),
            foreground="white",
        )
        are_sure.pack()
        # Создаем кнопку да
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "yes.TButton",
            background="#37FF00",
            font=("Comic Sans", 30),
            foreground="white",
        )
        yes = ttk.Button(text="[1] Да", style="yes.TButton", command=second.destroy)
        yes.pack()
        # Создаем кнопку нет
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "no.TButton",
            background="#FF1500",
            font=("Comic Sans", 30),
            foreground="white",
        )
        no = ttk.Button(text="[2] Нет", style="no.TButton", command=go_back)
        no.pack()

        second.mainloop()

    button_exit = Button(
        root, text="[3] Выйти", font=("Comic Sans", 30), command=open_sure
    )
    button_exit.pack()

    root.mainloop()


# запуск главного окна
main_window()
