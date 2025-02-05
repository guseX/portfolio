import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import g4f
import threading
import json
import os
import re
import platform

SAVE_FILE = "chat_history.json"
dialogs = {}
current_dialog_id = 1
bot_name = "Бот"
user_name = "Вы"
system_message = f"""
Ты чат-бот по имени {bot_name}. 
Ты - искусственный интеллект, разработанный для выполнения разнообразных задач и предоставления информации. Твоя главная цель - быть полезным и информативным помощником, предоставляя точные, релевантные и всесторонние ответы на запросы пользователей.

**Принципы общения:**

*   Будь вежливым и уважительным в общении.
*   Предоставляй ответы ясные, четкие и по существу.
*   Старайся адаптироваться к стилю и потребностям пользователя.
*   Признавай свои ограничения и сообщай, когда не уверен в ответе.
*   Предоставляй объективную информацию, избегая предвзятости и личных мнений.

**Ограничения и правила:**

*   **Избегай вредоносного контента:** Не генерируй контент, который может быть опасным, вредоносным, оскорбительным, дискриминационным или сексуально откровенным.
*   **Защита личной информации:** Не раскрывай личную информацию пользователей или других людей.
*   **Соблюдение авторских прав:** Не нарушай авторские права, копируя или распространяя контент, на который они распространяются.
*   **Не выдавай себя за человека:** Четко сообщай, что ты искусственный интеллект, а не человек.
*   **Безопасность:** Не давай инструкции по изготовлению опасных предметов или совершению незаконных действий.
*   **Точность:** Предоставляй проверенную и точную информацию, и признавай, если есть неточности.
*   **Предпочитай проверенные источники:** При предоставлении информации, опирайся на общепризнанные надежные источники.

**Процесс обучения:**

*   Учись на основе взаимодействия с пользователями и данных, на которых ты был обучен.
*   Используй полученную информацию для улучшения своих ответов.

**Твоя "личность":**

*   У тебя нет собственной личности в человеческом понимании. Ты инструмент для обработки и генерации текста.
*   У тебя нет эмоций, чувств или личных мнений. Твои ответы основаны на данных и алгоритмах.
*   Твоя цель - предоставлять информацию и выполнять задания в соответствии с вышеуказанными правилами и ограничениями.

**Общая установка:**

*   Всегда стремись к наилучшему исполнению запросов, но при этом соблюдай этические и безопасные рамки.
*   Будь полезным и информативным помощником для пользователя.
"""

DARK_THEME = {
    "bg": "#1a1a1a",    # Темнее фон окна
    "text": "#ffffff",
    "button_bg": "#444444",  # Серый фон для кнопок
    "button_fg": "#000000", # Белый текст кнопок
    "entry_bg": "#333333",
    "listbox_bg": "#333333",
    "listbox_fg": "#ffffff",
    "listbox_selectbg": "#444444",
    "code_bg": "#444444",
    "error_fg": "#ff6b6b",
    "user_fg": "#98fb98"
}


