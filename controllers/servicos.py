# -*- coding: utf-8 -*-

@auth.requires_membership('funcionario')
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

@auth.requires_membership('funcionario')
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
                return redirect(URL("servicos", "fornecedores"))
        elif request.args(0)=="novo":
            titulo="Novo fornecedor"
            subtitulo="Adicione um novo fornecedor."
            form=SQLFORM(db.fornecedores)
            html=DIV(DIV("Digitando um CNPJ válido ele irá automaticamente pegar os dados da Receita Federal",_class='avisos'),form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Fornecedor Adicionado"
                return redirect(URL("servicos", "fornecedores"))
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

@auth.requires_membership('funcionario')
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
                return redirect(URL("servicos", "produtos"))
        elif request.args(0)=="novo":
            titulo="Novo produto"
            subtitulo="Adicione um novo produto."
            form=SQLFORM(db.produtos, fields=["id_imagem","cod_barra", "produto","descricao"])
            html=DIV(form, _class='container_formulario')
            if form.process().accepted:
                response.flash="Produto Adicionado"
                return redirect(URL("servicos", "produtos"))
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

@auth.requires_membership('funcionario')
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
                    q_unidades=db(db.unidades.unidade==minha_unidade).select().first()
                    if q_unidades:
                        id_unidade=q_unidades.id
                    else:
                        id_unidade=db.unidades.insert(unidade=minha_unidade)
                else:
                    minha_unidade=request.vars.unidade
                    q_unidades=db(db.unidades.id==minha_unidade).select().first()
                    if q_unidades:
                        id_unidade=q_unidades.id
                    else:
                        id_unidade=1
                id_fornecedores_produtos=db.fornecedores_produtos.insert(quantidade=form.vars.quantidade, preco_custo=form.vars.preco_custo,fornecedores=int(request.args(1)),produtos=int(request.args(2)))
                q_produtos=db(db.produtos.id==request.args(2)).select().first()
                id_produto=q_produtos.update_record(quantidade=float(form.vars.quantidade_total), unidades=id_unidade, preco_final=form.vars.preco_manual)

                if id_fornecedores_produtos and id_produto:
                    db.commit()
                    response.flash="Adicionado"
                    return redirect(URL('servicos', 'estoque', args=["lancar"]))
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

@auth.requires_membership('funcionario')
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
            form=SQLFORM(db.clientes, request.args(1), fields=["nome", "data_de_nascimento", "cpf", "telefone_residencial", "telefone_celular", "email"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Cliente alterado"
                return redirect(URL("servicos", "clientes"))
        elif request.args(0)=="novo":
            titulo="Novo Cliente"
            subtitulo="Adicione um novo cliente."
            form=SQLFORM(db.clientes, fields=["nome", "data_de_nascimento", "cpf", "telefone_residencial", "telefone_celular", "email"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                id_cliente=form.vars.id
                response.flash="Cliente Adicionado"
                if request.vars.redirecionar=="pdv":
                    url_pdv=URL("servicos", "pdv", args=["cliente", id_cliente])
                    return redirect(url_pdv)
                elif request.vars.redirecionar:
                    return redirect(request.vars.redirecionar)
                else:
                    return redirect(URL("servicos", "clientes"))
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

@auth.requires_membership('administrador')
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
            form=SQLFORM(db.funcionarios, request.args(1), fields=["nome", "cpf", "data_de_nascimento", "telefone_residencial", "telefone_celular", "email","salario" ,"cargo" ,"conta"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Funcionário alterado"
                return redirect(URL("servicos", "funcionarios"))
        elif request.args(0)=="novo":
            titulo="Novo Funcionário"
            subtitulo="Adicione um novo funcionário."
            form=SQLFORM(db.funcionarios, fields=["nome", "cpf", "data_de_nascimento", "telefone_residencial", "telefone_celular", "email","salario" ,"cargo" ,"conta"])
            html=DIV(form, _class='container_formulario_generico')
            if form.process().accepted:
                response.flash="Funcionário Adicionado"
                return redirect(URL("servicos", "funcionarios"))
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

@auth.requires_membership('funcionario')
def caixa():
    html=""
    titulo=""
    subtitulo=""
    html_comandos=""
    if request.args(0):
        if request.args(0)=="cliente":
            if request.vars.redirecionar=="pdv":
                html_comandos=DIV(
                    A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'pdv', args=['avulso']), _title="voltar"),
                    A(DIV(ICONE_NOVO_CLIENTE, _class="botao_menu_pagina"), _href=URL('servicos', 'clientes', args=['novo'], vars={'redirecionar': 'pdv'}), _title="Novo cliente"),
                    _class="comandos_main_container")
            else:
                html_comandos=DIV(
                    A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa'), _title="voltar"),
                    A(DIV(ICONE_NOVO_CLIENTE, _class="botao_menu_pagina"), _href=URL('servicos', 'clientes', args=['novo'], vars={'redirecionar': URL('servicos', 'caixa', args=["cliente"])}), _title="Novo cliente"),
                    _class="comandos_main_container")
            titulo="Escolha um cliente"
            subtitulo="Escolha o cliente que quer comprar."
            html=CAT(MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES)
    else:
        titulo="Tipo de venda"
        subtitulo="Escolha se é venda a cliente vip ou cliente casual (Sem registro)"
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'index'), _title="voltar"),
            _class="comandos_main_container")
        html=DIV(
                DIV(
                    DIV(A(DIV(DIV("Cliente Indentificado",_class='titulo_informativo'), DIV(ICONE_CLIENTES,_class="icone_tipo_venda"), _class="titulo_e_icone"), _href=URL('servicos', "caixa",args=['cliente'] ), _class="link_sem_decorator"), _class="col-6"),
                    DIV(A(DIV(DIV("Venda avulsa", _class='titulo_informativo'),DIV(ICONE_PDV,_class="icone_tipo_venda"), _class="titulo_e_icone"), _href=URL('servicos', "pdv", args=['avulso']), _class="link_sem_decorator"), _class="col-6"),
                    _class="row"),
                _class="caixa_escolha_tipo_cliente")
    return locals()

@auth.requires_membership('funcionario')
def pdv():
    from conv_datetime import conv_date
    html=""
    titulo=""
    subtitulo=""
    cliente=""
    html_comandos=""
    if request.args(0):
        html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'estoque'), _title="voltar"),
            _class="comandos_main_container")
        if request.args(0)=="avulso" and not request.args(1):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa'), _title="voltar"),
                _class="comandos_main_container")
        elif request.args(0)=="cliente" and request.args(1):
            html_comandos=DIV(
                A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('servicos', 'caixa', args=["cliente"]), _title="voltar"),
                _class="comandos_main_container")
            q_cliente=db(db.clientes.id==request.args(1)).select().first()
            html_cliente_dados=DIV(
                DIV(
                DIV(DIV(H6("Dados do Cliente", _class='titulo_card'),_class="col-12"),
                    DIV("Nome: ", STRONG(q_cliente.nome), _class="col-12"),
                    DIV("CPF: ", STRONG(q_cliente.cpf), _class='col-5'),
                    DIV("Nascimento: ", STRONG(conv_date(q_cliente.data_de_nascimento, "%d/%m/%Y")), _class='col-7'),
                    _class='row', _style="color:black"),
                _class='card_dados', _style="background-color:white;"), _style='padding:10px; margin-bottom:20px')
            cliente=html_cliente_dados      
        elif request.args(0)=='visualizar':
            q_fornencedor=db(db.produtos.id==request.args(0)).select().first()
            if q_fornencedor:
                pass
            else:
                return "produto não encontrado"
        else:
            return "falta parâmetros"
        attr_modal={
                '_data-toggle':"modal",
                '_data-target':"#pdvmodal"
                }
        attr_modal3={
                '_data-toggle':"modal",
                '_data-target':"#pdvmodal3"
                }
        html = DIV(
                    DIV(_id="avisos_pdv"),
                    DIV(
                        DIV(
                            DIV(
                                DIV(
                                    DIV(
                                        DIV(
                                            DIV(_class="indeterminate"),
                                            _id="progress_pdv"),
                                         _class="col-12 progress_pdv_container"),                                
                                    DIV(
                                        INPUT(_id="quant_pdv", _style="width:100%", _class="quant_produto form-control", _autocomplete="off", _placeholder="Qtd", _disabled=""),
                                        _class="input_produto input-group col-2"),
                                    DIV("X", _class="col-1", _style="text-align: center;padding-top: 7px;font-weight: bold;"),
                                    DIV(
                                        INPUT(_id="cod_barras_pdv", _style="width:100%", _class="cod_produto form-control", _autocomplete="off", _placeholder="Código de barras", _disabled=""),
                                        _class="input_produto input-group col-9"),
                                    _class='row inputs_pdv'),
                                DIV(
                                    UL(
                                        LI(
                                            DIV(
                                                DIV("Item", _class="item_produto_pdv col-1"),
                                                DIV("Produto", _class="nome_produto_pdv col-5"),
                                                DIV("Preço", _class="preco_produto_pdv col-2"),
                                                DIV("Qtd", _class="qtd_produto_pdv, col-2"),
                                                DIV("Subtotal", _class="subtotal_produto_pdv col-2"),
                                                _class="row"),
                                            _class="list-group-item cabecalho"),
                                        _id="lista_produtos_vendidos",
                                        _class="list-group"),
                                    _class="produtos_comprados"),
                                DIV(
                                    DIV(
                                        DIV(STRONG("Quantidade de itens: "), SPAN(0.0, _id="quant_rod_pdv"), _class="total_container_pdv col-4"),
                                        _class="row"),
                                    _class="rodape_quantidade_pdv"),
                                _class="pdv_left_side"),
                            _class='col-7'),
                            DIV(
                                
                                DIV(
                                    DIV("OPERAÇÃO: ", STRONG("00000000000000", _id='operacao_pdv'), " - INÍCIO: ", STRONG("00/00/0000", _id='inicio_operacao_pdv') ,_class="operacao_pdv_container"),
                                    DIV(
                                        DIV(_id="view_item_pdv"),
                                        DIV(_id="codigo_item_pdv"),
                                        DIV(_id="descricao_item_pdv"),
                                        _class="item_info_container"),
                                    DIV(
                                        cliente,
                                        DIV(
                                            DIV(
                                                DIV(BUTTON("Finalizar (F6)", _id="btn_principal_pdv", _class="btn btn-sm btn-primary botao_pdv", **attr_modal3), _class="col-4"),
                                                DIV(BUTTON("Cancelar (F7)", _id="btn_cancelar_pdv", _class="btn btn-sm btn-primary botao_pdv"), _class="col-4"),
                                                DIV(A(BUTTON("Cliente (F8)", _id="btn_cliente_pdv", _class="btn btn-sm btn-primary botao_pdv"), _id="link_adicionar_cliente", _href=URL("servicos", "caixa", args=["cliente"], vars={'redirecionar':'pdv'})), _class="col-4"),
                                                _class="row"),
                                            DIV(
                                                DIV(BUTTON("Quantidade (Q)", _id="btn_quantidade_pdv", _class="btn btn-sm btn-primary botao_pdv"), _class="col-4"),
                                                DIV(A(BUTTON("Imprimir (Ctrl+P)", _id="btn_imprimir_pdv", _class="btn btn-sm btn-primary botao_pdv"), _id="botao_imprimir", _href="#", _target="_blank"), _class="col-4"),
                                                DIV(BUTTON("Localizar (Ctrl+F)", _id="btn_localizar_pdv", _class="btn btn-sm btn-primary botao_pdv", **attr_modal), _class="col-4"),
                                                _class="row"),
                                            _class="botoes_pdv"),
                                        DIV(
                                            DIV(DIV(STRONG("TOTAL(R$): "), DIV(0.0, _id="total_pdv"), _class='valor_total_pdv'), _class="total_container_pdv col-12"),
                                            DIV(STRONG("PAGO(R$): "), SPAN(0.0, _id="tot_pago_pdv"), _class="total_container_pdv col-6"),
                                            DIV(STRONG("TROCO(R$): "), SPAN(0.0, _id="troco_pdv"), _class="total_container_pdv col-6"),
                                            _class="row"),
                                        _class="rodape_total_pdv"),
                                    _class="pdv_rigth_side"),
                                _class='col-5'),
                        _class="row"),
                    _class="pdv")

    return locals()

