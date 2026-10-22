class Exporter:

    def __init__(self, whatsapp):

        self.whatsapp = whatsapp
        self.dados = []

    def run(self):

        chats = self.whatsapp.get_chat_names()

        print(f"{len(chats)} conversas encontradas.\n")

        for chat in chats:

            print(f"Processando: {chat}")

            if not self.whatsapp.open_chat(chat):
                continue

            mensagens = self.whatsapp.get_messages(chat)

            self.dados.extend(mensagens)

        print(f"\nTotal de registros: {len(self.dados)}")

        return self.dados