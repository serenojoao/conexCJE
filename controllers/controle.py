# -*- coding: utf-8 -*-

@auth.requires_membership('administrador')
def sobre():
    html=""
    titulo="Fale sobre a empresa"
    subtitulo="Dê ao cliente informações relevantes sobre a empresa, como por exemplo, a missão, objetivo, estrutura, etc."
    html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('default', 'sobre_nos'), _title="voltar"))
    if db(db.sobre).isempty():
        id_novo_sobre = db.sobre.insert(html="")
    else:
        id_novo_sobre = db(db.sobre).select().first().id
    form = SQLFORM(db.sobre, id_novo_sobre, showid=False)
    return locals()

@auth.requires_membership('administrador')
def contato():
    html=CAT()
    titulo="Contatos realizados"
    subtitulo="Aqui são listados os contatos realizados (lidos e não lidos)"
    html_comandos=DIV(
            A(DIV(ICONE_VOLTAR, _class="botao_menu_pagina"), _href=URL('default', 'contato'), _title="voltar"))
    if db(db.contato).isempty():
        html="Não há contatos disponíveis"
    else:
        html_contatos_novos=UL(_class="list-group lista_container_conexcje")
        html_contatos_antigos=UL(_class="list-group lista_container_conexcje")
        q_contatos = db(db.contato.visto==False).select()
        if q_contatos:
            html.append(CAT(BR(),H3("NOVOS CONTATOS"), HR(), html_contatos_novos))
            for x in q_contatos:
                attr={"_id":"btn_lista_%s" %(x.id), "_data-toggle":"dropdown", "_aria-haspopup":"true", "_aria-expanded":"false"}
                attr2={"_aria-labelledby": "btn_lista_%s" %(x.id)}
                data_attr = {"_data-id-contato": x.id}
                html_comando_item=DIV(
                        DIV(I(_class="fas fa-ellipsis-v"),_class='comandos_botao dropdown-toggle', **attr),
                    _class='comandos_container dropleft')
                menus=[
                    DIV("Ver", _class="botao_contato_ver", **data_attr),
                    DIV("Deletar", _class="botao_contato_deletar", **data_attr)
                    ]
                drop_item=CAT()
                html_comando_meuns=(DIV(
                            drop_item,
                            _class="dropdown-menu", **attr2))
                for z in menus:
                    drop_item.append(
                        DIV(z, _class="dropdown-item")
                        )
                html_comando_item.append(html_comando_meuns)
                html_contatos_novos.append(LI(
                    DIV(
                        DIV(x.nome, _class='col-2'),
                        DIV(A(x.email, _href="mailto:%s" %x.email), _class='col-2'),
                        DIV(DIV(x.mensagem, _id="mensagem_ver_contato_%s" %x.id, _class='mensagem_ver_contato hide'), _class='col-8'),
                        html_comando_item,
                        _class="row"),
                    _id="linha_contato_%s" %x.id,
                    _class="list-group-item cabecalho"))
        q_contatos2 = db(db.contato.visto==True).select()
        if q_contatos2:
            html.append(CAT(BR(),H3("CONTATOS JÁ LIDOS"), HR(), html_contatos_antigos))
            for x in q_contatos2:
                attr={"_id":"btn_lista_%s" %(x.id), "_data-toggle":"dropdown", "_aria-haspopup":"true", "_aria-expanded":"false"}
                attr2={"_aria-labelledby": "btn_lista_%s" %(x.id)}
                data_attr = {"_data-id-contato": x.id}
                html_comando_item=DIV(
                        DIV(I(_class="fas fa-ellipsis-v"),_class='comandos_botao dropdown-toggle', **attr),
                    _class='comandos_container dropleft')
                menus=[
                    DIV("Ver", _class="botao_contato_ver", **data_attr),
                    DIV("Deletar", _class="botao_contato_deletar", **data_attr)
                    ]
                drop_item=CAT()
                html_comando_meuns=(DIV(
                            drop_item,
                            _class="dropdown-menu", **attr2))
                for z in menus:
                    drop_item.append(
                        DIV(z, _class="dropdown-item")
                        )
                html_comando_item.append(html_comando_meuns)

                html_contatos_antigos.append(LI(
                    DIV(
                        DIV(x.nome, _class='col-2'),
                        DIV(A(x.email, _href="mailto:%s" %x.email), _class='col-2'),
                        DIV(DIV(x.mensagem, _id="mensagem_ver_contato_%s" %x.id, _class='mensagem_ver_contato hide'), _class='col-8'),
                        html_comando_item,
                        _class="row"),
                    _class="list-group-item"))
    return locals()    