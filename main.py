import sys
import pyautogui # !!! pip install opencv-contrib-python
import keyboard
import time

import threading
from threading import Thread

# pyautogui.mouseInfo()
# 1174,440
# 1556,440
# 382


#Эту функцию будем запускать в отдельном потоке. Она непрерывно следит за клавиатурой.
# И передаёт сигнал СТОП, если нажали на определённую клавишу
def EXIT():
    global stop
    global keyStop
    while True:
        if keyboard.is_pressed(keyStop):
            stop = True
            break

        # В случае исключения в основном потоке, выходим и отправляем СТОП, чтобы закрылся этот поток.
        if stop == True:
            break
        pyautogui.sleep(0.05)

#считываем четыре строчки из текстового файла
try:
    with open("settings.txt", "r") as file:
        pause = int(file.readline())
        confidence = float(file.readline())
        clickRight = int(file.readline())
        keyStop = file.readline()
except:
    pyautogui.alert('Ошибка чтения файла settings.txt', 'ВНИМАНИЕ')
    stop = True
    sys.exit()

#Переменная для остановки программы.
#Если она равна True, то программа должна завершить свою работу
stop = False

#Запускаем отдельный поток, в котором запускается функция EXIT()
th = Thread(target=EXIT)
th.start()

coords =pyautogui.locateCenterOnScreen('img.png')
print(coords)

#Бесконечный поиск изображения, пока не получен сигнал СТОП
while stop == False:
    try:
        button = pyautogui.locateCenterOnScreen('img.png', confidence=confidence/100)
    except:
        pyautogui.alert("Не могу открыть img.png", "ВНИМАНИЕ")
        stop = True
        sys.exit()

    if (button):
        pyautogui.click(button.x+clickRight, button.y, clicks=2)

    pyautogui.sleep(pause)

# pyinstaller -F -w -i "bot.ico" main.py
