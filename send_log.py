import argparse

from logger import NetworkLogger


def main():
    parser = argparse.ArgumentParser(
        description="Enviar un mensaje al servidor de logs."
    )
    parser.add_argument("message", help="Mensaje a enviar al servidor de logs")
    parser.add_argument(
        "--host", default="localhost", help="Host del servidor (por defecto: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=9999, help="Puerto del servidor (por defecto: 9999)"
    )
    args = parser.parse_args()

    logger = NetworkLogger(host=args.host, port=args.port)
    logger.log(args.message)


if __name__ == "__main__":
    main()
