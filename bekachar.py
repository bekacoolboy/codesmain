import tkinter as tk
from tkinter import messagebox
import random

# ---------------- ФУНКЦИИ ДЛЯ ЧТЕНИЯ ФАЙЛОВ ----------------
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден!")
        return []

# Загрузка данных из файлов
appearances = load_file("appearances.txt")
characters = load_file("characters.txt")
stories = load_file("stories.txt")

# ---------------- ОКНО ----------------
root = tk.Tk()
root.title("Создание персонажа")
root.geometry("620x580")
root.configure(bg="#0f172a")
root.resizable(False, False)

selected = {"appearance": "", "character": "", "story": ""}

# ---------------- СТИЛИ ----------------
CARD_BG = "#ffffff"
BTN_BG = "#e5e7eb"
BTN_HOVER = "#c7d2fe"
TITLE_COLOR = "#e5e7eb"
BTN_RANDOM_BG = "#10b981"
BTN_RANDOM_HOVER = "#059669"

# ---------------- ФУНКЦИИ ----------------
def clear():
    for w in content.winfo_children():
        w.destroy()

def hover(btn, color):
    btn.bind("<Enter>", lambda e: btn.config(bg=color))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG))

def hover_special(btn, bg_color, hover_color):
    btn.config(bg=bg_color, fg="white")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

def card(title_text, items, key, next_step):
    clear()

    card_frame = tk.Frame(content, bg=CARD_BG)
    card_frame.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(
        card_frame, text=title_text,
        font=("Segoe UI", 16, "bold"),
        bg=CARD_BG
    ).pack(pady=15)

    # Кнопка случайного выбора
    random_btn = tk.Button(
        card_frame,
        text="Выбрать случайно 🎲",
        font=("Segoe UI", 11, "bold"),
        bg=BTN_RANDOM_BG,
        bd=0,
        padx=15,
        pady=10,
        command=lambda: choose(random.choice(items), key, next_step)
    )
    random_btn.pack(pady=10)
    hover_special(random_btn, BTN_RANDOM_BG, BTN_RANDOM_HOVER)

    for item in items:
        btn = tk.Button(
            card_frame,
            text=item,
            wraplength=480,
            font=("Segoe UI", 11),
            bg=BTN_BG,
            bd=0,
            padx=12,
            pady=8,
            command=lambda x=item: choose(x, key, next_step)
        )
        btn.pack(fill="x", padx=20, pady=6)
        hover(btn, BTN_HOVER)

def choose(value, key, next_step):
    selected[key] = value
    next_step()

def save_to_file():
    try:
        with open("character.txt", "w", encoding="utf-8") as f:
            f.write("Персонаж:\n")
            f.write(f"Внешность: {selected['appearance']}\n")
            f.write(f"Характер: {selected['character']}\n")
            f.write(f"История: {selected['story']}\n")
        messagebox.showinfo("Сохранено", "Персонаж сохранён в файл character.txt")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

def result():
    clear()

    card_frame = tk.Frame(content, bg=CARD_BG)
    card_frame.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(card_frame, text="Ваш персонаж",
             font=("Segoe UI", 18, "bold"),
             bg=CARD_BG).pack(pady=15)

    for title, key in [("Внешность", "appearance"),
                       ("Характер", "character"),
                       ("История", "story")]:
        tk.Label(card_frame, text=title,
                 font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG).pack(anchor="w", padx=20, pady=(10,0))
        tk.Label(card_frame, text=selected[key],
                 wraplength=520,
                 bg=CARD_BG).pack(anchor="w", padx=20, pady=(0,8))

    buttons_frame = tk.Frame(card_frame, bg=CARD_BG)
    buttons_frame.pack(pady=20)

    restart = tk.Button(
        buttons_frame,
        text="Создать нового персонажа",
        font=("Segoe UI", 12, "bold"),
        bg="#6366f1",
        fg="white",
        bd=0,
        padx=18,
        pady=10,
        command=start
    )
    restart.grid(row=0, column=0, padx=10)
    hover_special(restart, "#6366f1", "#4f46e5")

    save_btn = tk.Button(
        buttons_frame,
        text="Сохранить в файл",
        font=("Segoe UI", 12, "bold"),
        bg="#2563eb",
        fg="white",
        bd=0,
        padx=18,
        pady=10,
        command=save_to_file
    )
    save_btn.grid(row=0, column=1, padx=10)
    hover_special(save_btn, "#2563eb", "#1e40af")

def start():
    selected["appearance"] = ""
    selected["character"] = ""
    selected["story"] = ""
    card("Выберите внешность", appearances,
         "appearance",
         lambda: card("Выберите характер", characters,
                      "character",
                      lambda: card("Выберите историю", stories,
                                   "story",
                                   result)))

# ---------------- КОНТЕЙНЕР ----------------
tk.Label(
    root,
    text="Генератор персонажа",
    font=("Segoe UI", 24, "bold"),
    fg=TITLE_COLOR,
    bg="#0f172a"
).pack(pady=20)

content = tk.Frame(root, bg="#0f172a")
content.pack(fill="both", expand=True)

start()
root.mainloop()
