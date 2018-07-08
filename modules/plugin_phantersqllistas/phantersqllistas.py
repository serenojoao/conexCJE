# -*- coding: utf-8 -*-

from gluon.html import *
from gluon import current
import json
from remover_acentos import remover_acentos
import types

class PhanterSqlListas():
    url_ajax=URL("plugin_phantersqllistas", 'echo_phantersqllistas')
    def __init__(self, db, table, searchfield, query=None, fields=None, url_ajax=url_ajax, pagina=None, linhas=None):
        self.db=db
        self.table=table
        self.url_ajax=url_ajax
        self.nome_tabela=table._tablename
        self.field_names=[]
        self.fields(fields)
        self._menu_item=[]
        self._funcao_linha=None
        self._funcao_campo=None
        self.pagina=pagina
        self.linhas=linhas
        self._query=query
        self.parentclass=""
        self._query=query
        self.searchfield=searchfield
        self.labelsearchfield=table[searchfield].label
        self.html_search=""
        self._ordem="id"
        self._sentido="crescente"
        self._campo=searchfield
        self._palavra=""
        self._num_registros=50
        self._pagina=1
        self._q_table(self._ordem, self._sentido, self.searchfield, self._palavra, self._num_registros, self._pagina)
        self.id_phantersqllistas_container="phantersqllistas-main_%s" %self.nome_tabela
        self.id_phantersqllistas_avisos="phantersqllistas-avisos_%s" %self.nome_tabela

    def fields(self, fields):
        if fields:
            if isinstance(fields, (tuple, list)):
                for x in fields:
                    if isinstance(x, (tuple, list)):
                        self.field_names.append(x[0])
                    else:
                        self.field_names.append(x)
            self._fields=fields
        else:
            table=self.table
            self._fields=table.fields


    def addMenuItem(self, lambda_function):
        if isinstance(lambda_function, types.FunctionType):
           self._menu_item.append(lambda_function)
        else:
            raise "O item deve ser uma função"
        return self._menu_item

    def personalizarLinha(self, lambda_function, parentclass="phantersqllistas-listas_linha_pesonalizada"):
        self.parentclass=parentclass
        if isinstance(lambda_function, types.FunctionType):

            self._funcao_linha=lambda_function
        else:
            raise "O item deve ser uma função"
    def personalizarCampo(self, dict_lambda_function):
        if isinstance(dict_lambda_function, dict):
            self._funcao_campo=dict_lambda_function
        else:
            raise "O item deve ser um dicionario como: {nome_do_Field: lambada}"        

    def urlAJAX(self, url):
        self.url_ajax=url
        table=self.table
        nome_tabela=self.nome_tabela
        searchfield=self.searchfield
        script=SCRIPT("""
            function pesquisar(){
                var botao_pesquisar=$("#%(nome_tabela)s_botao_pesquisar")
                var ordem=$(botao_pesquisar).attr("data-ordem");
                var sentido=$(botao_pesquisar).attr("data-sentido");
                var campo=$(botao_pesquisar).attr("data-campo");
                var num_registros=$(botao_pesquisar).attr("data-num_registros");
                var pagina=$(botao_pesquisar).attr("data-pagina");
                var palavra=$("#%(nome_tabela)s_input_pesquisar").val();
                if(palavra!=""){
                    $(".phantersqllistas-progress").addClass("actived");
                }
                var url_ajax="%(url)s?ordem="+ordem+"&sentido="+sentido+"&campo="+campo+"&num_registros="+num_registros+"&pagina="+pagina+"&palavra="+palavra
                console.log(url_ajax);
                ajax(url_ajax, [], ":eval");
            };
            $("#%(nome_tabela)s_select_campo_pesquisar").on("change", function(){
                $("#%(nome_tabela)s_botao_pesquisar").attr("data-campo", $(this).val())
                var valor_place=$("#%(nome_tabela)s_select_campo_pesquisar option:selected").text();
                $("#%(nome_tabela)s_input_pesquisar").attr("placeholder", "Pesquisar em "+valor_place)
            });            
            $("#%(nome_tabela)s_botao_pesquisar").on("click", function(){
                pesquisar();
            });
            $("#%(nome_tabela)s_input_pesquisar").on("keyup", function(event){
                  event.preventDefault();
                  if (event.keyCode === 13) {
                    pesquisar();
                  }
            });
        """ %dict(url=url, nome_tabela=nome_tabela))
        self.url_ajax=url
        attr={"_id":"%s_input_pesquisar" %nome_tabela,
            "_type":"text",
            "_class":"form-control",
            "_placeholder":"Pesquisar em %s" %(table[searchfield].label),
            "_aria-label":"Pesquisar...",
            "_aria-describedby":"basic-addon2",
            "_autocomplete":"off"}
        attr2={"_id":"%s_botao_pesquisar" %nome_tabela,
                "_class":"input-group-append phantersqllistas-botao_pesquisar",
                "_data-ordem":"id",
                "_data-sentido":"crescente",
                "_data-campo":self.searchfield,
                "_data-num_registros":50,
                "_data-pagina":1
                }
        html_select=SELECT(_autocomplete="off", _class="form-control", _id="%s_select_campo_pesquisar" %self.nome_tabela)
        for f in self.field_names:
            html_select.append(OPTION(table[f].label ,_value=f, _selected='selected' if f==self.searchfield else None))

        html=CAT(
            DIV(
                DIV(
                    DIV(
                        INPUT(**attr),
                        DIV(
                            SPAN("Pesquisar", _class="input-group-text", _id="basic-addon2"),
                        **attr2), 
                        _class="input-group mb-3"),
                    _class='col-8'),
                    DIV(
                DIV(html_select,  _class="input-group"),
                _class='col-4'
                ),
            _class='phantersqllistas-caixa_pesquisa row'), 
            script)
        self.html_search=DIV(
            html, 
            DIV(
                DIV(_class="indeterminate"),
                _class='phantersqllistas-progress'), 
            DIV(
                DIV(_id=self.id_phantersqllistas_avisos, _class="phantersqllistas-avisos"),
                _class="col-12"),
            _class="row")
    
    def _q_table(self, ordem, sentido , campo , palavra , num_registros=50 , pagina=1):
        self.html_paginacao=self.paginacao(campo, palavra, num_registros, pagina)
        inicio=((num_registros*pagina)-num_registros)
        fim=inicio+num_registros
        fields=self.field_names
        db=self.db
        table=self.table
        campos=[table[x] for x in fields]
        t_ordem=table[ordem]
        if sentido=="crescente":
            t_ordem=table[ordem]
        else:
            t_ordem=~table[ordem]
        if palavra:
            if self._query:
                query=(table[campo].contains([palavra, remover_acentos(palavra)]))&(self._query)
            else:
                query=table[campo].contains([palavra, remover_acentos(palavra)])
            q_table=db(query).select(table["id"],*campos, orderby=t_ordem, limitby=[inicio, fim])
            if not q_table:
                if self._query:
                    query=self._query
                else:
                    query=table
                q_table_temp=db(query).select(table.id, table[campo])
                dados_belongs=[x.id for x in q_table_temp if remover_acentos(palavra) in remover_acentos(x[campo])]
                q_table=db(table.id.belongs(dados_belongs)).select(table["id"],*campos, orderby=t_ordem, limitby=[inicio, fim])
        else:
            if self._query:
                query=self._query
            else:
                query=table
            q_table=db(query).select(table["id"],*campos, orderby=t_ordem, limitby=[inicio, fim])
        self.q_table=q_table

    def paginacao(self, campo, palavra, num_registros=50, pagina=1):
        html_final=""
        db=self.db
        table=self.table
        q_pesquisa=table[campo].contains(palavra)
        if palavra:
            quant=db(q_pesquisa).count()
        else:
            quant=db(table).count()
        quant_paginas=0
        if quant:
            if quant>num_registros:
                quant_paginas=quant/num_registros
                if q_table%num_registros:
                    quant_paginas+1
                attr={"_aria-label":"Paginação PhanterSqlListas"}
                attr_voltar={"_aria-label":"Voltar", "_class":"page-link"}
                attr_voltar2={"_aria-hidden":"true"}
                attr_avancar={"_aria-label":"Voltar", "_class":"page-link"}
                html_paginacao=UL(
                                LI(
                                    DIV(**attr_voltar), 
                                    SPAN(XML("&laquo;")**attr_voltar2),
                                    _class='page-item'),
                                _class="pagination")
                                   
                for y in range(0, quant_paginas):
                    html_paginacao.append(LI(DIV(y+1,_class="page-link%s" %(" active" if y+1 == pagina else "")),_class="page-item"))
                html_paginacao.append(LI(
                                            DIV(**attr_avancar), 
                                            SPAN(XML("&raquo;")**attr_voltar2),
                                            _class='page-item'))
                html_final=NAV(
                            html_paginacao,
                        **attr)
        return html_final

    def echoPhanterSqlListas(self, ordem, sentido , campo , palavra , num_registros=50 , pagina=1):
        self.searchfield=campo
        self.labelsearchfield=self.table[campo].label
        self._q_table(ordem, sentido, campo, palavra, num_registros, pagina)
        return self.update()

    def update(self):
        self.urlAJAX(self.url_ajax)
        html=UL(_class='list-group lista_container_conexcje')
        db=self.db
        q_table=self.q_table
        if q_table:
            html_head=DIV(_class="cabecalho_lista_container row")
            for x in self._fields:
                if isinstance(x,(list, tuple)):
                    campo=x[0]
                    attr=x[1]
                    if isinstance(attr, dict):
                        html_temp=DIV(self.table[campo].label, **attr)
                    else:
                        html_temp=DIV(self.table[campo].label, _class="thead %s" %(attr))
                else:
                    campo=x
                    html_temp=DIV(self.table[campo].label, _class="thead")
                html_head.append(html_temp)
            html.append(
                LI(
                    html_head,
                _class="list-group-item cabecalho")
                )
            for x in q_table:

                html_comando_item=""
                if self._funcao_linha:
                    classparent=str("list-group-item %s" %(self.parentclass)).strip()
                    html.append(
                        LI(
                            self._funcao_linha(x),
                        _class=classparent)
                    )
                else:
                    if self._menu_item:
                        attr={"_id":"btn_lista_%s" %(x.id), "_data-toggle":"dropdown", "_aria-haspopup":"true", "_aria-expanded":"false"}
                        attr2={"_aria-labelledby": "btn_lista_%s" %(x.id)}
                        html_comando_item=DIV(
                                DIV(I(_class="fas fa-ellipsis-v"),_class='comandos_botao dropdown-toggle', **attr),
                            _class='comandos_container dropleft')
                        for z in self._menu_item:
                            html_comando_item.append(DIV(
                                        DIV(z(x), _class="dropdown-item"),
                                        _class="dropdown-menu", **attr2)
                            )
                    html_campos=DIV(_class="item_lista_container row")
                    for z in self._fields:
                        if isinstance(z,(list, tuple)):
                            campo=z[0]
                            attr=z[1]
                            if self._funcao_campo:
                                if isinstance(self._funcao_campo, dict):
                                    print "passou aqui %s" %campo
                                    if campo in self._funcao_campo:
                                        print "opaaa"
                                        valor_campo=self._funcao_campo[campo](x[campo])
                                        print self._funcao_campo[campo]
                                    else:
                                        valor_campo=x[campo]
                                else:
                                    if self._funcao_campo[1]==campo:
                                        valor_campo=self._funcao_campo[0](x[campo])
                                    else:
                                        valor_campo=x[campo]
                            else:
                                valor_campo=x[campo]
                            if isinstance(attr, dict):
                                html_temp=DIV(valor_campo, **attr)
                            else:
                                html_temp=DIV(valor_campo, _class="tfield %s" %(attr))
                        else:
                            campo=z
                            if self._funcao_campo:
                                if isinstance(self._funcao_campo, dict):
                                    if campo in self._funcao_campo:
                                        valor_campo=self._funcao_campo[campo](x[campo])
                                    else:
                                        valor_campo=x[campo]
                                else:
                                    if self._funcao_campo[1]==campo:
                                        valor_campo=self._funcao_campo[0](x[campo])
                                    else:
                                        valor_campo=x[campo]
                            else:
                                valor_campo=x[campo]
                            html_temp=DIV(valor_campo, _class="tfield")
                        html_campos.append(html_temp)
                    html_campos.append(html_comando_item)
                    html.append(
                        LI(
                            html_campos,
                        _class="list-group-item")
                    )
        return CAT(self.html_search, html, self.html_paginacao)

    def xml(self):
        return "%s" %(DIV(self.update(), _class='phantersqllistas_container', _id=self.id_phantersqllistas_container))
