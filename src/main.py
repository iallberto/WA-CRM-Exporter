from whatsapp import WhatsApp


def main():

    wa = WhatsApp()

    wa.start()

    wa.wait_until_ready()

    chats = wa.get_chat_names()

    print("\nConversas encontradas:\n")

    for i, chat in enumerate(chats):
        print(f"{i + 1:02d} - {chat}")

    dados = []

    for chat in chats:

        print(f"\nProcessando: {chat}")

        if not wa.open_chat(chat):
            continue

        mensagens = wa.get_messages(chat)

        dados.extend(mensagens)

        print(f"\nTotal de registros: {len(dados)}") 

    print("\n" + "=" * 80)

    for i, msg in enumerate(mensagens, 1):

        print(f"\n[{i}]")
        print(msg)

    input("\nENTER para fechar...")

    wa.stop()


if __name__ == "__main__":
    main()