# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
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

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