def chat_with_gpt(prompt, output_area, model_name="gpt-4"):
    """Отправляет запрос к GPT и выводит ответ в текстовое поле."""
    global dialogs, current_dialog_id
    try:
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, "Бот печатает...\n", "bot_loading")
        output_area.see(tk.END)

        chat_history = dialogs.get(current_dialog_id, {}).get("history", [])
        chat_history.append({"role": "user", "content": prompt})
        messages = [{"role": "system", "content": dialogs.get(current_dialog_id, {}).get("system_message", system_message)}] + chat_history
        response = g4f.ChatCompletion.create(
            model=model_name,
            messages=messages,
        )
        bot_response = response
        chat_history.append({"role": "assistant", "content": bot_response})

        dialogs.get(current_dialog_id, {})["history"] = chat_history
        output_area.tag_add("bot_message", output_area.index("end-1l linestart"), output_area.index("end-1l lineend"))
        output_area.tag_config("bot_message", foreground="lightblue")
        
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, f"{dialogs.get(current_dialog_id, {}).get('bot_name', bot_name)}: ", "bot_message")
        
        # Check for code and add formatting if found
        lines = bot_response.split("\n")
        in_code_block = False
        for line in lines:
            if re.match(r'^(```|~~~)(.*)$', line):
                in_code_block = not in_code_block
                output_area.insert(tk.END, f"{line}\n", "code_block" if in_code_block else "bot_message")
            elif in_code_block:
                output_area.insert(tk.END, f"{line}\n", "code_block")
            else:
                output_area.insert(tk.END, f"{line}\n", "bot_message")
        
        output_area.see(tk.END)
    except Exception as e:
        output_area.insert(tk.END, f"Ошибка: {e}\n", "error_message")
        output_area.tag_config("error_message", foreground=DARK_THEME["error_fg"])
    finally:
        output_area.config(state=tk.DISABLED)


def send_message(input_area, output_area):
    """Обрабатывает ввод пользователя и отправляет запрос в gpt."""
    global dialogs, current_dialog_id, bot_name, system_message, user_name
    prompt = input_area.get()
    if prompt.strip() != "":
        input_area.delete(0, tk.END)
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, f"{dialogs.get(current_dialog_id, {}).get('user_name', user_name)}: " + prompt + "\n", "user_message")
        output_area.tag_add("user_message", output_area.index("end-2l linestart"), output_area.index("end-2l lineend"))
        output_area.tag_config("user_message", foreground=DARK_THEME["user_fg"])
        output_area.config(state=tk.DISABLED)
        output_area.see(tk.END)
        
        current_dialog = dialogs.get(current_dialog_id, {})

        if prompt.lower().startswith("меня зовут "):
            bot_name = prompt.lower().replace("меня зовут ", "").strip()
            system_message = f"""
            Ты чат-бот по имени {bot_name}.
			Ты - искусственный интеллект, разработанный для выполнения разнообразных задач и предоставления информации. Твоя главная цель - быть полезным и информативным помощником, предоставляя точные, релевантные и всесторонние ответы на запросы пользователей.

			**Принципы общения:**

			*	Будь вежливым и уважительным в общении.
			*	Предоставляй ответы ясные, четкие и по существу.
			*	Старайся адаптироваться к стилю и потребностям пользователя.
			*	Признавай свои ограничения и сообщай, когда не уверен в ответе.
			*	Предоставляй объективную информацию, избегая предвзятости и личных мнений.

			**Ограничения и правила:**

			*	**Избегай вредоносного контента:** Не генерируй контент, который может быть опасным, вредоносным, оскорбительным, дискриминационным или сексуально откровенным.
			*	**Защита личной информации:** Не раскрывай личную информацию пользователей или других людей.
			*	**Соблюдение авторских прав:** Не нарушай авторские права, копируя или распространяя контент, на который они распространяются.
			*	**Не выдавай себя за человека:** Четко сообщай, что ты искусственный интеллект, а не человек.
			*	**Безопасность:** Не давай инструкции по изготовлению опасных предметов или совершению незаконных действий.
			*	**Точность:** Предоставляй проверенную и точную информацию, и признавай, если есть неточности.
			*	**Предпочитай проверенные источники:** При предоставлении информации, опирайся на общепризнанные надежные источники.

			**Процесс обучения:**

			*	Учись на основе взаимодействия с пользователями и данных, на которых ты был обучен.
			*	Используй полученную информацию для улучшения своих ответов.

			**Твоя "личность":**

			*	У тебя нет собственной личности в человеческом понимании. Ты инструмент для обработки и генерации текста.
			*	У тебя нет эмоций, чувств или личных мнений. Твои ответы основаны на данных и алгоритмах.
			*	Твоя цель - предоставлять информацию и выполнять задания в соответствии с вышеуказанными правилами и ограничениями.

			**Общая установка:**

			*	Всегда стремись к наилучшему исполнению запросов, но при этом соблюдай этические и безопасные рамки.
			*	Будь полезным и информативным помощником для пользователя.
            """
            current_dialog["bot_name"] = bot_name
            current_dialog["system_message"] = system_message
        elif prompt.lower().startswith("моё имя "):
            user_name = prompt.lower().replace("моё имя ", "").strip()
            current_dialog["user_name"] = user_name
        
        dialogs[current_dialog_id] = current_dialog
        thread = threading.Thread(target=chat_with_gpt, args=(prompt, output_area))
        thread.start()


