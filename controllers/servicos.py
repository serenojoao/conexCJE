# -*- coding: utf-8 -*-

def index():
    html=""
    titulo="SERVIÇOS ConexCJE"
    subtitulo="O que deseja fazer?"
    html_comandos=DIV(
        A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('default', 'index'), _title="voltar"),
        _class="comandos_main_container")
    html=DIV(
            DIV(
                DIV(
                    A(
                        DIV(
                            ICONE_FORNECEDORES, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'fornecedores'), _title="fornecedores"),
                    _class="col-4"),
                DIV(
                    A(
                        DIV(
                            ICONE_PRODUTOS, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'produtos'), _title="produtos"),
                    _class="col-4"),
                DIV(
                    A(
                        DIV(
                            ICONE_PDV, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'caixa'), _title="caixa"),
                    _class="col-4"), 
                _class="row"),
            DIV(
                DIV(
                    A(
                        DIV(
                            ICONE_ESTOQUE, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'estoque'), _title="Estoque"),
                    _class="col-4"),
                DIV(
                    A(
                        DIV(
                            ICONE_CLIENTES, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'clientes'), _title="Clientes"),
                    _class="col-4"),
                DIV(
                    A(
                        DIV(
                            ICONE_FUNCIONARIOS, 
                            _class="svg_botoes"), 
                        _href=URL('servicos', 'funcionarios'), _title="Funcionarios"),
                    _class="col-4"),
                 _class="row"),
            # DIV(
            #     DIV(
            #         A(
            #             DIV(
            #                 ICONE_CONFIGURACOES, 
            #                 _class="svg_botoes"), 
            #             _href=URL('configuracoes', 'index')),
            #         _class="col-4"),
            #     _class="row"),
            _class="container")
    return locals()

def fornecedores():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'fornecedores'), _title="voltar"),
            
            _class="comandos_main_container")
        if request.args(0)=="editar" and request.args(1):
            html_comandos.append(A(DIV(ICONE_NOVO_FORNECEDOR, _class="botao_menu_pagina"), _href=URL('servicos', 'fornecedores', args=['novo']), _title="Novo fornecedor"))
            titulo="Editar fornecedor"
            subtitulo="Edite os dados do fornecedor."
            form=SQLFORM(db.fornecedores, request.args(1))
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Fornecedor alterado"
        elif request.args(0)=="novo":
            titulo="Novo fornecedor"
            subtitulo="Adicione um novo fornecedor."
            form=SQLFORM(db.fornecedores)
            html=DIV(DIV("Digitando um CNPJ válido ele irá automaticamente pegar os dados da Receita Federal",_class='avisos'),form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Fornecedor Adicionado"
        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.fornecedores.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "fornecedor não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Lista de fornecedores"
        subtitulo="Adicione, edite, crie fornecedores."
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            A(DIV(ICONE_NOVO_FORNECEDOR, _class="botao_menu_pagina"), _href=URL('servicos', 'fornecedores', args=['novo']), _title="Novo fornecedor"),
            _class="comandos_main_container")
        html=MODELS_PHANTERSQLLISTAS_FORNECEDORES
    return locals()

def produtos():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'produtos'), _title="voltar"),
            
            _class="comandos_main_container")
        if request.args(0)=="editar" and request.args(1):
            html_comandos.append(A(DIV(ICONE_NOVO_PRODUTO, _class="botao_menu_pagina"), _href=URL('servicos', 'produtos', args=['novo']), _title="Novo produto"))
            titulo="Editar produto"
            subtitulo="Edite os dados do produto."
            form=SQLFORM(db.produtos, request.args(1), fields=["id_imagem","cod_barra", "produto","descricao"])
            html=DIV(form, _class='container_formulario')
            if form.process().accepted:
                response.flash="Produto alterado"
        elif request.args(0)=="novo":
            titulo="Novo produto"
            subtitulo="Adicione um novo produto."
            form=SQLFORM(db.produtos, fields=["id_imagem","cod_barra", "produto","descricao"])
            html=DIV(form, _class='container_formulario')
            if form.process().accepted:
                response.flash="Produto Adicionado"
        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "produto não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Lista de produtos"
        subtitulo="Adicione, edite, crie produtos."
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            A(DIV(ICONE_NOVO_PRODUTO, _class="botao_menu_pagina"), _href=URL('servicos', 'produtos', args=['novo']), _title="Novo produto"),
            _class="comandos_main_container")
                
        html=MODELS_PHANTERSQLLISTAS
    return locals()

