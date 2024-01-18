import socket
import threading
import logging
import os
import requests

logging.basicConfig(filename='honeypot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

shutdown_event = threading.Event()

def get_country_by_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("country")
    except Exception as e:
        logging.error("[!] Errore durante il recupero del paese per l'IP {}: {}".format(ip, str(e)))
        return None

def handle_client(client_socket, client_address):
    try:
        logging.info("[*] Connessione accettata da: {}:{}".format(client_address[0], client_address[1]))

        country = get_country_by_ip(client_address[0])
        if country:
            logging.info("[*] Paese di provenienza da {}: {}".format(client_address[0], country))

        request = client_socket.recv(1024)
        logging.info("[*] Ricevuto da {}: {}".format(client_address[0], request.decode('utf-8')))

        request_parts = request.decode('utf-8').split(' ')
        if len(request_parts) >= 2:
            path = request_parts[1]
            logging.info("[*] Percorso richiesto da {}: {}".format(client_address[0], path))

            if path == '/IMMAGINE-A-CASO.jpg':
                with open('IMMAGINE-A-CASO.jpg', 'rb') as image_file:
                    image_content = image_file.read()
                client_socket.sendall(b"HTTP/1.1 200 OK\nContent-Type: image/jpeg\n\n" + image_content)
                return

        else:
            logging.warning("[!] Richiesta HTTP non valida da {}".format(client_address[0]))

        response = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-size: 20px;
            background-image: url('/buc.jpg');
            background-size: cover;
            background-position: center;
            color: #ffffff;
            text-align: center;
            padding: 50px;
        }
    </style>
</head>
<body>
    <p>Aggiungi qui il testo da mostrare nel corpo dell'HTML</p>
</body>
</html>
"""
        client_socket.send(response.encode('utf-8'))

    except Exception as e:
        logging.error("[!] Errore durante la gestione del client {}: {}".format(client_address[0], str(e)))

    finally:
        client_socket.close()

def honeypot():
    global shutdown_event

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('IL-TUO-INDIRIZZO-IP', 8080))
    server.listen(5)

    logging.info("[*] Honeypot in ascolto su IL-TUO-INDIRIZZO-IP:8080")

    while not shutdown_event.is_set():
        try:
            client, addr = server.accept()
            logging.info("[*] Connessione accettata da: {}:{}".format(addr[0], addr[1]))

            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()

        except KeyboardInterrupt:
            logging.info("[*] Ricevuta interruzione da tastiera. Chiusura in corso...")
            shutdown_event.set()

    server.close()

if __name__ == "__main__":
    honeypot()