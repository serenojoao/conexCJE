# -*- coding: utf-8 -*-
# Autor: PhanterJR

def index():
    from em_reais import em_reais
    q_produtos=db(db.produtos.quantidade>5).select()
    html=DIV(_class='row')
    for x in q_produtos:
        attr={"_data-url_imagem":URL('default', 'download', args=[x.id_imagem.imagem])}
        html.append(
            DIV(
                DIV(
                    A(IMG(_class="card-img-top", _src=URL('default', 'download', args=[x.id_imagem.imagem]), _alt=""), _href="#", _title="clique para ampliar", _class="imagem_para_visualizar", **attr),
                    DIV(
                        H4(
                            A(
                                x.produto,
                                _href="#"),
                            _class="card-title"),
                        P(
                            x.descricao,
                            _class="card-text"),
                         DIV(
                            LABEL("preço", _class="card-rotulo"),
                            DIV(em_reais(x.preco_final)),
                            _class="preco"),
                        _class="card-body"),
                    _class="card h-100"),
                _class="col-lg-3 col-md-4 col-sm-6 portfolio-item")
            )
    return locals()

def sobre_nos():
    html=""
    titulo="SOBRE NÓS"
    subtitulo="Conheça um pouco sobre nossa empresa"
    link_restrito=""
    if auth.user:
        if auth.has_membership("administrador"):
            link_restrito = A(DIV(ICONE_CONFIGURACOES, _class="botao_menu_pagina"),_href=URL('controle', 'sobre'), _title="Editar informações SOBRE NÓS")

    html_comandos=DIV(
        A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('default', 'index'), _title="voltar"),
        link_restrito,
        _class="comandos_main_container")
    html=DIV("Aguardando informações serem adicionadas")
    return locals()

def contato():
    
    html=""
    titulo="CONTATO"
    subtitulo="Entre em contato conosco, tire suas dúvidas."
    link_restrito=""
    if auth.user:
        if auth.has_membership("administrador"):
            link_restrito = A(DIV(ICONE_CONTATO, _class="botao_menu_pagina"),_href=URL('controle', 'contato'), _title="Ver mensagens recebidas")

    html_comandos=DIV(
        A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('default', 'index'), _title="voltar"),
        link_restrito,
        _class="comandos_main_container")
    form=SQLFORM(db.contato, fields=["nome", "email", "mensagem"])
    if form.process().accepted:
        response.flash="Mensagem Envida!"
    html=DIV(form, _class='container_formulario_generico')
    return locals()

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)
