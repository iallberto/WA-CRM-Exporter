from excel import Excel
from services.date_service import DateService

class Exporter:

    def __init__(self, whatsapp):

        self.whatsapp = whatsapp
        self.dados = []

    def run(self):

        chats = self.whatsapp.get_all_chat_names()

        print(f"{len(chats)} conversas encontradas.\n")

        for chat in self.whatsapp.iter_chat_elements():

            print(f"Processando: {chat['contato']}")

            chat["elemento"].click()

            self.whatsapp.page.wait_for_timeout(500)

            self.dados.append({
                "contato": chat["contato"],
                "data": "",
                "mensagem": "",
            })       

        date_service = DateService()

        self.dados = date_service.run(
            self.whatsapp,
            self.dados,
        )

        print(f"\nTotal de registros: {len(self.dados)}")

        excel = Excel()

        excel.export(
            self.dados,
            "output/conversas.xlsx",
        )

        print("\nPlanilha exportada com sucesso.")

        return self.dados