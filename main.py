from Data_base import Database


def inserir():
    pass


db = Database()

dicts_insert_data={
    'tipo_negociacao':{'neg_nome':'TEXT'},
    'status':{'sta_nome':'TEXT'},
    'endereco':{'end_logradouro':'TEXT','end_numero':'TEXT','end_cep':'TEXT','end_complemento':'TEXT','fk_bairro':'INTEGER'},
    'bairro':{'bai_nome':'TEXT','fk_cidade':'INTEGER'},
    'cidade':{'cid_nome':'TEXT','fk_estado':'INTEGER'},
    'estado':{'est_nome':'TEXT','est_uf':'TEXT'},
    'tipo_imovel':{'tim_nome':'TEXT'},
    'imovel':{'imo_descricao':'TEXT','imo_caracteristica':'TEXT','imo_condicoes':'TEXT','imo_observacoes':'TEXT','imo_preco':'REAL','fk_tipo_negociacao':'INTEGER','fk_status':'INTEGER','fk_tipo_imovel':'INTEGER'},
    'cliente':{'cli_nome':'TEXT','fk_endereco':'INTEGER'},
    'relacao_imovel_cliente':{'fk_tipo_relacao':'INTEGER','fk_cliente':'INTEGER','fk_imovel':'INTEGER'},
    'tipo_relacao':{'tre_nome':'TEXT'}
}

table_name = 'tipo_negociacao'
results = db.query_data(table_name)
print(len(results), 'tipo_negociacao', results)

table_name = 'status'
results = db.query_data(table_name)
print(len(results), 'status', results)

table_name = 'endereco'
results = db.query_data(table_name)
print(len(results), 'endereco', results)

table_name = 'bairro'
results = db.query_data(table_name)
print(len(results), 'bairro', results)

table_name = 'cidade'
results = db.query_data(table_name)
print(len(results), 'cidade', results)
# for cidade in results:
#     print(cidade)

table_name = 'estado'
results = db.query_data(table_name)
print(len(results), 'estado', results)
# for estado in results:
#     print (estado)

table_name = 'tipo_imovel'
results = db.query_data(table_name)
print(len(results), 'tipo_imovel', results)

table_name = 'imovel'
results = db.query_data(table_name)
print(len(results), 'imovel', results)

table_name = 'cliente'
results = db.query_data(table_name)
print(len(results), 'cliente', results)

table_name = 'relacao_imovel_cliente'
results = db.query_data(table_name)
print(len(results), 'relacao_imovel_cliente', results)

table_name = 'tipo_relacao'
results = db.query_data(table_name)
print(len(results), 'tipo_relacao', results)

table_name = 'bairro'
results = db.query_data(table_name)
print(len(results), 'bairro', results)

table_name = 'usuario'
results = db.query_data(table_name)
print(len(results), 'usuario', results)