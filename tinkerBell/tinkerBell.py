import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

candidatos = []
votacao_ativa = False

janela = tk.Tk()
janela.title("Sistema de Votacao")

# Carregar imagem de fundo
imagem_fundo = Image.open("img/laranja fundo.jpg")
largura, altura = imagem_fundo.size

# Centralizar janela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela - largura) // 2
pos_y = (altura_tela - altura) // 2
janela.geometry(f"{largura}x{altura}")

imagem_fundo = imagem_fundo.resize((largura, altura), Image.Resampling.LANCZOS)
fundo_tk = ImageTk.PhotoImage(imagem_fundo)

canvas = tk.Canvas(janela, width=largura, height=altura)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=fundo_tk, anchor="nw")

def mostra_menu():
    canvas.create_text(largura // 2, 30, text="Escolha uma opcao:", fill="white", font=("Arial", 14, "bold"))

    frame_botao = tk.Frame(janela, bg="white", bd=0)
    frame_botao.place(relx=0.5, rely=0.1, anchor="center")

    def mudar_cor(botao, cor):
        botao.config(bg=cor)

    botao_cadastro = tk.Button(frame_botao, text="Cadastro de Candidato", command=cadastra_candidato, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"), bd=0)
    botao_cadastro.pack(side='left', padx=10)
    botao_cadastro.bind("<Enter>", lambda e: mudar_cor(botao_cadastro, "#FFCC66"))
    botao_cadastro.bind("<Leave>", lambda e: mudar_cor(botao_cadastro, "#FFA500"))

    botao_votacao = tk.Button(frame_botao, text="Iniciar Votacao", command=iniciar_votacao, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"), bd=0)
    botao_votacao.pack(side='left', padx=10)
    botao_votacao.bind("<Enter>", lambda e: mudar_cor(botao_votacao, "#FFCC66"))
    botao_votacao.bind("<Leave>", lambda e: mudar_cor(botao_votacao, "#FFA500"))

    botao_encerrar = tk.Button(frame_botao, text="Encerrar Votacao", command=encerrar_votacao, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"), bd=0)
    botao_encerrar.pack(side='left', padx=10)
    botao_encerrar.bind("<Enter>", lambda e: mudar_cor(botao_encerrar, "#FFCC66"))
    botao_encerrar.bind("<Leave>", lambda e: mudar_cor(botao_encerrar, "#FFA500"))

def adicionar_gif_pixelado(janela_alvo, caminho_gif):
    gif = Image.open(caminho_gif)
    escala = 0.4
    quadros = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        nova_largura = int(frame.width * escala)
        nova_altura = int(frame.height * escala)
        quadros.append(ImageTk.PhotoImage(frame.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)))

    canvas_gif = tk.Canvas(janela_alvo, width=quadros[0].width(), height=quadros[0].height(), highlightthickness=0, bg="white")
    canvas_gif.place(relx=0.5, rely=0.85, anchor="center")

    gif_id = canvas_gif.create_image(0, 0, anchor="nw", image=quadros[0])

    def animar(indice=0):
        canvas_gif.itemconfig(gif_id, image=quadros[indice])
        janela_alvo.after(300, animar, (indice + 1) % len(quadros))

    animar()

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry(f"{largura}x{altura}")
    janela_cadastro.configure(bg="white")

    frame = tk.Frame(janela_cadastro, bg="white")
    frame.place(relx=0.5, rely=0.35, anchor="center")

    for texto in ["Número do Candidato:", "Nome do Candidato:", "Partido do Candidato:"]:
        tk.Label(frame, text=texto, bg="white", font=("Helvetica", 12)).pack(pady=4)
        tk.Entry(frame, fg="orange").pack(pady=4)

    entrada_numero, entrada_nome, entrada_partido = frame.winfo_children()[1], frame.winfo_children()[3], frame.winfo_children()[5]

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()
        candidatos.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0})
        messagebox.showinfo("Sucesso", "🍊Candidato cadastrado com sucesso!🍊")
        janela_cadastro.destroy()

    def mudar_cor(botao, cor):
        botao.config(bg=cor)

    botao_salvar = tk.Button(frame, text="Salvar", command=salvar_candidato, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"), bd=0)
    botao_salvar.pack(pady=10)
    botao_salvar.bind("<Enter>", lambda e: mudar_cor(botao_salvar, "#FFCC66"))
    botao_salvar.bind("<Leave>", lambda e: mudar_cor(botao_salvar, "#FFA500"))

    adicionar_gif_pixelado(janela_cadastro, "img/laranja_pixel.gif")

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votacao")
        janela_votacao.geometry(f"{largura}x{altura}")
        janela_votacao.configure(bg="white")

        frame = tk.Frame(janela_votacao, bg="white")
        frame.place(relx=0.5, rely=0.35, anchor="center")

        tk.Label(frame, text="Digite sua matricula:", bg="white", font=("Helvetica", 12)).pack(pady=5)
        entrada_matricula = tk.Entry(frame, fg="orange")
        entrada_matricula.pack(pady=5)

        tk.Label(frame, text="Digite o numero do candidato:", bg="white", font=("Helvetica", 12)).pack(pady=5)
        entrada_voto = tk.Entry(frame, fg="orange")
        entrada_voto.pack(pady=5)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()

            if not matricula:
                messagebox.showwarning("Erro", "🍊Matricula nao pode ser vazia.🍊")
                return

            candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)
            if candidato_escolhido:
                confirmar = messagebox.askyesno("Confirmacao", f"🍊Confirmar voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?🍊")
                if confirmar:
                    candidato_escolhido["votos"] += 1
                    messagebox.showinfo("Obrigado!", "🍊 Seu voto foi computado com sucesso! 🍊")
                    janela_votacao.destroy()
                    registrar_voto()
            else:
                confirmar = messagebox.askyesno("Confirmacao", "🍊Candidato inexistente. Confirmar voto nulo?🍊")
                if confirmar:
                    messagebox.showinfo("Sucesso", "🍊Voto nulo registrado!🍊")
                    janela_votacao.destroy()
                    registrar_voto()

        def mudar_cor(botao, cor):
            botao.config(bg=cor)

        botao_votar = tk.Button(frame, text="Votar", command=confirmar_voto, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"), bd=0)
        botao_votar.pack(pady=10)
        botao_votar.bind("<Enter>", lambda e: mudar_cor(botao_votar, "#FFCC66"))
        botao_votar.bind("<Leave>", lambda e: mudar_cor(botao_votar, "#FFA500"))

        adicionar_gif_pixelado(janela_votacao, "img/laranja_pixel.gif")

def salvar_relatorio_txt():
    with open("relatorio_votacao.txt", "w") as f:
        for c in candidatos:
            f.write(f"{c['nome']} ({c['partido']}): {c['votos']} votos\n")
    messagebox.showinfo("Relatorio Salvo", "🍊O relatorio foi salvo como 'relatorio_votacao.txt'.🍊")

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry(f"{largura}x{altura}")

    total_votos = sum(c["votos"] for c in candidatos)
    if total_votos > 0:
        for candidato in candidatos:
            tk.Label(janela_relatorio, text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos").pack(pady=5)
    else:
        tk.Label(janela_relatorio, text="Nao houve votos validos.").pack(pady=5)

    salvar_relatorio_txt()

    botao_fechar = tk.Button(janela_relatorio, text="Fechar", command=janela_relatorio.destroy)
    botao_fechar.pack(pady=5)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostra_menu()
janela.mainloop()
