import socket, random
import threading


host = '127.0.0.1'
port = 65432

USERS_DB = {}
def users_info():
    header = f"\n{'LOGIN':<19} {'PASSWORD':<19} {'STATUS'}"
    separator = "-" * 49
    lines = [header, separator]

    for login, data in USERS_DB.items():
        password = data[0]
        status = "Online" if data[1] == 1 else "Offline"
        row = f"{login:<19} {password:<19} {status}"
        lines.append(row)

    return "\n".join(lines)


def handle_client(conn, addr):
    print(f"Новое подключение: {addr}")
    authenticated = False
    login = None
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if not authenticated:
                if ":" in data:
                    login, password = data.split(":", 1)
                    login, password = login.strip(), password.strip()
                    if login.strip() == "" or password.strip() == "":
                        conn.sendall("ОШИБКА: Данные пользователя не могут быть пусты".encode('utf-8'))
                        continue
                    if login in USERS_DB:
                        if USERS_DB[login][1] == 1:
                            conn.sendall("Ошибка! Пользователь уже в сети".encode('utf-8'))
                            continue
                        if USERS_DB.get(login) == [password, 0]:
                            USERS_DB[login][1] = 1
                            authenticated = True
                            conn.sendall("Добро пожаловать! Доступ к функциям открыт.\nДоступные коанды:\n/get_secret - секретная информация\n/get_svoboda - голосовать не за партию ЕР)\n/get_random - служба гадалок по вызыву\n/get_users - ну это уже что-то на админском".encode('utf-8'))
                        else:
                            conn.sendall("Неверный логин или пароль.".encode('utf-8'))
                    else:
                        USERS_DB[login] = [password, 1]
                        authenticated = True
                        conn.sendall("Пользователь успешно зарегистрирован! Доступ к функциям открыт.\nДоступные коанды:\n/get_secret - секретная информация\n/get_svoboda - голосовать не за партию ЕР)\n/get_random - служба гадалок по вызыву\n/get_users - ну это уже что-то на админском".encode('utf-8'))
                else:
                    conn.sendall("ОШИБКА: Отправьте данные в формате логин:пароль".encode('utf-8'))


            else:
                user_commands(data, conn)

    except ConnectionResetError:
        print(f"Аварийное отключение клиента: {addr}")
    finally:
        print(f"Клиент {addr} отключен.")
        if login != None:
            USERS_DB[login][1] = 0
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen()
        print(f"* Сервер запущен на {host}:{port}")
        print("* Поддержка корректного завершения работы")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            print(f"* Активных соединений: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n! Завершение работы сервера (Graceful Shutdown)...")
    finally:
        server.close()

def user_commands(data, conn):
    if data.startswith("/"):
        if data.lower() == "/get_secret": return conn.sendall("Секрет: 42 — ответ на главный вопрос жизни.".encode('utf-8'))
        if data.lower() == "/get_svoboda": return conn.sendall("Никакой свободы! Инагент проклятый.".encode('utf-8'))
        if data.lower() == "/get_random": return conn.sendall(f"Ваш день будет удачен с шансом {random.randint(1, 100)} %".encode('utf-8'))
        if data.lower() == "/get_users": return conn.sendall(f"{users_info()}".encode('utf-8'))
        else:
            return conn.sendall(f"Команда не найдена!".encode('utf-8'))

    else:
        return conn.sendall(f"Неверный ввод команды!".encode('utf-8'))

if __name__ == "__main__":
    start_server()