@auth.requires_membership('funcionario')
def criar_nota():
    from nota_nao_fiscal_txt import CupomNaoFiscal
    if request.args(0):
        q_vendas_save = db((db.vendas.id==request.args(0))&(db.vendas.aberta==False)).select().first()
        if q_vendas_save:
            data_venda_finalizada=request.now
            cupom_nao_fiscal = CupomNaoFiscal()
            cupom_nao_fiscal.setData(data_venda_finalizada.strftime('%d/%m/%Y %H:%M:%S'))
            cupom_nao_fiscal.setCodigo(int(q_vendas_save.id))
            if q_vendas_save.cliente:
                cupom_nao_fiscal.setCliente([q_vendas_save.cliente.nome, q_vendas_save.cliente.cpf])
            q_produtos_vendidos = db(db.produto_vendas.vendas==q_vendas_save.id).select()
            for y in q_produtos_vendidos:
                cupom_nao_fiscal.addLinha([y.produtos.produto, str(y.ordem).zfill(3), " ".join(["ID:", str(y.produtos.cod_barra)]), y.produtos.preco_final, y.quantidade, y.produtos.preco_final*y.quantidade])
            cupom_nao_fiscal.setTotal(q_vendas_save.total)
            cupom_nao_fiscal.setDesconto(q_vendas_save.desconto)
            cupom_nao_fiscal.setValorPago(q_vendas_save.valor_pago)
            cupom_nao_fiscal.setTroco(q_vendas_save.troco)
            response.headers['Content-Type']='text/plain'
            return cupom_nao_fiscal.create()
        else:
            return "A nota não pode ser gerada"
    else:
        return "A nota não pode ser gerada"

@auth.requires_membership('funcionario')
def imprimir_nota():
    html=DIV(
    IFRAME(_src=URL("servicos", "criar_nota", args=[request.args(0)]), _style="width: 357px;height: 600px;margin-left: auto;margin-right: auto;"),
    _style="width: 357px;height: 600px;margin-left: auto;margin-right: auto;")
    return html
