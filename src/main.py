from whatsapp import WhatsApp
from exporter import Exporter


def main():

    wa = WhatsApp()

    wa.start()

    wa.wait_until_ready()

    exporter = Exporter(wa)

    dados = exporter.run()

    input("\nENTER para fechar...")

    wa.stop()


if __name__ == "__main__":
    main()