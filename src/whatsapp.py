from email.mime import message
from pathlib import Path
from pyexpat.errors import messages
from pyexpat.errors import messages
from tkinter.font import names

from playwright.sync_api import sync_playwright


class WhatsApp:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):

        session_dir = Path("session")
        session_dir.mkdir(exist_ok=True)

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,
        )

        self.page = self.browser.new_page()

        self.page.goto(
            "https://web.whatsapp.com",
            wait_until="domcontentloaded",
        )

    def wait_until_ready(self):

        print("Aguardando WhatsApp...")

        self.page.wait_for_selector(
            '[data-testid="chat-list"]',
            timeout=120000,
        )

        print("WhatsApp carregado!")

    def get_chat_elements(self):

        self.page.wait_for_selector(
            '[data-testid="cell-frame-container"]',
            timeout=30000,
        )

        return self.page.locator(
            '[data-testid="cell-frame-container"]'
        )    

    def scroll_chat_list(self):

        chats = self.get_chat_elements()

        ultimo = chats.nth(chats.count() - 1)

        ultimo.scroll_into_view_if_needed()

        self.page.wait_for_timeout(500)    

    def get_chat_names(self):

        chats = self.get_chat_elements()

        total = chats.count()

        names = []

        for i in range(total):

            try:

                chat = chats.nth(i)

                title = chat.locator("span[title]").first

                if title.count() == 0:
                    continue

                name = title.get_attribute("title")

                if name and name not in names:
                    names.append(name)

            except Exception:
                continue

        return names

    def iter_chat_elements(self):

        chats = self.get_chat_elements()

        total = chats.count()

        for i in range(total):

            try:

                chat = chats.nth(i)

                title = chat.locator("span[title]").first

                if title.count() == 0:
                    continue

                nome = title.get_attribute("title")

                if not nome:
                    continue

                yield {
                    "contato": nome,
                    "elemento": chat,
                }

            except Exception:
                continue

    def get_all_chat_names(self):

        conversas = set()

        sem_novidades = 0

        while sem_novidades < 3:

            nomes = self.get_chat_names()

            quantidade_anterior = len(conversas)

            conversas.update(nomes)

            if len(conversas) == quantidade_anterior:
                sem_novidades += 1
            else:
                sem_novidades = 0

            self.scroll_chat_list()

        return sorted(conversas)

    def open_chat(self, chat_name: str) -> bool:

        print(f"Abrindo conversa: {chat_name}")

        chats = self.page.locator('[data-testid="cell-frame-container"]')

        total = chats.count()

        for i in range(total):

            chat = chats.nth(i)

            title = chat.locator("span[title]").first

            if title.count() == 0:
                continue

            name = title.get_attribute("title")

            if name == chat_name:
                chat.click()
                self.page.wait_for_timeout(1000)
                print("Conversa aberta.")
                return True

        print("Conversa não encontrada.")
        return False  

    def get_messages(self, contato: str):

        self.page.wait_for_timeout(1000)

        messages = self.page.locator(
        '[data-testid="msg-container"]'
        )

        total = messages.count()

        print(f"\nMensagens encontradas: {total}\n")

        resultado = []

        for i in range(total):

            try:

                message = messages.nth(i)

                texto = message.inner_text().strip()

                if texto:

                    resultado.append({
                        "contato": contato,
                        "mensagem": texto,
                    })

            except Exception:
                pass

        return resultado

    def stop(self):

        self.browser.close()
        self.playwright.stop()