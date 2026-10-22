from whatsapp import WhatsApp
from exporter import Exporter


def main():

    wa = WhatsApp()

    wa.start()

    wa.wait_until_ready()

    exporter = Exporter(wa)

    dados = exporter.run()

    for chat in wa.iter_chat_elements():

        print(chat["contato"])

    input("\nENTER para fechar...")

    wa.stop()


if __name__ == "__main__":
    main()