# Programa de Automação Interna
# Desenvolvido por Natanael Flores Martins - © 2025
# Licenciado sob a "Licença de Uso"

licenca = '''1. Concessão de Licença de Uso
O presente software foi desenvolvido exclusivamente por Natanael Flores Martins, e é cedido, em caráter não exclusivo, à empresa SUPERMERCADOS GUANABARA, unicamente durante o período em que o autor mantiver vínculo formal com a referida empresa, seja por contrato de trabalho ou prestação de serviços.

Caso qualquer uma das partes rescinda o vínculo trabalhista ou contratual, o autor, no exercício de seus direitos, poderá retirar o software da rede da empresa, cessando imediatamente a licença de uso concedida, sem que tal ato implique em qualquer direito a compensações ou indenizações para a empresa. A retirada do software poderá ocorrer a qualquer momento após o término da relação contratual.

A utilização, reprodução, modificação, distribuição, sublicenciamento ou qualquer outra forma de exploração deste software, total ou parcial, não será permitida após o encerramento do referido vínculo, salvo mediante autorização expressa e por escrito do autor.

2. Restrições de Uso
É expressamente vedado o uso deste software para fins comerciais externos à SUPERMERCADOS GUANABARA, bem como sua aplicação em unidades diversas da empresa, sem o consentimento prévio e formal do autor.

Fica proibida a revenda, sublicenciamento, cessão ou redistribuição do software, sob qualquer forma, a terceiros.

3. Direitos Autorais
O autor se reserva todos os direitos morais e patrimoniais sobre o código-fonte, nos termos da Lei de Direitos Autorais (Lei nº 9.610/98).

Qualquer versão modificada ou adaptada deste software, desde que devidamente autorizada, deverá manter expressamente a identificação da autoria original de Natanael Flores Martins.

4. Isenção de Garantias
Este software é fornecido "no estado em que se encontra", sem garantias de funcionamento contínuo, suporte técnico ou atualizações, salvo se houver acordo específico e formal entre as partes.

5. Cláusula Resolutiva
O descumprimento de quaisquer das condições aqui estabelecidas, bem como o uso indevido do software ou a violação dos direitos autorais, poderá ensejar a revogação imediata da licença de uso por parte do autor, sem prejuízo das medidas legais cabíveis.

6. Contato para Autorizações
Para solicitações de uso após o encerramento do vínculo contratual, ou para qualquer outro fim que extrapole os limites aqui definidos nesses termos, deverá ser feito contato diretamente com o autor através do e-mail:

📧 natanaelfmartins7890@hotmail.com 


© 2025 Quark CO. Todos os direitos reservados.'''

import threading
import customtkinter as ctk
import time
import os
from PIL import Image
import customtkinter as ctk
from pynput.mouse import Listener, Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener


# Constantes para otimizar valores repetidos
DISTANCIA_PAD = 5
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Calibri", 14, "bold")
FONT_ENTRY = ("Segoe UI", 11)
FONT_TERMINAL = ("Consolas", 12)
TERMINAL_LARGURA = 530  # Largura do terminal
TERMINAL_ALTURA = 200   # Altura do terminal
BORDAS = 4

mouse = Controller()
teclado = KeyboardController()

# Variáveis globais
quantidade = 0
tempo = 0

ultimo_botao = ""
captura_ativa = False  # Indica se devemos capturar coordenadas
ctrl_pressed = False
parar_execucao = False
escutador_esc = None
lista_tarefas = []
triagem_tarefas = {}


# Funções do Programa

# Funções Da Interface
def nome_task(grade, nome_botao, linha, coluna, colunas_ocupadas=1, task=None, distancia=(1.5, 3), width=100, height=30, color='#2A5EBC', color_mouse='#034297'):
    global ultimo_botao

    def wrapper():
        global ultimo_botao
        ultimo_botao = nome_botao
        if task:
           task()
            
    botao = ctk.CTkButton(grade, text=nome_botao, command=wrapper, width=width, height=height, corner_radius=BORDAS, font=FONT_BUTTON, fg_color=color, hover_color=color_mouse)
    botao.grid(row=linha, column=coluna, padx=1, pady=distancia,columnspan=colunas_ocupadas, sticky='nsew')
    
# Funções dos Botões

# Funções para capturar eventos do teclado
def on_press(key):
    global ctrl_pressed
    if key in (Key.ctrl_l, Key.ctrl_r):
        ctrl_pressed = True

def on_release(key):
    global ctrl_pressed
    if key in (Key.ctrl_l, Key.ctrl_r):
        ctrl_pressed = False

