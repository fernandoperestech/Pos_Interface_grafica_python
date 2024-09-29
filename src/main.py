from data_base import Database
import data_base as data
from interface import iniciar_interface

# Inicia o banco de dados e cria as tabelas
db = Database()
db.create_tables()

# Popula as tabelas com dados iniciais
db.popular_tabelas_iniciais()

# Inicia a interface gráfica
iniciar_interface(db)

# Fecha a conexão com o banco de dados ao finalizar
db.close()