def estoque():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque'), _title="voltar"),
            _class="comandos_main_container")
        if request.args(0)=="lancar" and not request.args(1):
            html_comandos.append(A(DIV(ICONE_LANCAR_EM_ESTOQUE, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque', args=['lancar']), _title="Lanças em estoque"))
            titulo="Escolha um fornecedor"
            subtitulo="Escolha o fornecedor responsável pelo produto a ser lançado no estoque."
            html=MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES

        elif request.args(0)=="lancar" and request.args(1) and not request.args(2):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque', args=["lancar"]), _title="voltar"),
                _class="comandos_main_container")
            titulo="Escolha um produto"
            subtitulo="Escolha o produto fornecido pelo fornecedor para ser lançado no estoque."
            q_fornecedor=db(db.fornecedores.id==request.args(1)).select().first()
            html_fornecedor_dados=DIV(DIV(
                DIV(DIV(H4("FORNECEDOR DO PRODUTO", _class='titulo_card'),_class="col-12"),
                    DIV(q_fornecedor.cnpj,_class="col-4"),
                    DIV(q_fornecedor.fantasia,_class="col-4"),
                    DIV(q_fornecedor.nome,_class="col-4"),
                    _class='row'),
                _class='card_dados'), _class='padding_20')
            html=CAT(html_fornecedor_dados, MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS)
        elif request.args(0)=="lancar" and request.args(1) and request.args(2):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque', args=["lancar"]), _title="voltar"),
                _class="comandos_main_container")
            titulo="Escolha um produto"
            subtitulo="Escolha o produto fornecido pelo fornecedor para ser lançado no estoque."
            q_fornecedor=db(db.fornecedores.id==request.args(1)).select().first()
            html_fornecedor_dados=DIV(DIV(
                DIV(DIV(H4("FORNECEDOR DO PRODUTO", _class='titulo_card'),_class="col-12"),
                    DIV(q_fornecedor.cnpj,_class="col-4"),
                    DIV(q_fornecedor.fantasia,_class="col-4"),
                    DIV(q_fornecedor.nome,_class="col-4"),
                    _class='row'),
                _class='card_dados'), _class='padding_20')
            q_produto=db(db.produtos.id==request.args(2)).select().first()
            html_produto_dados=DIV(DIV(
                DIV(DIV(H4("PRODUTO ESCOLHIDO", _class='titulo_card'),_class="col-12"),
                    DIV(q_produto.cod_barra,_class="col-4"),
                    DIV(q_produto.produto,_class="col-4"),
                    DIV(q_produto.descricao,_class="col-4"),
                    _class='row'),
                _class='card_dados'), _class='padding_20')
            db.fornecedores_produtos.fornecedores.default=request.args(1)
            db.fornecedores_produtos.produtos.default=request.args(2)
            quant_vendida=0.0
            valor_tem_atualmente=0.0
            valor_preco_custo_medio=0.0
            valor_preco_custo_max=0.0
            valor_preco_custo_min=0.0
            valor_preco_sugerido=0.0
            valor_quantidade_total=0.0
            q_vendas=db(db.produto_vendas.produtos==request.args(2)).select()
            q_lancado=db(db.fornecedores_produtos.produtos==request.args(2)).select(db.fornecedores_produtos.quantidade, db.fornecedores_produtos.preco_custo)
            if q_vendas:
                quant_vendida=sum([x.quantidade for x in q_vendas])

            if q_lancado:
                temp_prod=sum([x.quantidade for x in q_lancado])
                valor_tem_atualmente=temp_prod-quant_vendida
                valor_quantidade_total=valor_tem_atualmente

                precos_custo=[x.preco_custo for x in q_lancado]
                temp_prec=sum(precos_custo)
                quant_preco_custo=len(precos_custo)
                valor_preco_custo_medio=temp_prec/quant_preco_custo
                valor_preco_custo_min=min(precos_custo)
                valor_preco_custo_max=max(precos_custo)
                valor_preco_sugerido=valor_preco_custo_medio+(valor_preco_custo_medio*MODELS_PORCENTAGEM_DE_LUCRO)

            valor_preco_atual=0.0
            valor_preco_manual=0.0
            dicionario_set={x.id: x.unidade for x in db(db.unidades).select()}
            dicionario_set["Nova Unidade"]="Nova Unidade"
            new_field=[db.fornecedores_produtos[x] for x in db.fornecedores_produtos.fields]+[
            Field('quantidade_total', 'double', default=valor_quantidade_total, label="Quantidade Total"),
            Field('unidade', 'string', default=1, label="Unidade", requires=IS_IN_SET(dicionario_set)),
            Field('nova_unidade', 'string', label="Nova Unidade"),
            Field('preco_manual', 'double', label="Preço Final", default=0.0, requires=[IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0.0000000001, None, dot=".", error_message='O Preço Final não pode ser ZERO')])
            ]

            form=SQLFORM.factory( *new_field,
                fields=['quantidade','preco_custo','quantidade_total','preco_manual', 'unidade', 'nova_unidade'])
            if form.process().accepted:
                print form.vars
                print form.vars.quantidade_total
                if request.vars.unidade=="Nova Unidade":
                    minha_unidade=request.vars.nova_unidade
                else:
                    minha_unidade=request.vars.unidade
                q_unidades=db(db.unidades.unidade==minha_unidade).select().first()
                if q_unidades:
                    id_unidade=q_unidades.id
                else:
                    id_unidade=db.unidades.insert(unidade=minha_unidade)
                id_fornecedores_produtos=db.fornecedores_produtos.insert(quantidade=form.vars.quantidade, preco_custo=form.vars.preco_custo,fornecedores=int(request.args(1)),produtos=int(request.args(2)))
                q_produtos=db(db.produtos.id==request.args(2)).select().first()
                id_produto=q_produtos.update_record(quantidade=float(form.vars.quantidade_total), unidades=id_unidade, preco_final=form.vars.preco_manual)

                if id_fornecedores_produtos and id_produto:
                    db.commit()
                    response.flash="Adicionado"
                else:
                    response.flash="Houve algum erro"
                    db.rollback()


            html=CAT(html_fornecedor_dados, html_produto_dados)            

        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "produto não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Lista de produtos em estoque"
        subtitulo="Adicione, edite, crie produtos."
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            A(DIV(ICONE_LANCAR_EM_ESTOQUE, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque', args=['lancar']), _title="Lançar em estoque"),
            _class="comandos_main_container")
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL
    return locals()

def clientes():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'clientes'), _title="voltar"),
            _class="comandos_main_container")
        if request.args(0)=="editar" and request.args(1):
            html_comandos.append(A(DIV(ICONE_NOVO_CLIENTE, _class="botao_menu_pagina"), _href=URL('servicos', 'cliente', args=['novo']), _title="Novo cliente"))
            titulo="Editar Cliente"
            subtitulo="Edite os dados do cliente."
            form=SQLFORM(db.clientes, request.args(1), fields=["nome", "cpf", "telefone_residencial", "telefone_celular", "email"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Cliente alterado"
        elif request.args(0)=="novo":
            titulo="Novo Cliente"
            subtitulo="Adicione um novo cliente."
            form=SQLFORM(db.clientes, fields=["nome", "cpf", "telefone_residencial", "telefone_celular", "email"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Cliente Adicionado"
        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "cliente não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Lista de clientes"
        subtitulo="Adicione, edite, crie produtos."
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            A(DIV(ICONE_NOVO_CLIENTE, _class="botao_menu_pagina"), _href=URL('servicos', 'clientes', args=['novo']), _title="Novo cliente"),
            _class="comandos_main_container")
                
        html=MODELS_PHANTERSQLLISTAS_CLIENTES
    return locals()

def funcionarios():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'funcionarios'), _title="voltar"),
            _class="comandos_main_container")
        if request.args(0)=="editar" and request.args(1):
            html_comandos.append(A(DIV(ICONE_NOVO_FUNCIONARIO, _class="botao_menu_pagina"), _href=URL('servicos', 'funcionario', args=['novo']), _title="Novo funcionário"))
            titulo="Editar Funcionário"
            subtitulo="Edite os dados do funcionário."
            form=SQLFORM(db.funcionarios, request.args(1), fields=["nome", "cpf", "telefone_residencial", "telefone_celular", "email","salario" ,"cargo" ,"conta"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Funcionário alterado"
        elif request.args(0)=="novo":
            titulo="Novo Funcionário"
            subtitulo="Adicione um novo funcionário."
            form=SQLFORM(db.funcionarios, fields=["nome", "cpf", "telefone_residencial", "telefone_celular", "email","salario" ,"cargo" ,"conta"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Funcionário Adicionado"
        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "funcionário não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Lista de funcionarios"
        subtitulo="Adicione, edite, crie produtos."
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            A(DIV(ICONE_NOVO_FUNCIONARIO, _class="botao_menu_pagina"), _href=URL('servicos', 'funcionarios', args=['novo']), _title="Novo cliente"),
            _class="comandos_main_container")
                
        html=MODELS_PHANTERSQLLISTAS_FUNCIONARIOS
    return locals()

def caixa():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque'), _title="voltar"),
            _class="comandos_main_container")
        if request.args(0)=="vender" and request.args(1)=="pdv" and not request.args(2):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa'), _title="voltar"),
                _class="comandos_main_container")
            html=DIV("Sem conexao com a rede...")
        elif request.args(0)=="vender" and request.args(1)=="cliente" and not request.args(2):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa'), _title="voltar"),
                _class="comandos_main_container")
            titulo="Escolha um cliente"
            subtitulo="Escolha o cliente que quer comprar."
            html=CAT(MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES)

        elif request.args(0)=="vender" and request.args(1) and request.args(2):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa', args=["vender", "cliente"]), _title="voltar"),
                _class="comandos_main_container")
            titulo="Vender"
            subtitulo="Efetue a venda"
            q_cliente=db(db.fornecedores.id==request.args(1)).select().first()
            html_cliente_dados=DIV(DIV(
                DIV(DIV(H4("", _class='titulo_card'),_class="col-12"),
                    DIV(q_cliente.nome,_class="col-6"),
                    DIV(q_cliente.cpf,_class="col-3"),
                    DIV(q_cliente.email,_class="col-3"),
                    _class='row'),
                _class='card_dados'), _class='padding_20')

            html=CAT(html_cliente_dados, DIV("Criando..."))      

        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "produto não encontrado"
        else:
            return "falta parâmetros"
    else:
        titulo="Tipo de venda"
        subtitulo="Escolha se é venda a cliente vip ou cliente casual (Sem registro)"
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            _class="comandos_main_container")
        html=DIV(
                DIV(
                    DIV(A(DIV(DIV("Cliente Indentificado",_class='titulo_informativo'), DIV(ICONE_CLIENTES,_class="icone_tipo_venda"), _class="titulo_e_icone"), _href=URL('servicos', "caixa",args=['vender', 'cliente'] ), _class="link_sem_decorator"), _class="col-6"),
                    DIV(A(DIV(DIV("Venda avulsa", _class='titulo_informativo'),DIV(ICONE_PDV,_class="icone_tipo_venda"), _class="titulo_e_icone"), _href=URL('servicos', "caixa", args=['vender', 'pdv']), _class="link_sem_decorator"), _class="col-6"),
                    _class="row"),
                _class="caixa_escolha_tipo_cliente")
    return locals()  