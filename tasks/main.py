import sys
import task_5, task_6, task_7
import os

if not os.path.exists("gifs"):
    os.mkdir("gifs")
if __name__ == "__main__":
    print('1 — Поиск каркаса, фундаментальной системы циклов и разрезов в ненагруженном графе\n2 — Поиск каркаса, фундаментальной системы циклов и разрезов в нагруженном графе\n3 — Поиск совершенного паросочетания в двудольном графе\n0 — Выход из программы')
    task_number = input('Выберите задачу, которую хотите решить: ')
    while task_number:
        if task_number == '1':
            task_5.main()
        elif task_number == '2':
            task_6.main()
        elif task_number == '3':
            task_7.main()
        elif task_number == '0':
            sys.exit()
        else:
            print('Введите корректный номер задачи, либо введите 0 для выхода из программы')
        task_number = input('Выберите задачу, которую хотите решить: ')
