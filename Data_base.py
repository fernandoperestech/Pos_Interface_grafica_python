import os
import sqlite3

class Database:
    DB_NAME = 'py_assessoria.db'
    DB_FOLDER = 'DataBase'
    os.makedirs(DB_FOLDER, exist_ok=True)
    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    TABLE_INSERT_IS_TRUE = 'insert_is_true'
    TABLE_TIPO_NEGOCIACAO = 'tipo_negociacao'
    TABLE_STATUS = 'status'
    TABLE_ENDERECO = 'endereco'
    TABLE_USER = 'usuario'
    TABLE_BAIRRO = 'bairro'
    TABLE_CIDADE = 'cidade'
    TABLE_ESTADO = 'estado'
    TABLE_TIPO_IMOVEL = 'tipo_imovel'
    TABLE_IMOVEL = 'imovel'
    TABLE_CLIENTE = 'cliente'
    TABLE_RELACAO_IMOVEL_CLIENTE = 'relacao_imovel_cliente'
    TABLE_TIPO_RELACAO = 'tipo_relacao'

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        try:
            columns_str = ', '.join(columns)
            query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})'
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)

    def create_tables(self):
        # self.create_table(self.TABLE_INSERT_IS_TRUE,[
        #     '',
        #     '',
        # ])
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
            'end_numero TEXT NOT NULL',
            'end_cep TEXT NOT NULL',
            'end_complemento TEXT NOT NULL',
            'fk_bairro INTEGER',
            'FOREIGN KEY(fk_bairro) REFERENCES bairro (pk_bairro)'
        ])

        self.create_table(self.TABLE_BAIRRO, [
            'pk_bairro INTEGER PRIMARY KEY AUTOINCREMENT',
            'bai_nome TEXT NOT NULL',
            'fk_cidade INTEGER',
            'FOREIGN KEY(fk_cidade) REFERENCES cidade (pk_cidade)'
        ])

        self.create_table(self.TABLE_CIDADE, [
            'pk_cidade INTEGER PRIMARY KEY AUTOINCREMENT',
            'cid_nome TEXT NOT NULL',
            'fk_estado INTEGER',
            'FOREIGN KEY(fk_estado) REFERENCES estado (pk_estado)'
        ])

        self.create_table(self.TABLE_ESTADO, [
            'pk_estado INTEGER PRIMARY KEY AUTOINCREMENT',
            'est_nome TEXT NOT NULL',
            'est_uf TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_TIPO_IMOVEL, [
            'pk_tipo_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'tim_nome TEXT NOT NULL'
        ])

        self.create_table(self.TABLE_IMOVEL, [
            'pk_imovel INTEGER PRIMARY KEY AUTOINCREMENT',
            'imo_descricao TEXT NOT NULL',
            'imo_caracteristica TEXT NOT NULL',
            'imo_condicoes TEXT NOT NULL',
            'imo_observacoes TEXT NOT NULL',
            'imo_preco REAL NOT NULL',
            'fk_tipo_negociacao INTEGER',
            'fk_status INTEGER',
            'fk_tipo_imovel INTEGER',
            'FOREIGN KEY(fk_tipo_negociacao) REFERENCES tipo_negociacao (pk_tip_negociacao)',
            'FOREIGN KEY(fk_status) REFERENCES status (pk_status)',
            'FOREIGN KEY(fk_tipo_imovel) REFERENCES tipo_imovel (pk_tipo_imovel)'
        ])

        self.create_table(self.TABLE_CLIENTE, [
            'pk_cliente INTEGER PRIMARY KEY AUTOINCREMENT',
            'cli_nome TEXT NOT NULL',
            'fk_endereco INTEGER',
            'FOREIGN KEY(fk_endereco) REFERENCES endereco (pk_endereco)'
        ])

        self.create_table(self.TABLE_RELACAO_IMOVEL_CLIENTE, [
            'pk_relacao_imovel_cliente INTEGER PRIMARY KEY AUTOINCREMENT',
            'fk_tipo_relacao INTEGER',
            'fk_cliente INTEGER',
            'fk_imovel INTEGER',
            'FOREIGN KEY(fk_tipo_relacao) REFERENCES tipo_relacao (pk_tipo_relacao)',
            'FOREIGN KEY(fk_cliente) REFERENCES cliente (pk_cliente)',
            'FOREIGN KEY(fk_imovel) REFERENCES imovel (pk_imovel)'
        ])

        self.create_table(self.TABLE_TIPO_RELACAO, [
            'pk_tipo_relacao INTEGER PRIMARY KEY',
            'tre_nome TEXT NOT NULL'
        ])
        # TABLE_USER = 'usuario'

        self.create_table(self.TABLE_USER, [
            'pk_usuario INTEGER PRIMARY KEY',
            'usu_nome TEXT NOT NULL',
            'usu_senha TEXT NOT NULL'
        ])
    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        values = tuple(data.values())
        self.cursor.execute(query, values)
        self.conn.commit()

    '''
    Essa função permite atualizar dados em uma tabela com base em uma condição. 
    Você precisa passar o nome da tabela, um dicionário com os novos valores, 
    e uma condição que especifica quais registros devem ser atualizados.
    '''
    def update_data(self, table_name, data, condition):
        set_values = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f'UPDATE {table_name} SET {set_values} WHERE {condition}'
        values = tuple(data.values())
        self.cursor.execute(query, values)
        self.conn.commit()

    '''
    Essa função permite excluir registros de uma tabela com base em uma condição.
    '''
    def delete_data(self, table_name, condition):
        query = f'DELETE FROM {table_name} WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()

    '''
    Essa função permite consultar dados de uma tabela. Você pode especificar quais 
    colunas deseja recuperar e aplicar uma condição opcional para filtrar os resultados.
    '''
    def query_data(self, table_name, columns=None, condition=None):
        if columns is None:
            columns = '*'
        query = f'SELECT {columns} FROM {table_name}'
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.conn.close()

    def popular_tabelas_iniciais(self):
        try:
            result_negociacao = (db.query_data('tipo_negociacao'))
            if len(result_negociacao)==0:
                lista_tipos_negociacao = [{'neg_nome': 'Venda'}, {'neg_nome': 'Locacao'}, {'neg_nome': 'Venda/Locação'}]
                for tipo in lista_tipos_negociacao:
                    self.insert_data(self.TABLE_TIPO_NEGOCIACAO, tipo)

            result_user = (db.query_data('usuario'))
            if len(result_user)==0:
                usuario = [{'usu_nome': 'Fernando', 'usu_senha': '123mudar'}]
                for tipo in usuario:
                    self.insert_data(self.TABLE_USER, tipo)

            result_status = (db.query_data('status'))
            if len(result_status)==0:
                lista_tipos_status = [{'sta_nome': 'Disponível'}, {'sta_nome': 'Locado'}, {'sta_nome': 'Vendido'}, {'sta_nome': 'À liberar'}]
                for tipo in lista_tipos_status:
                    self.insert_data(self.TABLE_STATUS, tipo)

            result_status = (db.query_data('tipo_imovel'))
            if len(result_status)==0:
                lista_tipos_imovel = [{'tim_nome': 'Apartamento'}, {'tim_nome': 'Casa'}, {'tim_nome': 'Terreno'}]
                for tipo in lista_tipos_imovel:
                    self.insert_data(self.TABLE_TIPO_IMOVEL, tipo)
            
            result_status = (db.query_data('tipo_relacao'))
            if len(result_status)==0:
                lista_tipos_relacao = [{'tre_nome':'Comprador'},{'tre_nome':'Vendedor'},{'tre_nome':'Locatário'},{'tre_nome':'Locador'},{'tre_nome':'Investidor'},{'tre_nome':'Proprietário'}]
                for tipo in lista_tipos_relacao:
                    self.insert_data(self.TABLE_TIPO_RELACAO, tipo)

            result_status = (db.query_data('estado'))
            if len(result_status)==0:
                lista_estados = [{'est_nome': 'Acre', 'est_uf': 'AC'},{'est_nome': 'Alagoas', 'est_uf': 'AL'},{'est_nome': 'Amapá', 'est_uf': 'AP'},{'est_nome': 'Amazonas', 'est_uf': 'AM'},{'est_nome': 'Bahia', 'est_uf': 'BA'},{'est_nome': 'Ceará', 'est_uf': 'CE'},{'est_nome': 'Distrito Federal', 'est_uf': 'DF'},{'est_nome': 'Espírito Santo', 'est_uf': 'ES'},{'est_nome': 'Goiás', 'est_uf': 'GO'},{'est_nome': 'Maranhão', 'est_uf': 'MA'},{'est_nome': 'Mato Grosso', 'est_uf': 'MT'},{'est_nome': 'Mato Grosso do Sul', 'est_uf': 'MS'},{'est_nome': 'Minas Gerais', 'est_uf': 'MG'},{'est_nome': 'Pará', 'est_uf': 'PA'},{'est_nome': 'Paraíba', 'est_uf': 'PB'},{'est_nome': 'Paraná', 'est_uf': 'PR'},{'est_nome': 'Pernambuco', 'est_uf': 'PE'},{'est_nome': 'Piauí', 'est_uf': 'PI'},{'est_nome': 'Rio de Janeiro', 'est_uf': 'RJ'},{'est_nome': 'Rio Grande do Norte', 'est_uf': 'RN'},{'est_nome': 'Rio Grande do Sul', 'est_uf': 'RS'},{'est_nome': 'Rondônia', 'est_uf': 'RO'},{'est_nome': 'Roraima', 'est_uf': 'RR'},{'est_nome': 'Santa Catarina', 'est_uf': 'SC'},{'est_nome': 'São Paulo', 'est_uf': 'SP'},{'est_nome': 'Sergipe', 'est_uf': 'SE'},{'est_nome': 'Tocantins', 'est_uf': 'TO'}]
                for tipo in lista_estados:
                    self.insert_data(self.TABLE_ESTADO, tipo)

            result_status = (db.query_data('cidade'))
            if len(result_status)==0:
                lista_cidades = [{'cid_nome': 'Rio Branco', 'fk_estado': 1},{'cid_nome': 'Cruzeiro do Sul', 'fk_estado': 1},{'cid_nome': 'Sena Madureira', 'fk_estado': 1},{'cid_nome': 'Tarauacá', 'fk_estado': 1},{'cid_nome': 'Maceió', 'fk_estado': 2},{'cid_nome': 'Arapiraca', 'fk_estado': 2},{'cid_nome': 'Palmeira dos Índios', 'fk_estado': 2},{'cid_nome': 'Penedo', 'fk_estado': 2},{'cid_nome': 'Macapá', 'fk_estado': 3},{'cid_nome': 'Santana', 'fk_estado': 3},{'cid_nome': 'Laranjal do Jari', 'fk_estado': 3},{'cid_nome': 'Oiapoque', 'fk_estado': 3},{'cid_nome': 'Manaus', 'fk_estado': 4},{'cid_nome': 'Itacoatiara', 'fk_estado': 4},{'cid_nome': 'Parintins', 'fk_estado': 4},{'cid_nome': 'Tefé', 'fk_estado': 4},{'cid_nome': 'Salvador', 'fk_estado': 5},{'cid_nome': 'Feira de Santana', 'fk_estado': 5},{'cid_nome': 'Vitória da Conquista', 'fk_estado': 5},{'cid_nome': 'Barreiras', 'fk_estado': 5},{'cid_nome': 'Fortaleza', 'fk_estado': 6},{'cid_nome': 'Caucaia', 'fk_estado': 6},{'cid_nome': 'Juazeiro do Norte', 'fk_estado': 6},{'cid_nome': 'Sobral', 'fk_estado': 6},{'cid_nome': 'Brasília', 'fk_estado': 7},{'cid_nome': 'Vitória', 'fk_estado': 8},{'cid_nome': 'Vila Velha', 'fk_estado': 8},{'cid_nome': 'Cariacica', 'fk_estado': 8},{'cid_nome': 'Serra', 'fk_estado': 8},{'cid_nome': 'Goiânia', 'fk_estado': 9},{'cid_nome': 'Aparecida de Goiânia', 'fk_estado': 9},{'cid_nome': 'Anápolis', 'fk_estado': 9},{'cid_nome': 'Rio Verde', 'fk_estado': 9},{'cid_nome': 'São Luís', 'fk_estado': 10},{'cid_nome': 'Imperatriz', 'fk_estado': 10},{'cid_nome': 'Caxias', 'fk_estado': 10},{'cid_nome': 'Timon', 'fk_estado': 10},{'cid_nome': 'Cuiabá', 'fk_estado': 11},{'cid_nome': 'Várzea Grande', 'fk_estado': 11},{'cid_nome': 'Rondonópolis', 'fk_estado': 11},{'cid_nome': 'Sinop', 'fk_estado': 11},{'cid_nome': 'Campo Grande', 'fk_estado': 12},{'cid_nome': 'Dourados', 'fk_estado': 12},{'cid_nome': 'Três Lagoas', 'fk_estado': 12},{'cid_nome': 'Corumbá', 'fk_estado': 12},{'cid_nome': 'Belo Horizonte', 'fk_estado': 13},{'cid_nome': 'Uberlândia', 'fk_estado': 13},{'cid_nome': 'Contagem', 'fk_estado': 13},{'cid_nome': 'Juiz de Fora', 'fk_estado': 13},{'cid_nome': 'Belém', 'fk_estado': 14},{'cid_nome': 'Ananindeua', 'fk_estado': 14},{'cid_nome': 'Santarém', 'fk_estado': 14},{'cid_nome': 'Marabá', 'fk_estado': 14},{'cid_nome': 'João Pessoa', 'fk_estado': 15},{'cid_nome': 'Campina Grande', 'fk_estado': 15},{'cid_nome': 'Santa Rita', 'fk_estado': 15},{'cid_nome': 'Patos', 'fk_estado': 15},{'cid_nome': 'Curitiba', 'fk_estado': 16},{'cid_nome': 'Londrina', 'fk_estado': 16},{'cid_nome': 'Maringá', 'fk_estado': 16},{'cid_nome': 'Ponta Grossa', 'fk_estado': 16},{'cid_nome': 'Recife', 'fk_estado': 17},{'cid_nome': 'Jaboatão dos Guararapes', 'fk_estado': 17},{'cid_nome': 'Olinda', 'fk_estado': 17},{'cid_nome': 'Caruaru', 'fk_estado': 17},{'cid_nome': 'Teresina', 'fk_estado': 18},{'cid_nome': 'Parnaíba', 'fk_estado': 18},{'cid_nome': 'Picos', 'fk_estado': 18},{'cid_nome': 'Floriano', 'fk_estado': 18},{'cid_nome': 'Rio de Janeiro', 'fk_estado': 19},{'cid_nome': 'São Gonçalo', 'fk_estado': 19},{'cid_nome': 'Duque de Caxias', 'fk_estado': 19},{'cid_nome': 'Nova Iguaçu', 'fk_estado': 19},{'cid_nome': 'Natal', 'fk_estado': 20},{'cid_nome': 'Mossoró', 'fk_estado': 20},{'cid_nome': 'Parnamirim', 'fk_estado': 20},{'cid_nome': 'Caicó', 'fk_estado': 20},{'cid_nome': 'Porto Alegre', 'fk_estado': 21},{'cid_nome': 'Caxias do Sul', 'fk_estado': 21},{'cid_nome': 'Canoas', 'fk_estado': 21},{'cid_nome': 'Pelotas', 'fk_estado': 21},{'cid_nome': 'Porto Velho', 'fk_estado': 22},{'cid_nome': 'Ji-Paraná', 'fk_estado': 22},{'cid_nome': 'Vilhena', 'fk_estado': 22},{'cid_nome': 'Ariquemes', 'fk_estado': 22},{'cid_nome': 'Boa Vista', 'fk_estado': 23},{'cid_nome': 'Rorainópolis', 'fk_estado': 23},{'cid_nome': 'Caracaraí', 'fk_estado': 23},{'cid_nome': 'São João da Baliza', 'fk_estado': 23},{'cid_nome': 'Florianópolis', 'fk_estado': 24},{'cid_nome': 'Joinville', 'fk_estado': 24},{'cid_nome': 'Blumenau', 'fk_estado': 24},{'cid_nome': 'São José', 'fk_estado': 24},{'cid_nome': 'São Paulo', 'fk_estado': 25},{'cid_nome': 'Guarulhos', 'fk_estado': 25},{'cid_nome': 'Campinas', 'fk_estado': 25},{'cid_nome': 'São Bernardo do Campo', 'fk_estado': 25},{'cid_nome': 'Aracaju', 'fk_estado': 26},{'cid_nome': 'Nossa Senhora do Socorro', 'fk_estado': 26},{'cid_nome': 'Lagarto', 'fk_estado': 26},{'cid_nome': 'Itabaiana', 'fk_estado': 26},{'cid_nome': 'Palmas', 'fk_estado': 27},{'cid_nome': 'Araguaína', 'fk_estado': 27},{'cid_nome': 'Gurupi', 'fk_estado': 27},{'cid_nome': 'Porto Nacional', 'fk_estado': 27}]
                for tipo in lista_cidades:
                    self.insert_data(self.TABLE_CIDADE, tipo)

            result_status = (db.query_data('bairro'))
            if len(result_status)==0:
                lista_bairros = [{'bai_nome':'Bairro Verde','fk_cidade':1},{'bai_nome':'Bairro Sol','fk_cidade':1},{'bai_nome':'Bairro Estrela','fk_cidade':2},{'bai_nome':'Bairro Aurora','fk_cidade':2},{'bai_nome':'Bairro Floresta','fk_cidade':3},{'bai_nome':'Bairro Primavera','fk_cidade':3},{'bai_nome':'Bairro Rio Azul','fk_cidade':4},{'bai_nome':'Bairro São João','fk_cidade':4},{'bai_nome':'Bairro Marítimo','fk_cidade':5},{'bai_nome':'Bairro Pajuçara','fk_cidade':5},{'bai_nome':'Bairro Jardim','fk_cidade':6},{'bai_nome':'Bairro Bela Vista','fk_cidade':6},{'bai_nome':'Bairro Centenário','fk_cidade':7},{'bai_nome':'Bairro Novo Horizonte','fk_cidade':7},{'bai_nome':'Bairro Ouro Preto','fk_cidade':8},{'bai_nome':'Bairro Monte Belo','fk_cidade':8},{'bai_nome':'Bairro Santa Clara','fk_cidade':9},{'bai_nome':'Bairro Central','fk_cidade':9},{'bai_nome':'Bairro São Francisco','fk_cidade':10},{'bai_nome':'Bairro Bela Vista','fk_cidade':10},{'bai_nome':'Bairro Rio Branco','fk_cidade':11},{'bai_nome':'Bairro Novo Horizonte','fk_cidade':11},{'bai_nome':'Bairro Pérola','fk_cidade':12},{'bai_nome':'Bairro Tropical','fk_cidade':12},{'bai_nome':'Bairro Cidade Nova','fk_cidade':13},{'bai_nome':'Bairro Parque 10','fk_cidade':13},{'bai_nome':'Bairro Santo Antônio','fk_cidade':14},{'bai_nome':'Bairro Nossa Senhora das Graças','fk_cidade':14},{'bai_nome':'Bairro Amazonas','fk_cidade':15},{'bai_nome':'Bairro Vitória','fk_cidade':15},{'bai_nome':'Bairro Flor de Lis','fk_cidade':16},{'bai_nome':'Bairro São José','fk_cidade':16},{'bai_nome':'Bairro Barra','fk_cidade':17},{'bai_nome':'Bairro Pelourinho','fk_cidade':17},{'bai_nome':'Bairro Cidade Nova','fk_cidade':18},{'bai_nome':'Bairro São João','fk_cidade':18},{'bai_nome':'Bairro Recreio','fk_cidade':19},{'bai_nome':'Bairro Bela Vista','fk_cidade':19},{'bai_nome':'Bairro Cerrado','fk_cidade':20},{'bai_nome':'Bairro Jardim das Acácias','fk_cidade':20},{'bai_nome':'Bairro Praia de Iracema','fk_cidade':21},{'bai_nome':'Bairro Aldeota','fk_cidade':21},{'bai_nome':'Bairro Tabuba','fk_cidade':22},{'bai_nome':'Bairro Planalto Caucaia','fk_cidade':22},{'bai_nome':'Bairro São José','fk_cidade':23},{'bai_nome':'Bairro Triângulo','fk_cidade':23},{'bai_nome':'Bairro Dom Expedito','fk_cidade':24},{'bai_nome':'Bairro Sinhá Sabóia','fk_cidade':24},{'bai_nome':'Bairro Asa Sul','fk_cidade':25},{'bai_nome':'Bairro Lago Sul','fk_cidade':25},{'bai_nome':'Bairro Jardim Camburi','fk_cidade':26},{'bai_nome':'Bairro Mata da Praia','fk_cidade':26},{'bai_nome':'Bairro Itapoã','fk_cidade':27},{'bai_nome':'Bairro Praia da Costa','fk_cidade':27},{'bai_nome':'Bairro Campo Grande','fk_cidade':28},{'bai_nome':'Bairro Jardim América','fk_cidade':28},{'bai_nome':'Bairro Jacaraípe','fk_cidade':29},{'bai_nome':'Bairro Parque Residencial Laranjeiras','fk_cidade':29},{'bai_nome':'Bairro Setor Bueno','fk_cidade':30},{'bai_nome':'Bairro Jardim Goiás','fk_cidade':30},{'bai_nome':'Bairro Garavelo','fk_cidade':31},{'bai_nome':'Bairro Buriti Sereno','fk_cidade':31},{'bai_nome':'Bairro Jundiaí','fk_cidade':32},{'bai_nome':'Bairro Vila Jaiara','fk_cidade':32},{'bai_nome':'Bairro Popular','fk_cidade':33},{'bai_nome':'Bairro Promissão','fk_cidade':33},{'bai_nome':'Bairro Renascença','fk_cidade':34},{'bai_nome':'Bairro Cohab Anil','fk_cidade':34},{'bai_nome':'Bairro Santa Rita','fk_cidade':35},{'bai_nome':'Bairro Jardim São Luís','fk_cidade':35},{'bai_nome':'Bairro Nova Caxias','fk_cidade':36},{'bai_nome':'Bairro Volta Redonda','fk_cidade':36},{'bai_nome':'Bairro São Benedito','fk_cidade':37},{'bai_nome':'Bairro Parque Alvorada','fk_cidade':37},{'bai_nome':'Bairro Centro Sul','fk_cidade':38},{'bai_nome':'Bairro Quilombo','fk_cidade':38},{'bai_nome':'Bairro Cristo Rei','fk_cidade':39},{'bai_nome':'Bairro Jardim Glória','fk_cidade':39},{'bai_nome':'Bairro Vila Operária','fk_cidade':40},{'bai_nome':'Bairro Jardim Itapuã','fk_cidade':40},{'bai_nome':'Bairro Jardim das Oliveiras','fk_cidade':41},{'bai_nome':'Bairro Jardim Maringá','fk_cidade':41},{'bai_nome':'Bairro Jardim dos Estados','fk_cidade':42},{'bai_nome':'Bairro Tiradentes','fk_cidade':42},{'bai_nome':'Bairro Parque Alvorada','fk_cidade':43},{'bai_nome':'Bairro Jardim Água Boa','fk_cidade':43},{'bai_nome':'Bairro Santa Terezinha','fk_cidade':44},{'bai_nome':'Bairro Jardim Primaveril','fk_cidade':44},{'bai_nome':'Bairro Centro América','fk_cidade':45},{'bai_nome':'Bairro Popular Nova','fk_cidade':45},{'bai_nome':'Bairro Savassi','fk_cidade':46},{'bai_nome':'Bairro Santa Tereza','fk_cidade':46},{'bai_nome':'Bairro Santa Mônica','fk_cidade':47},{'bai_nome':'Bairro Martins','fk_cidade':47},{'bai_nome':'Bairro Eldorado','fk_cidade':48},{'bai_nome':'Bairro Industrial','fk_cidade':48},{'bai_nome':'Bairro São Mateus','fk_cidade':49},{'bai_nome':'Bairro Manoel Honório','fk_cidade':49},{'bai_nome':'Bairro Nazaré','fk_cidade':50},{'bai_nome':'Bairro Umarizal','fk_cidade':50},{'bai_nome':'Bairro Cidade Nova','fk_cidade':51},{'bai_nome':'Bairro Águas Brancas','fk_cidade':51},{'bai_nome':'Bairro Santarenzinho','fk_cidade':52},{'bai_nome':'Bairro Aldeia','fk_cidade':52},{'bai_nome':'Bairro Cidade Nova','fk_cidade':53},{'bai_nome':'Bairro Morada Nova','fk_cidade':53},{'bai_nome':'Bairro Tambaú','fk_cidade':54},{'bai_nome':'Bairro Manaíra','fk_cidade':54},{'bai_nome':'Bairro Catolé','fk_cidade':55},{'bai_nome':'Bairro José Pinheiro','fk_cidade':55},{'bai_nome':'Bairro Municípios','fk_cidade':56},{'bai_nome':'Bairro Tibiri','fk_cidade':56},{'bai_nome':'Bairro Belo Horizonte','fk_cidade':57},{'bai_nome':'Bairro São Sebastião','fk_cidade':57},{'bai_nome':'Bairro Batel','fk_cidade':58},{'bai_nome':'Bairro Centro Cívico','fk_cidade':58},{'bai_nome':'Bairro Gleba Palhano','fk_cidade':59},{'bai_nome':'Bairro Universitário','fk_cidade':59},{'bai_nome':'Bairro Zona 7','fk_cidade':60},{'bai_nome':'Bairro Vila Nova','fk_cidade':60},{'bai_nome':'Bairro Nova Rússia','fk_cidade':61},{'bai_nome':'Bairro Contorno','fk_cidade':61},{'bai_nome':'Bairro Boa Viagem','fk_cidade':62},{'bai_nome':'Bairro Casa Amarela','fk_cidade':62},{'bai_nome':'Bairro Candeias','fk_cidade':63},{'bai_nome':'Bairro Piedade','fk_cidade':63},{'bai_nome':'Bairro Bairro Novo','fk_cidade':64},{'bai_nome':'Bairro Jardim Atlântico','fk_cidade':64},{'bai_nome':'Bairro Indianópolis','fk_cidade':65},{'bai_nome':'Bairro Salgado','fk_cidade':65},{'bai_nome':'Bairro Centro','fk_cidade':66},{'bai_nome':'Bairro Horto','fk_cidade':66},{'bai_nome':'Bairro Boa Esperança','fk_cidade':67},{'bai_nome':'Bairro São Vicente de Paula','fk_cidade':67},{'bai_nome':'Bairro Parque de Exposições','fk_cidade':68},{'bai_nome':'Bairro Boa Sorte','fk_cidade':68},{'bai_nome':'Bairro Tiberão','fk_cidade':69},{'bai_nome':'Bairro Irapuá','fk_cidade':69},{'bai_nome':'Bairro Copacabana','fk_cidade':70},{'bai_nome':'Bairro Laranjeiras','fk_cidade':70},{'bai_nome':'Bairro Mutondo','fk_cidade':71},{'bai_nome':'Bairro Boaçu','fk_cidade':71},{'bai_nome':'Bairro Jardim Primavera','fk_cidade':72},{'bai_nome':'Bairro Parque Lafaiete','fk_cidade':72},{'bai_nome':'Bairro Comendador Soares','fk_cidade':73},{'bai_nome':'Bairro Miguel Couto','fk_cidade':73},{'bai_nome':'Bairro Tirol','fk_cidade':74},{'bai_nome':'Bairro Petrópolis','fk_cidade':74},{'bai_nome':'Bairro Alto de São Manoel','fk_cidade':75},{'bai_nome':'Bairro Abolição','fk_cidade':75},{'bai_nome':'Bairro Emaús','fk_cidade':76},{'bai_nome':'Bairro Rosa dos Ventos','fk_cidade':76},{'bai_nome':'Bairro Boa Passagem','fk_cidade':77},{'bai_nome':'Bairro Castelo Branco','fk_cidade':77},{'bai_nome':'Bairro Moinhos de Vento','fk_cidade':78},{'bai_nome':'Bairro Bela Vista','fk_cidade':78},{'bai_nome':'Bairro São Pelegrino','fk_cidade':79},{'bai_nome':'Bairro Panazzolo','fk_cidade':79},{'bai_nome':'Bairro Estância Velha','fk_cidade':80},{'bai_nome':'Bairro Mathias Velho','fk_cidade':80},{'bai_nome':'Bairro Fragata','fk_cidade':81},{'bai_nome':'Bairro Centro','fk_cidade':81},{'bai_nome':'Bairro Olaria','fk_cidade':82},{'bai_nome':'Bairro Agenor de Carvalho','fk_cidade':82},{'bai_nome':'Bairro Urupá','fk_cidade':83},{'bai_nome':'Bairro Jardim dos Migrantes','fk_cidade':83},{'bai_nome':'Bairro Jardim Eldorado','fk_cidade':84},{'bai_nome':'Bairro Alto Alegre','fk_cidade':84},{'bai_nome':'Bairro Setor 3','fk_cidade':85},{'bai_nome':'Bairro Centro','fk_cidade':85},{'bai_nome':'Bairro São Francisco','fk_cidade':86},{'bai_nome':'Bairro Paraviana','fk_cidade':86},{'bai_nome':'Bairro Centro','fk_cidade':87},{'bai_nome':'Bairro Jardim das Flores','fk_cidade':87},{'bai_nome':'Bairro Centro','fk_cidade':88},{'bai_nome':'Bairro Jardim Floresta','fk_cidade':88},{'bai_nome':'Bairro Centro','fk_cidade':89},{'bai_nome':'Bairro Novo Horizonte','fk_cidade':89},{'bai_nome':'Bairro Trindade','fk_cidade':90},{'bai_nome':'Bairro Coqueiros','fk_cidade':90},{'bai_nome':'Bairro Boa Vista','fk_cidade':91},{'bai_nome':'Bairro Iririú','fk_cidade':91},{'bai_nome':'Bairro Velha','fk_cidade':92},{'bai_nome':'Bairro Garcia','fk_cidade':92},{'bai_nome':'Bairro Forquilhas','fk_cidade':93},{'bai_nome':'Bairro Campinas','fk_cidade':93},{'bai_nome':'Bairro Jardim Paulista','fk_cidade':94},{'bai_nome':'Bairro Moema','fk_cidade':94},{'bai_nome':'Bairro Vila Augusta','fk_cidade':95},{'bai_nome':'Bairro Parque Renato Maia','fk_cidade':95},{'bai_nome':'Bairro Cambuí','fk_cidade':96},{'bai_nome':'Bairro Taquaral','fk_cidade':96},{'bai_nome':'Bairro Centro','fk_cidade':97},{'bai_nome':'Bairro Rudge Ramos','fk_cidade':97},{'bai_nome':'Bairro Atalaia','fk_cidade':98},{'bai_nome':'Bairro 13 de Julho','fk_cidade':98},{'bai_nome':'Bairro Taiçoca','fk_cidade':99},{'bai_nome':'Bairro Parque dos Faróis','fk_cidade':99},{'bai_nome':'Bairro Centro','fk_cidade':100},{'bai_nome':'Bairro Jardim Campo Novo','fk_cidade':100},{'bai_nome':'Bairro Campo Grande','fk_cidade':101},{'bai_nome':'Bairro Moita Formosa','fk_cidade':101},{'bai_nome':'Bairro Plano Diretor Sul','fk_cidade':102},{'bai_nome':'Bairro Taquaralto','fk_cidade':102},{'bai_nome':'Bairro Setor Central','fk_cidade':103},{'bai_nome':'Bairro Jardim das Flores','fk_cidade':103},{'bai_nome':'Bairro Alto da Boa Vista','fk_cidade':104},{'bai_nome':'Bairro Parque das Acácias','fk_cidade':104},{'bai_nome':'Bairro Centro','fk_cidade':105},{'bai_nome':'Bairro Jardim Girassol','fk_cidade':105}]
                for tipo in lista_bairros:
                    self.insert_data(self.TABLE_BAIRRO, tipo)

        except Exception as e:
            print(e)

db=Database()
db.create_tables()
db.popular_tabelas_iniciais()





