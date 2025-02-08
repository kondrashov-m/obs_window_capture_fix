import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con

selected_hwnd = None

def enum_window_callback(hwnd, windows):
    # Фильтруем: окно должно быть видимым и иметь ненулевой заголовок
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append((hwnd, title))
    return True

def get_active_windows():
    windows = []
    win32gui.EnumWindows(enum_window_callback, windows)
    return windows

def move_window_offscreen(hwnd):
    # Получаем координаты и размеры окна
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    # Перемещаем окно за пределы экрана (например, в отрицательные координаты)
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOP,
        -width, -height,
        width, height,
        win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
    )

def on_select_window(event):
    global selected_hwnd
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        hwnd, title = windows_list[index]
        if messagebox.askyesno("Скрыть окно", f"Переместить окно '{title}' за пределы экрана?\n(Окно будет постоянно восстанавливаться, если его свернуть)"):
            move_window_offscreen(hwnd)
            selected_hwnd = hwnd  # запоминаем выбранное окно
            messagebox.showinfo("Успех", f"Окно '{title}' перемещено за пределы экрана.\nOBS Studio сможет его захватывать.")

def refresh_window_list():
    global windows_list
    windows_list = get_active_windows()
    listbox.delete(0, tk.END)
    for hwnd, title in windows_list:
        listbox.insert(tk.END, f"{hwnd} - {title}")

def check_window_state():
    """
    Периодически проверяем, не свернуто ли выбранное окно или оно не скрыто (например, из-за "Свернуть все").
    Если окно не отображается, пытаемся его восстановить и переместить за пределы экрана.
    """
    global selected_hwnd
    if selected_hwnd:
        # Если окно свернуто или не видно, то пытаемся его восстановить.
        if win32gui.IsIconic(selected_hwnd) or not win32gui.IsWindowVisible(selected_hwnd):
            # Восстанавливаем окно
            win32gui.ShowWindow(selected_hwnd, win32con.SW_RESTORE)
            # Для «разбудить» окно устанавливаем его на верх, затем снимаем флаг TopMost
            win32gui.SetWindowPos(
                selected_hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
            win32gui.SetWindowPos(
                selected_hwnd,
                win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
            # Перемещаем окно за пределы экрана
            move_window_offscreen(selected_hwnd)
    root.after(1000, check_window_state)  # проверяем каждую секунду

# Создаём главное окно приложения
root = tk.Tk()
root.title("Выбор окна для OBS захвата")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Список для отображения окон
listbox = tk.Listbox(frame, width=80, height=20)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Вертикальный скроллбар
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# При двойном щелчке по элементу списка выбираем окно
listbox.bind("<Double-Button-1>", on_select_window)

# Кнопка для обновления списка окон
refresh_button = ttk.Button(root, text="Обновить список окон", command=refresh_window_list)
refresh_button.pack(pady=5)

# Инициализируем список окон
windows_list = get_active_windows()
for hwnd, title in windows_list:
    listbox.insert(tk.END, f"{hwnd} - {title}")

# Запускаем периодическую проверку состояния выбранного окна
root.after(1000, check_window_state)

root.mainloop()