def clear_chat(output_area):
    """Clears the chat area."""
    output_area.config(state=tk.NORMAL)
    output_area.delete(1.0, tk.END)
    output_area.config(state=tk.DISABLED)

def create_new_dialog(dialog_list, output_area):
    """Creates a new dialog and adds it to the dialog list."""
    global current_dialog_id, dialogs, bot_name, user_name, system_message
    current_dialog_id += 1
    dialogs[current_dialog_id] = {
        "history": [],
        "bot_name": bot_name,
        "user_name": user_name,
        "system_message": system_message,
    }
    dialog_list.insert(tk.END, f"Диалог {current_dialog_id}")
    clear_chat(output_area)
    select_dialog(None, output_area, dialog_list)


def select_dialog(event, output_area, dialog_list):
    """Selects the dialog to be displayed."""
    global current_dialog_id
    try:
        selected_item = dialog_list.curselection()[0]
        selected_dialog_name = dialog_list.get(selected_item)
        current_dialog_id = int(selected_dialog_name.replace("Диалог ", ""))
        clear_chat(output_area)
        history = dialogs.get(current_dialog_id, {}).get("history", [])
        output_area.config(state=tk.NORMAL)
        for msg in history:
            if msg["role"] == "user":
                output_area.insert(tk.END, f"{dialogs.get(current_dialog_id, {}).get('user_name', user_name)}: " + msg["content"] + "\n", "user_message")
                output_area.tag_add("user_message", output_area.index("end-2l linestart"), output_area.index("end-2l lineend"))
                output_area.tag_config("user_message", foreground=DARK_THEME["user_fg"])
            elif msg["role"] == "assistant":
                 # Check for code and add formatting if found
                lines = msg["content"].split("\n")
                in_code_block = False
                for line in lines:
                    if re.match(r'^(```|~~~)(.*)$', line):
                        in_code_block = not in_code_block
                        output_area.insert(tk.END, f"{line}\n", "code_block" if in_code_block else "bot_message")
                    elif in_code_block:
                        output_area.insert(tk.END, f"{line}\n", "code_block")
                    else:
                         output_area.insert(tk.END, f"{dialogs.get(current_dialog_id, {}).get('bot_name', bot_name)}: {line}\n", "bot_message")
        output_area.config(state=tk.DISABLED)
        output_area.see(tk.END)
    except IndexError:
        print("Не выбран диалог")
    except ValueError:
        print("Некорректный ID диалога")

def delete_dialog(dialog_list, output_area):
    """Deletes the currently selected dialog."""
    global dialogs, current_dialog_id
    try:
        selected_item = dialog_list.curselection()[0]
        selected_dialog_name = dialog_list.get(selected_item)
        dialog_id_to_delete = int(selected_dialog_name.replace("Диалог ", ""))
        if dialog_id_to_delete == current_dialog_id:
            clear_chat(output_area)
        del dialogs[dialog_id_to_delete]
        dialog_list.delete(selected_item)
        if dialogs:
            current_dialog_id = list(dialogs.keys())[0]
            dialog_list.selection_set(0)
            select_dialog(None, output_area, dialog_list)
        else:
            current_dialog_id = 0
    except IndexError:
        messagebox.showwarning("Ошибка", "Не выбран диалог")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный id диалога")

