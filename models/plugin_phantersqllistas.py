# -*- coding: utf-8 -*-
import plugin_phantersqllistas.phantersqllistas
import em_reais
reload(plugin_phantersqllistas.phantersqllistas)
from plugin_phantersqllistas.phantersqllistas import PhanterSqlListas

MODELS_PHANTERSQLLISTAS=PhanterSqlListas(db, db.produtos, searchfield="produto", fields=[['cod_barra','col-4'],['produto','col-4'],['descricao','col-4']])
MODELS_PHANTERSQLLISTAS.addMenuItem(lambda row: A("Editar", _href=URL("servicos", "produtos", args=['editar', row.id]), _class="link_dropdown dropdown-item"))


MODELS_PHANTERSQLLISTAS_FORNECEDORES=PhanterSqlListas(db, db.fornecedores, searchfield="fantasia", fields=[['cnpj','col-4'],['fantasia','col-4'],['nome','col-4']])
MODELS_PHANTERSQLLISTAS_FORNECEDORES.addMenuItem(lambda row: A("Editar", _href=URL("servicos", "fornecedores", args=['editar', row.id]), _class="link_dropdown dropdown-item"))
MODELS_PHANTERSQLLISTAS_FORNECEDORES.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_fornecedores'))

MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES=PhanterSqlListas(db, db.fornecedores, searchfield="fantasia", fields=[['cnpj','col-4'],['fantasia','col-4'],['nome','col-4']])
MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.personalizarLinha(lambda row: A(DIV(row['cnpj'], _class="tfield col-4"), DIV(row['fantasia'], _class="tfield col-4"), DIV(row['nome'], _class="tfield col-4"), _href=URL("servicos", "estoque", args=["lancar", row.id]), _class="row linha_escolha"))
MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_estoque_fornecedores'))

MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS=PhanterSqlListas(db, db.produtos, searchfield="produto", fields=[['cod_barra','col-4'],['produto','col-4'],['descricao','col-4']])
MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.personalizarLinha(lambda row: A(DIV(row['cod_barra'], _class="tfield col-4"), DIV(row['produto'], _class="tfield col-4"), DIV(row['descricao'], _class="tfield col-4"), _href=URL("servicos", "estoque", args=["lancar", request.args(1), row.id]), _class="row linha_escolha"))
MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_estoque_produtos'))

MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL=PhanterSqlListas(db, db.produtos, searchfield="produto", query=(db.produtos.quantidade>0),fields=[['cod_barra','col-2'],['produto','col-4'],['quantidade','col-2'],['unidades', 'col-2'],['preco_final','col-2']])
MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_estoque_disponivel'))
meu_lambda=lambda field: field.unidade
MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.personalizarCampo({'unidades':meu_lambda})

MODELS_PHANTERSQLLISTAS_CLIENTES=PhanterSqlListas(db, db.clientes, searchfield="nome", fields=[['nome','col-6'],['cpf','col-3'],['email','col-3']])
MODELS_PHANTERSQLLISTAS_CLIENTES.addMenuItem(lambda row: A("Editar", _href=URL("servicos", "clientes", args=['editar', row.id]), _class="link_dropdown dropdown-item"))
MODELS_PHANTERSQLLISTAS_CLIENTES.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_clientes'))

MODELS_PHANTERSQLLISTAS_FUNCIONARIOS=PhanterSqlListas(db, db.funcionarios, searchfield="nome", fields=[['nome','col-6'],['cpf','col-3'],['cargo','col-3']])
MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.addMenuItem(lambda row: A("Editar", _href=URL("servicos", "funcionarios", args=['editar', row.id]), _class="link_dropdown dropdown-item"))
MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_funcionarios'))

MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES=PhanterSqlListas(db, db.clientes, searchfield="nome", fields=[['nome','col-6'],['cpf','col-3'],['email','col-3']])
MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.personalizarLinha(lambda row: A(DIV(row['nome'], _class="tfield col-6"), DIV(row['cpf'], _class="tfield col-3"), DIV(row['email'], _class="tfield col-3"), _href=URL("servicos", "pdv", args=["cliente", row.id]), _class="row linha_escolha"))
MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_caixa_clientes'))

MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS=PhanterSqlListas(db, db.produtos, searchfield="produto", fields=[['cod_barra','col-3'],['produto','col-3'],['descricao','col-3'],['preco_final','col-3']])
MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.personalizarLinha(lambda row: A(DIV(row['cod_barra'], _class="tfield col-3"), DIV(row['produto'], _class="tfield col-3"), DIV(row['descricao'], _class="tfield col-3"), DIV(em_reais.em_reais(row['preco_final']), _class="tfield col-3"), _href="#", _class="row linha_escolha", _onclick="adc_cod_barra(\"%s\", \"%s\")" %(row['cod_barra'], URL('default', 'download', args=[db.produtos[row['id']].id_imagem.imagem]))))
MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.urlAJAX(URL('plugin_phantersqllistas', 'echo_phantersqllistas_pdv_produtos'))