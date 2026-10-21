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

    def get_chat_names(self):

        self.page.wait_for_selector(
            '[data-testid="cell-frame-container"]',
            timeout=30000,
        )

        chats = self.page.locator('[data-testid="cell-frame-container"]')

        total = chats.count()

        print(f"Conversas encontradas: {total}")

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

            except Exception as e:
                print(f"Erro na conversa {i}: {e}")

        return names

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