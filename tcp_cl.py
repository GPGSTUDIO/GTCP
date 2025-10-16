import socket
import sys
import os

def tcp_client():
    # Настройки подключения
    together = (sys.argv[1].split(':')[0],int(sys.argv[1].split(':')[1]))
    host = together[0]
    port = together[1]
    try:
        # Создаем TCP сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Подключаемся к серверу
            sock.connect((host,port))
            print(f"Подключено к {host}:{port}")
            
            # Формируем сообщение для отправки
            message = 'What inside: '+sys.argv[2]
            print(f"Отправляю запрос...")
            
            # Отправляем сообщение (кодируем в bytes)
            sock.sendall(message.encode('utf-8'))
            
            # Получаем ответ от сервера
            print("Ожидание данных от сервера...")
            data = b""
            sock.settimeout(5.0)
            # Получаем данные частями
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
            
            if data.startswith(b"<OKAY> No problem (text): "):
                data = data[len("<OKAY> No problem (text): "):]
                print(f"\nПолучено сырых данных: {len(data)} байт")
                if len(sys.argv)==4:
                    with open(sys.argv[3],"wb") as f:
                        f.write(data)
                else:
                    print(f"Сырые данные: {data}")
                    print(f"Декодированные данные: {data.decode('utf-8', errors='replace')}")
                #os.system(sys.argv[3])
            elif data.startswith(b"<OKAY> No problem (binary): "):
                data = data[len("<OKAY> No problem (binary): "):]
                print(f"\nПолучено сырых данных: {len(data)} байт")
                if len(sys.argv)==4:
                    with open(sys.argv[3],"wb") as f:
                        f.write(data)
                else:
                    print(f"Сырые данные: {data}")
                #os.system(sys.argv[3])
            elif data.startswith(b"<404>"):
                print("Ошибка 404 без ответа")
                if len(sys.argv)==4:
                    with open(sys.argv[3],"wb") as f:
                        f.write(b"404")
                #os.system(sys.argv[3])
            elif data.startswith(b"<404W>"):
                data = data[len("<404W> This is webpage: "):]
                print("Ошибка 404!")
                print(f"\nПолучено сырых данных: {len(data)} байт")
                if len(sys.argv)==4:
                    with open(sys.argv[3],"wb") as f:
                        f.write(data)
                else:
                    print(f"Сырые данные: {data}")
                    print(f"Декодированные данные: {data.decode('utf-8', errors='replace')}")
                #os.system(sys.argv[3])
                #print("Сырые данные (bytes):", data)
                #print("Декодированные данные:", data.decode('utf-8', errors='replace'))
            
    except ConnectionRefusedError:
        print(f"Не удалось подключиться к {host}:{port}. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    tcp_client()