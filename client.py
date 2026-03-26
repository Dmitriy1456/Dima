import socket

host = '127.0.0.1'
port = 65432


def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Подключено к серверу.")

        while True:
            msg = input("\nВведите команду (или 'exit' для выхода): ")

            if msg.lower() == 'exit':
                break

            s.sendall(msg.encode('utf-8'))

            data = s.recv(1024)
            if not data:
                print("Сервер разорвал соединение.")
                break

            print(f"Ответ сервера: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print("Ошибка: Сервер не доступен.")
    except Exception as e:
        print(f"Сетевая ошибка: {e}")
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        s.close()
        print("Соединение закрыто.")


if __name__ == "__main__":
    start_client()