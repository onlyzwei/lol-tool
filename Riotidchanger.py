from lcu_core import Lcu_core
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from os import system

# Constantes
MAX_NAME_LENGTH = 16
MIN_NAME_LENGTH = 3
MAX_TAG_LENGTH = 5
MIN_TAG_LENGTH = 3

# Inicializa o lcu_core e o Console do Rich
lcu_core = Lcu_core()
console = Console()

# Caracteres especiais para gerar nicks e tags aleatórias
caracteres = [
    '一', '了', 'ζ', 'Ж', 'Щ', 'Ю', 'Э', '〆', '个', 'Λ', '十', 'Ξ', 'へωへ', '丶', 'Ｓ', 'ﬁ', '티', '廴', 'ﬂ', 'Ｊ', '尺'
]

def get_eligibility():
    """ Verifica se o usuário pode trocar o Riot ID. """
    eligibility = lcu_core.lcu_request("GET", "/lol-summoner/v1/riot-alias-free-eligibility")

    if eligibility.text == "false":
        console.print("[bold red]Você não pode trocar o nome agora.[/]")
        console.print("[bold cyan]Pressione Enter para continuar...[/]", end=" ")
        input()
        return False
    return True

def gerar_caracteres(tamanho):
    """ Gera um nome aleatório com caracteres especiais. """
    nick = ""
    while len(nick) != tamanho:
        escolha = random.choice(caracteres)
        espaco_restante = tamanho - len(nick)
        if len(escolha) <= espaco_restante:
            nick += escolha 
    return nick

def change_riotid(name, tag):
    """ Altera o Riot ID do usuário. """
    body = {
        "gameName": name,
        "tagLine": tag
    }
    eligibility = get_eligibility()
    if not eligibility:
        return
     
    response = lcu_core.lcu_request("POST", "/lol-summoner/v1/save-alias", body)

    if response.status_code == 200:
        data = response.json()
        error_code = data.get("errorMessage")

        if error_code == "alias_not_allowed":
            console.print("[bold red]O nome é inapropriado.[/]")
        elif error_code == "alias_not_available":
            console.print("[bold red]O nome já está em uso.[/]")
        elif error_code == "invalid_alias":
            console.print("[bold red]Inválido, escolha ou gere outro nick.)[/]")
        else:
            console.print("[bold green]Riot ID alterado com sucesso![/]")
    else:
        console.print(f"[bold red]Erro na requisição: {response.status_code}[/]")
    
    console.print("[bold cyan]Pressione Enter para continuar...[/]", end=" ")
    input()

def change_riotid_menu():
    """ Menu para trocar o Riot ID. """
    eligibility = get_eligibility()
    if not eligibility:
        return
    
    while True:
        system("cls")
        console.print(Panel.fit("Trocar Riot ID", style="bold cyan"))

        name = Prompt.ask("[bold cyan]Digite o novo nome (ou pressione Enter para voltar)[/]")
        if not name:
            return

        if len(name) > MAX_NAME_LENGTH or len(name) < MIN_NAME_LENGTH:
            console.print(f"[bold yellow]Aviso:[/] O nome deve estar entre {MIN_NAME_LENGTH} e {MAX_NAME_LENGTH} caracteres.", style="bold yellow")
            continue
        break

    while True:
        system("cls")
        tag = Prompt.ask("[bold cyan]Digite a nova tag (ou pressione Enter para voltar)[/]")
        if not tag:
            return
            
        if len(tag) > MAX_TAG_LENGTH or len(tag) < MIN_TAG_LENGTH:
            console.print(f"[bold yellow]Aviso:[/] A tag deve estar entre {MIN_TAG_LENGTH} e {MAX_TAG_LENGTH} caracteres.", style="bold yellow")
            continue
        break

    change_riotid(name, tag)

def show_suggestions():
    """ Exibe sugestões de Nick e Tag com a opção de selecionar um para trocar. """
    while True:
        system("cls")
        console.print(Panel.fit("Gerador de Nick", style="bold magenta"))

        sugestões = []
        
        # Gerar 5 nicks e tags e armazenar com índice
        for i in range(5):
            nick_gerado = gerar_caracteres(MAX_NAME_LENGTH)
            tag_gerada = gerar_caracteres(MAX_TAG_LENGTH)
            sugestões.append((nick_gerado, tag_gerada))
            console.print(f"[cyan]{i+1}. {nick_gerado}[/]#[yellow]{tag_gerada}[/]")

        # Pergunta para o usuário escolher um ou gerar mais
        escolha = Prompt.ask("\n[bold cyan]Deseja selecionar algum nick (digite o número)?[/]", choices=["1", "2", "3", "4", "5", "n"])
        
        if escolha.lower() == 'n':
            system("cls")
            escolha = Prompt.ask("\n[bold cyan]Deseja gerar mais?[/]", choices=["y", "n"])
            if escolha == "n":
                break
            continue

        elif escolha in ["1", "2", "3", "4", "5"]:
            # Se escolher um número, trocar o Riot ID para o escolhido
            selected_index = int(escolha) - 1
            selected_nick, selected_tag = sugestões[selected_index]
            
            # Aqui você já pode realizar a troca, preenchendo os campos
            change_riotid(selected_nick, selected_tag)
            break
        else:
            break  # Se sair, volta ao menu anterior


def riotid_menu():
    while True:
        system("cls")
        console.print(Panel.fit("Riot ID Menu", style="bold cyan"))
        console.print("[1] Trocar Riot ID", style="bold cyan")
        console.print("[2] Gerar nick", style="bold cyan")
        console.print("[3] Sair", style="bold red")

        escolha = Prompt.ask("\n[bold cyan]Escolha uma opção[/]", choices=["1", "2", "3"])

        if escolha == "1":
            change_riotid_menu()
        elif escolha == "2":
            show_suggestions()
        elif escolha == "3":
            console.print("[bold red]Saindo...[/]")
            break