def esc_listener():
    global escutador_esc

    def esc_pressionado(tecla):
        global parar_execucao
        if tecla == Key.esc:
            terminal_tarefas.insert("end", "Interrompendo Execução ao Fim do Loop.!\n")
            terminal_tarefas.see("end")
            parar_execucao = True
            return False

    if escutador_esc is not None and escutador_esc.running:
        escutador_esc.stop()

    escutador_esc = KeyboardListener(on_press=esc_pressionado)
    escutador_esc.start()

# Função para capturar coordenadas do clique
def capturar_coordenadas(x, y, button, pressed):
    global captura_ativa, lista_tarefas, triagem_tarefas, ultimo_botao
    if captura_ativa and ctrl_pressed and pressed:
        if ultimo_botao == 'CLIQUE':
            triagem_tarefas[ultimo_botao] = {"coordenadas": (x, y), "func": lambda: clicar(x, y)}

        if ultimo_botao == 'CLIQUE DUPLO':
            triagem_tarefas[ultimo_botao] = {"coordenadas": (x, y), "func": lambda: clicar_duplo(x, y)}

        lista_tarefas.append(triagem_tarefas.copy())
        triagem_tarefas.clear()
        terminal_comandos.insert("end", f"As coordenadas X: {x} e Y: {y} foram salvas!\n")
        terminal_comandos.see("end")
        captura_ativa = False  # Desativa a captura até o próximo clique no botão

def adicionar_acao(nome, funcao):
    global lista_tarefas
    lista_tarefas.append({nome: funcao})
    terminal_comandos.insert("end", f"Comando {nome} foi salvo!\n")
    terminal_comandos.see("end")

# Iniciar os Listeners apenas uma vez
def iniciar_listeners():
    threading.Thread(target=esc_listener, daemon=True).start()
    threading.Thread(target=lambda: KeyboardListener(on_press=on_press, on_release=on_release).run(), daemon=True).start()
    threading.Thread(target=lambda: Listener(on_click=capturar_coordenadas).run(), daemon=True).start()

# Função chamada para mapear as coordenadas.
def mapear_coordenadas():
    global captura_ativa
    terminal_comandos.insert("end", "Pressione CTRL + Botão esquerdo para salvar.\n")
    terminal_comandos.see("end")
    captura_ativa = True  # Ativa a captura de coordenadas]

# Função chamada para dar um clique no botão esquerdo do Mouse.
def executar():
    global quantidade, tempo, parar_execucao, escutador_esc
    parar_execucao = False

    esc_listener()

    try:
        quantidade = int(campo_quant.get())
        tempo = float(campo_segundo.get())

        if quantidade <= 0 or tempo <= 0:
            raise ValueError

        if not lista_tarefas:
            terminal_tarefas.insert('end', 'Não há comandos a executar.\n')
            terminal_tarefas.see("end")
        
        else:
            win()
            for execucao in range(1, quantidade + 1):
                if parar_execucao:
                    terminal_tarefas.insert("end", "Execução Interrompida!\n")
                    terminal_tarefas.see("end")
                    break

                for tarefas in lista_tarefas:
                    for chave, valor in tarefas.items():
                        if isinstance(valor, dict) and 'func' in valor:
                            valor['func']()
                        elif callable(valor):
                            valor()
    except ValueError:
        terminal_tarefas.insert('end', 'Verifique os campos: Tempo e Quantidade, nenhum deles pode ser 0.\n')

def deletar_item():
    if lista_tarefas == []:
        terminal_tarefas.insert("end", "A Lista de Execuções está vazia.\n")
        terminal_tarefas.see("end")
    else:
        lista_tarefas.pop()
        terminal_tarefas.insert("end", "Último comando removido da lista.\n")
        terminal_tarefas.see("end")

def deletar_lista():
    if lista_tarefas == []:
        terminal_tarefas.insert("end", "A Lista de Execuções está vazia.\n")
        terminal_tarefas.see("end")
    else:
        lista_tarefas.clear()
        terminal_tarefas.insert("end", "Todos os comandos foram removidos da lista.\n")
        terminal_tarefas.see("end")

def clicar(x, y):
    global tempo
    time.sleep(tempo)
    mouse.position = (x, y)
    time.sleep(0.3)
    mouse.click(Button.left, 1)
    time.sleep(0.4)

# Função chamada para dar dois clique no botão esquerdo do Mouse.
def clicar_duplo(x, y):
    global tempo
    time.sleep(tempo)
    mouse.position = (x, y)
    time.sleep(0.3)
    mouse.click(Button.left, 2)
    time.sleep(0.3)

# Função para Copiar a informação selecionada.
def copiar():
    time.sleep(tempo)
    teclado.press(Key.ctrl)
    teclado.press('c')
    time.sleep(0.3)
    teclado.release('c')
    teclado.release(Key.ctrl)
    time.sleep(0.3)

