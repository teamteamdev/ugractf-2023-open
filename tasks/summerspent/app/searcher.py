import shlex
import subprocess
import time


class Searcher:
    def __init__(self, conn, token, cwd):
        self.conn = conn
        self.token = token
        self.cwd = cwd


    async def prompt(self):
        return (await self.conn.readline()).decode(errors="ignore").strip()


    async def iterate_commands(self):
        self.conn.write(("\n\n"
            "Это архив документальных свидетельств о лете 2022 года, \n"
            "собранных с учащихся средних классов в течение сентября \n"
            "того же года. Все свидетельства упорядочены по порядку, \n"
            "им присвоены индивидуальные порядковые номера.\n\n"
            "Доступные команды:\n\n"
            "search: текстовый поиск\n"
            "exit: выход\n").encode())
        send_times = [0] * 30
        while True:
            send_times = send_times[1:] + [time.time()]
            if send_times[-1] - send_times[0] < 0.25:
                break  # connection lost

            res = self.conn.write("\nВведите команду. > ".encode())
            command = await self.prompt()
            if not command:
                continue

            if command == "exit":
                self.conn.write("\nДо свидания.\n".encode())
                break
            elif command == "search":
                self.conn.write("Введите поисковый запрос. > ".encode())
                query = await self.prompt()
                if not query:
                    self.conn.write("Ошибка: задан пустой запрос.\n".encode())
                    continue

                self.conn.write("Введите порядковый номер документа. > ".encode())
                number_str = await self.prompt()
                try:
                    number = int(number_str)
                except ValueError:
                    self.conn.write("Ошибка: введено неверное число.\n".encode())
                    continue
                if number < 500:
                    self.conn.write(("У вас есть доступ только к свидетельствам с номерами от 500,\n"
                                     "а к остальным нет доступа, потому что \n"
                                     "ЗАПРЕЩЕНО по причине СЕКРЕТНО (ЗАСЕКРЕЧЕНО).\n").encode())
                    continue

                self.conn.write("Введите 1, если требуется поиск по соседним документам, иначе 0. > ".encode())
                siblings_str = await self.prompt()
                try:
                    siblings = int(siblings_str)
                except ValueError:
                    continue
                if siblings not in {0, 1}:
                    self.conn.write("Введено неверное значение.\n".encode())
                    continue

                quoted_query = shlex.quote(query)
                if siblings:
                    run_command = ("grep -C1 -H -e " + quoted_query + " $(( " + number_str + " - 2 )).txt $(( " +
                                   number_str + " - 1 )).txt " + number_str + ".txt $(( " + number_str +
                                   " + 1 )).txt $(( " + number_str + " + 2 )).txt")
                else:
                    run_command = "grep -C1 -H -e " + quoted_query + " " + number_str + ".txt"


                try:
                    output = subprocess.check_output(["/bin/bash", "-c", run_command + " ; exit 0"],
                                                                stderr=subprocess.DEVNULL, cwd=self.cwd)
                    if not output.strip():
                        raise ValueError
                    self.conn.write(output + b"\n")
                except (subprocess.CalledProcessError, ValueError):
                    self.conn.write("Ничего не найдено.\n".encode())
            else:
                self.conn.write(f"Неизвестный ввод. (\"{command}\")\n".encode())