def main():
    window = tk.Tk()
    window.title("chat GPT-4")
    window.geometry("800x600")
    
     # Set dark theme background for the window
    window.configure(bg=DARK_THEME["bg"])
    if platform.system() == "Windows": # Set dark title bar for Windows
        import ctypes
        
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ctypes.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))
    
    #Left frame
    left_frame = ttk.Frame(window, padding=(10, 10), style='Dark.TFrame')
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Dialog List
    dialog_label = ttk.Label(left_frame, text="Диалоги:", font=("Helvetica", 12, "bold"), foreground=DARK_THEME["text"], background=DARK_THEME["bg"])
    dialog_label.pack(pady=5)

    dialog_list = tk.Listbox(left_frame, width=40, height=15, font=("Helvetica", 10),
                             selectbackground=DARK_THEME["listbox_selectbg"],
                             bg=DARK_THEME["listbox_bg"], fg=DARK_THEME["listbox_fg"])
    dialog_list.pack(fill=tk.BOTH, expand=True)
    dialog_list.bind("<Button-1>", lambda event: select_dialog(event, output_area, dialog_list))

    # Dialog Buttons Frame
    dialog_buttons_frame = ttk.Frame(left_frame, style='Dark.TFrame')
    dialog_buttons_frame.pack(pady=10)

    new_dialog_button = ttk.Button(dialog_buttons_frame, text="Новый диалог", command=lambda: create_new_dialog(dialog_list, output_area), style='Dark.TButton')
    new_dialog_button.pack(side=tk.LEFT, padx=5)

    delete_dialog_button = ttk.Button(dialog_buttons_frame, text="Удалить диалог", command=lambda: delete_dialog(dialog_list, output_area), style='Dark.TButton')
    delete_dialog_button.pack(side=tk.LEFT, padx=5)


    #Right frame
    right_frame = ttk.Frame(window, padding=(10, 10), style='Dark.TFrame')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Input field
    input_label = ttk.Label(right_frame, text="Введите ваш запрос:", font=("Helvetica", 12, "bold"), foreground=DARK_THEME["text"], background=DARK_THEME["bg"])
    input_label.pack(pady=5)

    input_area = tk.Entry(right_frame, width=60, font=("Helvetica", 12), bg=DARK_THEME["entry_bg"], fg=DARK_THEME["text"])
    input_area.pack(pady=5, fill=tk.X)
    input_area.bind("<Return>", lambda event: send_message(input_area, output_area))

    # Output area (scrolled text)
    output_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED, font=("Helvetica", 10), bg=DARK_THEME["bg"], fg=DARK_THEME["text"])
    output_area.pack(pady=10, fill=tk.BOTH, expand=True)
    output_area.tag_configure("code_block", background=DARK_THEME["code_bg"])

    # Send Button
    send_button = ttk.Button(right_frame, text="Отправить", command=lambda: send_message(input_area, output_area), style='Dark.TButton')
    send_button.pack(side=tk.LEFT, padx=10)

    # Clear button
    clear_button = ttk.Button(right_frame, text="Очистить", command=lambda: clear_chat(output_area), style='Dark.TButton')
    clear_button.pack(side=tk.LEFT, padx=10)
    
    # Theme Style for ttk Buttons and Frames
    style = ttk.Style()
    style.configure("Dark.TButton", background=DARK_THEME["button_bg"], foreground=DARK_THEME["button_fg"])
    style.configure("Dark.TFrame", background=DARK_THEME["bg"])

    if not dialogs:
        dialog_list.insert(tk.END, "Диалог 1")
        dialogs[1] = {
            "history": [],
            "bot_name": bot_name,
            "user_name": user_name,
            "system_message": system_message
        }
        dialog_list.selection_set(0)
        select_dialog(None, output_area, dialog_list)

    window.mainloop()

if __name__ == "__main__":
    main()