# Função para Colar a informação copiada.
def colar():  
    time.sleep(tempo)
    teclado.press(Key.ctrl)
    teclado.press('v')
    time.sleep(0.3)
    teclado.release('v')
    teclado.release(Key.ctrl)
    time.sleep(0.3)

# Função para apertar F2 (limpar na Consinco).
def limpar():
    time.sleep(tempo)
    teclado.press(Key.f2)
    time.sleep(0.2)
    teclado.release(Key.f2)

# Função para apertar F4 (e salvar na Consinco)
def salvar():
    time.sleep(tempo)
    teclado.press(Key.f4)
    time.sleep(0.3)
    teclado.release(Key.f4)
    time.sleep(0.3)

# Função para apertar F8 (pesquisar na Consinco).
def pesquisar():
    time.sleep(tempo)
    teclado.press(Key.f8)
    time.sleep(0.2)
    teclado.release(Key.f8)
    time.sleep(0.3)

# Função para apertar a tecla Enter.
def enter():
    time.sleep(tempo)
    teclado.press(Key.enter)
    time.sleep(tempo)
    teclado.release(Key.enter)
    time.sleep(0.3)

def selecionar_tudo():  # Função para minimizar o Script.
    time.sleep(tempo)
    teclado.press(Key.ctrl_l)
    teclado.press(Key.shift_l)
    teclado.press('a')
    time.sleep(0.3)
    teclado.release('a')
    teclado.release(Key.shift_l)
    teclado.release(Key.ctrl_l)

def backspace():
    time.sleep(tempo)
    teclado.press(Key.backspace)
    time.sleep(tempo)
    teclado.release(Key.backspace)
    time.sleep(0.3)
    
def win():  # Função para minimizar o Script.
    time.sleep(tempo)
    teclado.press(Key.cmd)
    teclado.press(Key.down)
    time.sleep(0.3)
    teclado.release(Key.down)
    teclado.release(Key.cmd)

def abrir_termos():
    termos_window = ctk.CTkToplevel()
    termos_window.title("Termos de Uso")
    termos_window.geometry("450x350")  # Ajuste conforme quiser

    termos_window.attributes('-topmost', True)

    # Texto dos termos (exemplo de como quebrar a linha e formatar o texto)


    # Usando CTkLabel para exibir o texto
    termos_scroll = ctk.CTkScrollableFrame(termos_window)
    termos_scroll.pack(padx=2, pady=2, fill="both", expand=True)

    termos_label = ctk.CTkLabel(termos_scroll, text=licenca, anchor="nw", justify="left", wraplength=390, font=("Times New Roman", 14))
    termos_label.pack(padx=1, pady=1)

# Função para mostrar a Lista atual.
def mostrar_lista():
    global lista_tarefas

    terminal_tarefas.delete("1.0", "end")

    if lista_tarefas == []:
        terminal_tarefas.insert("end",  "Não há comandos a executar.\n")
        terminal_tarefas.see("end")

    else:
        for i, tarefas in enumerate(lista_tarefas):
            for chave, valor in tarefas.items():
                if isinstance(valor, dict) and 'coordenadas' in valor:
                    x, y = valor['coordenadas']
                    terminal_tarefas.insert("end",  f"{i+1}º {chave} - X:{x} Y:{y}\n")
                elif callable(valor):
                    terminal_tarefas.insert("end",  f"{i+1}º {chave}\n")
                else:
                    terminal_tarefas.insert("end",  f"{i+1}º {chave} - Tipo não Reconhecido.\n")

                terminal_tarefas.see("end")
                terminal_tarefas.clipboard_clear()

# Configurações da Janela
alccor = ctk.CTk()
alccor.title('Módulo Alccor - v2.0')
alccor.geometry('650x370')
alccor.grid_columnconfigure(0, weight=1, uniform="terminal")  # Coluna para o terminal
alccor.grid_columnconfigure(1, weight=1, uniform="terminal")  # Coluna para o terminal
alccor.grid_rowconfigure(2, weight=1)
alccor.grid_rowconfigure(3, weight=0)
ctk.set_appearance_mode("dark")


frame_esquerdo = ctk.CTkScrollableFrame(alccor, width=406, height=15)  # Ajuste a largura e altura conforme necessário
frame_esquerdo.grid(row=2, column=0, padx=(5, 5), pady=(25,25), sticky="nw", columnspan=2)

frame_direito = ctk.CTkFrame(alccor)  # Criamos um bloco dentro do atlas
frame_direito.grid(row=2, column=1, padx=5, pady=(10, 0), sticky="ne", columnspan=2)

