import tkinter as tk
from tkinter import ttk

def iniciar_interface(db):
    root = tk.Tk()
    root.title("Cadastro de Imóveis")

    # Tipo de Negociação
    lbl_tipo_negociacao = tk.Label(root, text="Tipo de Negociação")
    lbl_tipo_negociacao.grid(row=0, column=0)
    combo_tipo_negociacao = ttk.Combobox(root, values=["Venda", "Locação", "Venda/Locação"])
    combo_tipo_negociacao.grid(row=0, column=1)

    # Status do Imóvel
    lbl_status = tk.Label(root, text="Status")
    lbl_status.grid(row=1, column=0)
    combo_status = ttk.Combobox(root, values=["Disponível", "Locado", "Vendido", "À liberar"])
    combo_status.grid(row=1, column=1)

    # Preço
    lbl_preco = tk.Label(root, text="Preço")
    lbl_preco.grid(row=2, column=0)
    entry_preco = tk.Entry(root)
    entry_preco.grid(row=2, column=1)

    # Descrição
    lbl_descricao = tk.Label(root, text="Descrição")
    lbl_descricao.grid(row=3, column=0)
    entry_descricao = tk.Entry(root)
    entry_descricao.grid(row=3, column=1)

    # Características
    lbl_caracteristicas = tk.Label(root, text="Características")
    lbl_caracteristicas.grid(row=4, column=0)
    entry_caracteristicas = tk.Entry(root)
    entry_caracteristicas.grid(row=4, column=1)

    # Observações
    lbl_observacoes = tk.Label(root, text="Observações")
    lbl_observacoes.grid(row=5, column=0)
    entry_observacoes = tk.Entry(root)
    entry_observacoes.grid(row=5, column=1)

    # Função de cadastro
    def cadastrar_imovel():
        imovel_data = {
            'fk_tipo_negociacao': combo_tipo_negociacao.get(),
            'fk_status': combo_status.get(),
            'imo_preco': entry_preco.get(),
            'imo_descricao': entry_descricao.get(),
            'imo_caracteristica': entry_caracteristicas.get(),
            'imo_observacoes': entry_observacoes.get()
        }
        db.insert_data('imovel', imovel_data)
        print("Imóvel cadastrado com sucesso!")

    # Botão de Cadastrar
    btn_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar_imovel)
    btn_cadastrar.grid(row=6, column=1)

    root.mainloop()
