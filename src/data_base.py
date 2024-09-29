import os
import sqlite3

class Database:
    DB_NAME = 'py_assessoria.db'
    DB_FOLDER = 'data_base'
    os.makedirs(DB_FOLDER, exist_ok=True)
    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    
    TABLE_TIPO_NEGOCIACAO = 'tipo_negociacao'
    TABLE_STATUS = 'status'
    TABLE_ENDERECO = 'endereco'
    TABLE_TIPO_IMOVEL = 'tipo_imovel'
    TABLE_IMOVEL = 'imovel'

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
        self.cursor.execute(query)
        self.conn.commit()

    def create_tables(self):
        self.create_table(self.TABLE_TIPO_NEGOCIACAO, [
            'pk_tip_negociacao INTEGER PRIMARY KEY AUTOINCREMENT',
            'neg_nome TEXT NOT NULL'
        ])
        
        self.create_table(self.TABLE_STATUS, [
            'pk_status INTEGER PRIMARY KEY AUTOINCREMENT',
            'sta_nome TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_ENDERECO, [
            'pk_endereco INTEGER PRIMARY KEY AUTOINCREMENT',
            'end_logradouro TEXT NOT NULL',
            'end_numero TEXT',
            'end_cep TEXT NOT NULL',
            'end_complemento TEXT'
        ])

        self.create_table(self.TABLE_TIPO_IMOVEL, [
            'pk_tipo_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'tim_nome TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_IMOVEL, [
            'pk_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'imo_descricao TEXT NOT NULL',
            'imo_caracteristica TEXT',
            'imo_condicoes TEXT',
            'imo_observacoes TEXT',
            'imo_preco REAL NOT NULL',
            'fk_tipo_negociacao INTEGER',
            'fk_status INTEGER',
            'fk_tipo_imovel INTEGER',
            'FOREIGN KEY(fk_tipo_negociacao) REFERENCES tipo_negociacao(pk_tip_negociacao)',
            'FOREIGN KEY(fk_status) REFERENCES status(pk_status)',
            'FOREIGN KEY(fk_tipo_imovel) REFERENCES tipo_imovel(pk_tipo_imovel)'
        ])

    import os
import sqlite3

class Database:
    DB_NAME = 'py_assessoria.db'
    DB_FOLDER = 'DataBase'
    os.makedirs(DB_FOLDER, exist_ok=True)
    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

    # Tabelas
    TABLE_TIPO_NEGOCIACAO = 'tipo_negociacao'
    TABLE_STATUS = 'status'
    TABLE_ENDERECO = 'endereco'
    TABLE_TIPO_IMOVEL = 'tipo_imovel'
    TABLE_IMOVEL = 'imovel'

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
        self.cursor.execute(query)
        self.conn.commit()

    def create_tables(self):
        self.create_table(self.TABLE_TIPO_NEGOCIACAO, [
            'pk_tip_negociacao INTEGER PRIMARY KEY AUTOINCREMENT',
            'neg_nome TEXT NOT NULL'
        ])
        
        self.create_table(self.TABLE_STATUS, [
            'pk_status INTEGER PRIMARY KEY AUTOINCREMENT',
            'sta_nome TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_TIPO_IMOVEL, [
            'pk_tipo_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'tim_nome TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_IMOVEL, [
            'pk_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'imo_descricao TEXT NOT NULL',
            'imo_caracteristica TEXT',
            'imo_condicoes TEXT',
            'imo_observacoes TEXT',
            'imo_preco REAL NOT NULL',
            'fk_tipo_negociacao INTEGER',
            'fk_status INTEGER',
            'fk_tipo_imovel INTEGER',
            'FOREIGN KEY(fk_tipo_negociacao) REFERENCES tipo_negociacao(pk_tip_negociacao)',
            'FOREIGN KEY(fk_status) REFERENCES status(pk_status)',
            'FOREIGN KEY(fk_tipo_imovel) REFERENCES tipo_imovel(pk_tipo_imovel)'
        ])

    # CREATE
    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        values = tuple(data.values())
        self.cursor.execute(query, values)
        self.conn.commit()

    # READ
    def query_data(self, table_name, columns='*', condition=None):
        query = f'SELECT {columns} FROM {table_name}'
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # UPDATE
    def update_data(self, table_name, data, condition):
        columns = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values())
        query = f'UPDATE {table_name} SET {columns} WHERE {condition}'
        self.cursor.execute(query, values)
        self.conn.commit()

    # DELETE
    def delete_data(self, table_name, condition):
        query = f'DELETE FROM {table_name} WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()


    def popular_tabelas_iniciais(self):
        try:
            # Verifica e insere tipos de negociação
            result_negociacao = self.query_data(self.TABLE_TIPO_NEGOCIACAO)
            if len(result_negociacao) == 0:
                lista_tipos_negociacao = [{'neg_nome': 'Venda'}, {'neg_nome': 'Locacao'}, {'neg_nome': 'Venda/Locação'}]
                for tipo in lista_tipos_negociacao:
                    self.insert_data(self.TABLE_TIPO_NEGOCIACAO, tipo)

            # Verifica e insere usuários
            result_user = self.query_data('usuario')
            if len(result_user) == 0:
                usuario = [{'usu_nome': 'Fernando', 'usu_senha': '123mudar'}]
                for tipo in usuario:
                    self.insert_data(self.TABLE_USER, tipo)

            # Verifica e insere status
            result_status = self.query_data(self.TABLE_STATUS)
            if len(result_status) == 0:
                lista_tipos_status = [{'sta_nome': 'Disponível'}, {'sta_nome': 'Locado'}, {'sta_nome': 'Vendido'}, {'sta_nome': 'À liberar'}]
                for tipo in lista_tipos_status:
                    self.insert_data(self.TABLE_STATUS, tipo)

            # Verifica e insere tipos de imóvel
            result_tipo_imovel = self.query_data(self.TABLE_TIPO_IMOVEL)
            if len(result_tipo_imovel) == 0:
                lista_tipos_imovel = [{'tim_nome': 'Apartamento'}, {'tim_nome': 'Casa'}, {'tim_nome': 'Terreno'}]
                for tipo in lista_tipos_imovel:
                    self.insert_data(self.TABLE_TIPO_IMOVEL, tipo)

            # Verifica e insere tipos de relação
            result_tipo_relacao = self.query_data('tipo_relacao')
            if len(result_tipo_relacao) == 0:
                lista_tipos_relacao = [{'tre_nome':'Comprador'},{'tre_nome':'Vendedor'},{'tre_nome':'Locatário'},{'tre_nome':'Locador'},{'tre_nome':'Investidor'},{'tre_nome':'Proprietário'}]
                for tipo in lista_tipos_relacao:
                    self.insert_data(self.TABLE_TIPO_RELACAO, tipo)

            # Verifica e insere estados
            result_estados = self.query_data('estado')
            if len(result_estados) == 0:
                lista_estados = [{'est_nome': 'Acre', 'est_uf': 'AC'}, ...]  # Adicione o restante dos estados
                for tipo in lista_estados:
                    self.insert_data(self.TABLE_ESTADO, tipo)

            # Verifica e insere cidades
            result_cidades = self.query_data('cidade')
            if len(result_cidades) == 0:
                lista_cidades = [{'cid_nome': 'Rio Branco', 'fk_estado': 1}, ...]  # Adicione o restante das cidades
                for tipo in lista_cidades:
                    self.insert_data(self.TABLE_CIDADE, tipo)

            # Verifica e insere bairros
            result_bairros = self.query_data('bairro')
            if len(result_bairros) == 0:
                lista_bairros = [{'bai_nome':'Bairro Verde','fk_cidade':1}, ...]  # Adicione o restante dos bairros
                for tipo in lista_bairros:
                    self.insert_data(self.TABLE_BAIRRO, tipo)

            # Adicione um imóvel padrão para testar
            imovel_data = {
                'imo_descricao': 'Casa exemplo',
                'imo_caracteristica': '3 quartos, 2 banheiros',
                'imo_condicoes': 'Bom estado',
                'imo_observacoes': 'Perto da escola',
                'imo_preco': 250000.00,
                'end_logradouro': 'Rua das Flores',
                'end_numero': '123',
                'end_complemento': 'Apto 202',
                'end_cep': '12345-678',
                'end_bairro': 'Bairro Verde',
                'end_cidade': 'Rio Branco',
                'end_estado': 'AC',
                'fk_tipo_negociacao': 1,  # 'Venda'
                'fk_status': 1,            # 'Disponível'
                'fk_tipo_imovel': 1        # 'Casa'
            }
            self.insert_data('imovel', imovel_data)

        except Exception as e:
            print(e)
