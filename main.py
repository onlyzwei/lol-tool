from os import system
from rich.console import Console
from rich.prompt import Prompt
from Dodge import dodge
from Riotidchanger import riotid_menu
from RestartUX import restart
from lcu_core import check_league_client
from disconnect_reconnect_chat import Chat
import io
import sys

class MenuOption:
    def __init__(self, title, action, show_state=False, feature_name=""):
        self.title = title
        self.action = action
        self.show_state = show_state
        self.feature_name = feature_name

class LeagueClientTool:
    def __init__(self):
        self.console = Console()
        self.chat = Chat()
        self._initialize_menu_options()

    def _initialize_menu_options(self):
        self.menu_options = {
            1: MenuOption("Dodge", dodge),
            2: MenuOption("Riot ID Changer", riotid_menu),
            3: MenuOption("Restart Client UX", restart),
            4: MenuOption("Disconnect Chat", self.chat.toggle_chat, True, "chat"),
            99: MenuOption("Exit", self._exit_program)
        }

    def _display_menu(self):
        system("cls")
        for key, option in self.menu_options.items():
            menu_text = f"[bold yellow]{key}.[/] {option.title}"
            if option.show_state:
                state = self._get_feature_state(option.feature_name)
                menu_text += f" ([bold green]{state}[/])"
            self.console.print(menu_text)

        return Prompt.ask("\n[bold cyan]Escolha uma opção[/]", choices=[str(k) for k in self.menu_options.keys()])

    def _get_feature_state(self, feature_name):
        states = {"chat": self.chat.chat_state}
        return "ON" if states.get(feature_name, False) else "OFF"

    def _exit_program(self):
        self.console.print("[bold red]Saindo...[/]")
        raise SystemExit


    def run(self):
        self.console.print("\n[bold cyan]Aguardando o cliente do League...[/]\n")
        check_league_client()

        while True:
            try:
                check_league_client()
                option = self._display_menu()

                if int(option) not in self.menu_options:
                    continue

                self.menu_options[int(option)].action()

            except KeyboardInterrupt:
                self._exit_program()
            except Exception as e:
                self.console.print(f"[bold red]Erro:[/] {str(e)}")
                continue

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') 
    system("chcp 65001 > nul")

    system("mode con: cols=80 lines=25")

    client_tool = LeagueClientTool()
    client_tool.run()