# Configuração Tempo e Quantidade
label_segundo = ctk.CTkLabel(frame_direito, text='TEMPO', width=10, height=30, font=FONT_LABEL)
label_segundo.grid(row=2, column=0, padx=3, pady=1)

label_quant = ctk.CTkLabel(frame_direito, text='QUANT.', width=10, height=30, font=FONT_LABEL)
label_quant.grid(row=2, column=1, padx=3, pady=1)

campo_segundo = ctk.CTkEntry(frame_direito, width=50, height=20, placeholder_text='00:00', justify='center', font=FONT_ENTRY, corner_radius=BORDAS)
campo_segundo.grid(row=3, column=0, padx=0, pady=0)
campo_quant = ctk.CTkEntry(frame_direito, width=45, height=20, placeholder_text='0', justify='center', font=FONT_ENTRY, corner_radius=BORDAS)
campo_quant.grid(row=3, column=1, padx=0, pady=0)

# Configurações no Terminal
terminal_comandos = ctk.CTkTextbox(alccor, width=TERMINAL_LARGURA, height=TERMINAL_ALTURA, wrap="word", font=FONT_TERMINAL,
                          corner_radius=3.5, fg_color="black", text_color="white")
terminal_comandos.grid(row=0, column=0, padx=(4, 2), pady=(DISTANCIA_PAD, 3), columnspan=1, sticky="")

terminal_tarefas = ctk.CTkTextbox(alccor, width=TERMINAL_LARGURA, height=TERMINAL_ALTURA, wrap="word", font=FONT_TERMINAL,
                          corner_radius=3.5, fg_color="black", text_color="white")
terminal_tarefas.grid(row=0, column=1, padx=(2, 4), pady=(DISTANCIA_PAD, 3), columnspan=1, sticky="")

terms_use = ctk.CTkButton(alccor, text='TERMOS DE USO', command=abrir_termos, width=50, height=15, font=("Calibri", 10, "bold"), corner_radius=4, fg_color='#2A5EBC', hover_color='#034297')
terms_use.grid(row=3, column=0, pady=(0, 7), padx=7, sticky='sw')


# Botões (Usando a função `button`)

nome_task(frame_esquerdo, 'CLIQUE', distancia=(4.5,3), task=mapear_coordenadas, linha=1, coluna=0)
nome_task(frame_esquerdo, 'CLIQUE DUPLO', distancia=(4.5,3), task=mapear_coordenadas, linha=1, coluna=1)

nome_task(frame_esquerdo, 'COPIAR', distancia=(4.5,3), task=lambda:adicionar_acao('COPIAR', copiar), linha=1, coluna=2)
nome_task(frame_esquerdo, 'COLAR', distancia=(4.5,3), task=lambda:adicionar_acao('COLAR', colar), linha=1, coluna=3)
nome_task(frame_esquerdo, 'LIMPAR', task=lambda:adicionar_acao('LIMPAR', limpar), linha=2, coluna=0)
nome_task(frame_esquerdo, 'SALVAR', task=lambda:adicionar_acao('SALVAR', salvar),linha=2, coluna=1)
nome_task(frame_esquerdo, 'PESQUISAR', task=lambda:adicionar_acao('PESQUISAR', pesquisar), linha=2, coluna=2)
nome_task(frame_esquerdo, 'ENTER', task=lambda:adicionar_acao('ENTER', enter), linha=2, coluna=3)
nome_task(frame_esquerdo, 'SELECIONAR', task=lambda:adicionar_acao('SELECIONAR', selecionar_tudo), linha=3, coluna=0)
nome_task(frame_esquerdo, 'BACKSPACE', task=lambda:adicionar_acao('BACKSPACE', backspace), linha=3, coluna=1)

nome_task(frame_direito, 'EXECUTAR', task=lambda: threading.Thread(target=executar, daemon=True).start(), linha=0, coluna=1, width=45, color='#07A931', color_mouse='#039318')
nome_task(frame_direito, 'TAREFAS', task=mostrar_lista, linha=0, coluna=0, width=45, color='#FE470E', color_mouse='#CB3101')
nome_task(frame_direito, 'LIMPAR ITENS', task=deletar_item, linha=1, coluna=0, width=45, color='#9D9D9D', color_mouse='#888888')
nome_task(frame_direito, 'LIMPAR LISTA', task=deletar_lista, linha=1, coluna=1, width=45, color='#9D9D9D', color_mouse='#888888')

# Caminho para o ícone
icone_path = r"C:\Users\Natanael\Desktop\Programação\Python\Projetos\Modulo Alccor\Imagens\alccor.ico"
alccor.iconbitmap(icone_path)

iniciar_listeners()

alccor.mainloop()
