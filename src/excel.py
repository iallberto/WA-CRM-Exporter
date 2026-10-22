from openpyxl import Workbook


class Excel:

    def export(self, registros, arquivo):

        wb = Workbook()

        ws = wb.active

        ws.title = "Conversas"

        ws.append([
            "Contato",
            "Data",
            "Mensagem",
        ])

        for registro in registros:

            ws.append([
                registro["contato"],
                registro.get("data", ""),
                registro["mensagem"],
            ])

        wb.save(arquivo)