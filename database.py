import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('imoveis.db')
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS imoveis
                  (id INTEGER PRIMARY KEY,
                  tipo_negociacao TEXT,
                  status TEXT,
                  endereco TEXT,
                  descricao_curta TEXT,
                  tipo_imovel TEXT,
                  caracteristicas TEXT,
                  preco REAL,
                  condicoes TEXT,
                  observacoes TEXT)
                  ''')
        self.conn.commit()

    def inserir_imovel(self, tipo_negociacao, status, endereco, descricao_curta, tipo_imovel, caracteristicas, preco, condicoes, observacoes):
        c = self.conn.cursor()
        c.execute('''
                  INSERT INTO imoveis (tipo_negociacao, status, endereco, descricao_curta, tipo_imovel, caracteristicas, preco, condicoes, observacoes)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (tipo_negociacao, status, endereco, descricao_curta, tipo_imovel, caracteristicas, preco, condicoes, observacoes))
        self.conn.commit()

    def obter_imoveis(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM imoveis')
        return c.fetchall()

    def obter_imovel_por_id(self, imovel_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM imoveis WHERE id = ?', (imovel_id,))
        return c.fetchone()

    def atualizar_imovel(self, imovel_id, tipo_negociacao, status, endereco, descricao_curta, tipo_imovel, caracteristicas, preco, condicoes, observacoes):
        c = self.conn.cursor()
        c.execute('''
                  UPDATE imoveis
                  SET tipo_negociacao = ?, status = ?, endereco = ?, descricao_curta = ?, tipo_imovel = ?, caracteristicas = ?, preco = ?, condicoes = ?, observacoes = ?
                  WHERE id = ?''',
                  (tipo_negociacao, status, endereco, descricao_curta, tipo_imovel, caracteristicas, preco, condicoes, observacoes, imovel_id))
        self.conn.commit()
