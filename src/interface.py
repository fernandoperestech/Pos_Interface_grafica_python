import tkinter as tk
from tkinter import ttk

def iniciar_interface(db):
    root = tk.Tk()
    root.title("Sistema de Imóveis")

    # Cria um notebook (sistema de abas)
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    # ==================== Frame Cadastro ====================
    frame_cadastro = ttk.Frame(notebook, width=400, height=280)
    frame_cadastro.pack(fill="both", expand=True)

    # Função para cadastrar imóvel
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

    # Campos de cadastro
    lbl_tipo_negociacao = ttk.Label(frame_cadastro, text="Tipo de Negociação")
    lbl_tipo_negociacao.grid(row=0, column=0, padx=10, pady=5)
    combo_tipo_negociacao = ttk.Combobox(frame_cadastro, values=["Venda", "Locação", "Venda/Locação"])
    combo_tipo_negociacao.grid(row=0, column=1, padx=10, pady=5)

    lbl_status = ttk.Label(frame_cadastro, text="Status")
    lbl_status.grid(row=1, column=0, padx=10, pady=5)
    combo_status = ttk.Combobox(frame_cadastro, values=["Disponível", "Locado", "Vendido", "À liberar"])
    combo_status.grid(row=1, column=1, padx=10, pady=5)

    lbl_preco = ttk.Label(frame_cadastro, text="Preço")
    lbl_preco.grid(row=2, column=0, padx=10, pady=5)
    entry_preco = ttk.Entry(frame_cadastro)
    entry_preco.grid(row=2, column=1, padx=10, pady=5)

    lbl_descricao = ttk.Label(frame_cadastro, text="Descrição")
    lbl_descricao.grid(row=3, column=0, padx=10, pady=5)
    entry_descricao = ttk.Entry(frame_cadastro)
    entry_descricao.grid(row=3, column=1, padx=10, pady=5)

    lbl_caracteristicas = ttk.Label(frame_cadastro, text="Características")
    lbl_caracteristicas.grid(row=4, column=0, padx=10, pady=5)
    entry_caracteristicas = ttk.Entry(frame_cadastro)
    entry_caracteristicas.grid(row=4, column=1, padx=10, pady=5)

    lbl_observacoes = ttk.Label(frame_cadastro, text="Observações")
    lbl_observacoes.grid(row=5, column=0, padx=10, pady=5)
    entry_observacoes = ttk.Entry(frame_cadastro)
    entry_observacoes.grid(row=5, column=1, padx=10, pady=5)

    btn_cadastrar = ttk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_imovel)
    btn_cadastrar.grid(row=6, column=1, padx=10, pady=10)

    # ==================== Frame Pesquisa/Editar ====================
    frame_pesquisa = ttk.Frame(notebook, width=400, height=400)
    frame_pesquisa.pack(fill="both", expand=True)

    # Função para verificar se um valor pode ser convertido para inteiro
    def is_convertible_to_int(value):
        try:
            int(value)  # Tenta converter para inteiro
            return True
        except (ValueError, TypeError):
            return False  # Retorna False se ocorrer um erro

    # Função para carregar imóvel selecionado
    def carregar_imovel(event):
        selected_index = listbox_result.curselection()
        if selected_index:
            imovel_id = listbox_result.get(selected_index)[0]  # Primeiro elemento é o ID do imóvel
            imovel_data = db.query_data('imovel', '*', f'pk_imovel = {imovel_id}')[0]  # Carrega os dados do imóvel

            # Verifica e converte os índices corretamente
            if is_convertible_to_int(imovel_data[6]):  # Verifica fk_tipo_negociacao
                tipo_negociacao_index = int(imovel_data[6]) - 1  # Converte para int e ajusta o índice
                combo_pesquisa_tipo_negociacao.current(tipo_negociacao_index)
            else:
                print(f"Valor inválido para tipo de negociação: {imovel_data[6]}")

            if is_convertible_to_int(imovel_data[7]):  # Verifica fk_status
                status_index = int(imovel_data[7]) - 1  # Converte para int e ajusta o índice
                combo_pesquisa_status.current(status_index)
            else:
                print(f"Valor inválido para status: {imovel_data[7]}")

            # Preenche os campos de edição com os dados do imóvel selecionado
            entry_pesquisa_preco.delete(0, tk.END)
            entry_pesquisa_preco.insert(0, imovel_data[5])
            entry_pesquisa_descricao.delete(0, tk.END)
            entry_pesquisa_descricao.insert(0, imovel_data[1])
            entry_pesquisa_caracteristicas.delete(0, tk.END)
            entry_pesquisa_caracteristicas.insert(0, imovel_data[2])
            entry_pesquisa_observacoes.delete(0, tk.END)
            entry_pesquisa_observacoes.insert(0, imovel_data[4])


    # Função para editar e salvar imóvel
    def salvar_imovel():
        selected_index = listbox_result.curselection()
        if selected_index:
            imovel_id = listbox_result.get(selected_index)[0]  # Primeiro elemento é o ID do imóvel

            imovel_data = {
                'fk_tipo_negociacao': combo_pesquisa_tipo_negociacao.get(),
                'fk_status': combo_pesquisa_status.get(),
                'imo_preco': entry_pesquisa_preco.get(),
                'imo_descricao': entry_pesquisa_descricao.get(),
                'imo_caracteristica': entry_pesquisa_caracteristicas.get(),
                'imo_observacoes': entry_pesquisa_observacoes.get()
            }
            db.update_data('imovel', imovel_data, f'pk_imovel = {imovel_id}')
            print(f"Imóvel {imovel_id} atualizado com sucesso!")

    # Função para excluir imóvel
    def excluir_imovel():
        selected_index = listbox_result.curselection()
        if selected_index:
            imovel_id = listbox_result.get(selected_index)[0]  # Primeiro elemento é o ID do imóvel
            db.delete_data('imovel', f'pk_imovel = {imovel_id}')
            print(f"Imóvel {imovel_id} excluído com sucesso!")
            listbox_result.delete(selected_index)  # Remove o item da Listbox

    # Pesquisa e exibição de imóveis
    def pesquisar_imovel():
        tipo_negociacao = combo_pesquisa_tipo_negociacao.get()
        status = combo_pesquisa_status.get()

        # Condição de pesquisa
        condition = []
        if tipo_negociacao:
            condition.append(f"fk_tipo_negociacao = {combo_pesquisa_tipo_negociacao.current() + 1}")
        if status:
            condition.append(f"fk_status = {combo_pesquisa_status.current() + 1}")
        
        condition_str = " AND ".join(condition) if condition else None
        result = db.query_data('imovel', '*', condition_str)

        # Exibe os resultados na Listbox
        listbox_result.delete(0, tk.END)
        for row in result:
            listbox_result.insert(tk.END, row)

    # Campos de pesquisa/edição
    lbl_pesquisa_tipo_negociacao = ttk.Label(frame_pesquisa, text="Tipo de Negociação")
    lbl_pesquisa_tipo_negociacao.grid(row=0, column=0, padx=10, pady=5)
    combo_pesquisa_tipo_negociacao = ttk.Combobox(frame_pesquisa, values=["Venda", "Locação", "Venda/Locação"])
    combo_pesquisa_tipo_negociacao.grid(row=0, column=1, padx=10, pady=5)

    lbl_pesquisa_status = ttk.Label(frame_pesquisa, text="Status")
    lbl_pesquisa_status.grid(row=1, column=0, padx=10, pady=5)
    combo_pesquisa_status = ttk.Combobox(frame_pesquisa, values=["Disponível", "Locado", "Vendido", "À liberar"])
    combo_pesquisa_status.grid(row=1, column=1, padx=10, pady=5)

    lbl_pesquisa_preco = ttk.Label(frame_pesquisa, text="Preço")
    lbl_pesquisa_preco.grid(row=2, column=0, padx=10, pady=5)
    entry_pesquisa_preco = ttk.Entry(frame_pesquisa)
    entry_pesquisa_preco.grid(row=2, column=1, padx=10, pady=5)

    lbl_pesquisa_descricao = ttk.Label(frame_pesquisa, text="Descrição")
    lbl_pesquisa_descricao.grid(row=3, column=0, padx=10, pady=5)
    entry_pesquisa_descricao = ttk.Entry(frame_pesquisa)
    entry_pesquisa_descricao.grid(row=3, column=1, padx=10, pady=5)

    lbl_pesquisa_caracteristicas = ttk.Label(frame_pesquisa, text="Características")
    lbl_pesquisa_caracteristicas.grid(row=4, column=0, padx=10, pady=5)
    entry_pesquisa_caracteristicas = ttk.Entry(frame_pesquisa)
    entry_pesquisa_caracteristicas.grid(row=4, column=1, padx=10, pady=5)

    lbl_pesquisa_observacoes = ttk.Label(frame_pesquisa, text="Observações")
    lbl_pesquisa_observacoes.grid(row=5, column=0, padx=10, pady=5)
    entry_pesquisa_observacoes = ttk.Entry(frame_pesquisa)
    entry_pesquisa_observacoes.grid(row=5, column=1, padx=10, pady=5)

    # Botões de pesquisa, salvar e excluir
    btn_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_imovel)
    btn_pesquisar.grid(row=6, column=0, padx=10, pady=10)

    btn_salvar = ttk.Button(frame_pesquisa, text="Salvar Alterações", command=salvar_imovel)
    btn_salvar.grid(row=6, column=1, padx=10, pady=10)

    btn_excluir = ttk.Button(frame_pesquisa, text="Excluir Imóvel", command=excluir_imovel)
    btn_excluir.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # Listbox para exibir resultados
    listbox_result = tk.Listbox(frame_pesquisa, width=50)
    listbox_result.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
    listbox_result.bind('<<ListboxSelect>>', carregar_imovel)

    # ==================== Adiciona as abas ao Notebook ====================
    notebook.add(frame_cadastro, text="Cadastro de Imóveis")
    notebook.add(frame_pesquisa, text="Pesquisa/Editar Imóveis")

    root.mainloop()

