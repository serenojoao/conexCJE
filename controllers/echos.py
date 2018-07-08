# -*- coding: utf-8 -*-
# Autor: PhanterJR

from em_reais import em_reais
from nota_nao_fiscal_txt import CupomNaoFiscal
import json

@auth.requires_membership('funcionario')
def dados_cnpj():
    if request.args(0):
        import urllib2
        import json
        aberto = urllib2.urlopen("https://www.receitaws.com.br/v1/cnpj/%s" %request.args(0))
        html=aberto.read()
        return response.json(json.loads(html))

@auth.requires_membership('funcionario')
def pdv():
    import json
    if request.args(0):
        if request.args(0)=="abrir-venda" and request.args(1) and request.args(2):
            vendedor = request.args(1)
            cliente = request.args(2)
            q_vendedor = db(db.funcionarios.id==vendedor).select(db.funcionarios.id).first()
            if q_vendedor:
                q_venda_aberta = db((db.vendas.vendedor==q_vendedor.id)&(db.vendas.aberta==True)).select().first()
                total = 0.0
                tot_itens=0
                if q_venda_aberta:
                    q_produtos_vendidos = db(db.produto_vendas.vendas==q_venda_aberta.id).select()
                    print cliente
                    if not cliente=="avulso":
                        q_cliente = db(db.clientes.id==cliente).select(db.clientes.id).first()
                        if q_cliente:
                            if not (q_venda_aberta.cliente==q_cliente.id):
                                q_venda_aberta.update_record(cliente=q_cliente.id)
                                db.commit()
                    html_produtos=CAT()
                    url_foto=""
                    codigo_barra_prod=""
                    descricao=""
                    for x in q_produtos_vendidos:
                        print "oxe"
                        tot_itens+=1
                        total += (x.produtos.preco_final*x.quantidade)
                        html_produtos.append(LI(
                                                DIV(
                                                    DIV(str(tot_itens).zfill(3), _class="item_produto_pdv col-1"),
                                                    DIV(x.produtos.produto, _class="nome_produto_pdv col-5"),
                                                    DIV(em_reais(x.produtos.preco_final), _class="preco_produto_pdv col-2"),
                                                    DIV(x.quantidade, _class="qtd_produto_pdv, col-2"),
                                                    DIV(em_reais(x.produtos.preco_final*x.quantidade), _class="subtotal_produto_pdv col-2"),
                                                    _class="row"),
                                                _class="list-group-item")
                        )
                        url_foto = URL('default', 'download', args=[x.produtos.id_imagem.imagem])
                        codigo_barra_prod = x.produtos.cod_barra
                        descricao = x.produtos.descricao

                    url_ajax = URL('echos', 'pdv', args=['adicionar-produtos', q_venda_aberta.id])
                    script = '$("#quant_pdv").removeAttr("disabled").val("1");'
                    script+= '$("#operacao_pdv").text(%s);' %json.dumps(str(q_venda_aberta.id).zfill(10))
                    script+= '$("#inicio_operacao_pdv").text(%s);' %json.dumps(str(q_venda_aberta.data_venda.strftime('%d/%m/%Y %H:%M:%S')))
                    script+= '$("#codigo_item_pdv").html("<strong>ÚLTIMO ITEM</strong> - CÓDIGO: %s");' %codigo_barra_prod
                    script+= '$("#descricao_item_pdv").text(%s);' %json.dumps(descricao)
                    script+= '$("#cod_barras_pdv").removeAttr("disabled").focus();'
                    if q_produtos_vendidos:
                        script+= '$("#avisos_pdv").text("Atenção! A compra se encontra em aberto, para nova compra esta tem que ser fechada.");'
                        script+= '$("#view_item_pdv").css("background-image", "url(\'%s\')");' %url_foto
                        script+= '$("#view_item_pdv").css("background-size", "100% auto");'
                    script+= '$("#progress_pdv").fadeOut();$("#cod_barras_pdv").attr("url-ajax","%s");' %(url_ajax)
                    script+= '$("#cod_barras_pdv").attr("data-tot-itens","%s");' %(tot_itens)
                    script+= '$("#quant_rod_pdv").text("%s");' %(tot_itens)
                    script+= '$("#lista_produtos_vendidos").append(%s);' %(json.dumps(html_produtos.xml()))
                    script+= '$("#cod_barras_pdv").attr("data-tot-preco","%s");' %(total)
                    script+= '$("#total_pdv").text("%s");' %(em_reais(float(total)))
                    script+= '$("#total_pdv_modal").text("%s");' %(total)
                    script+= '$("#cod_barras_pdv").attr("data-id-venda","%s");' %(q_venda_aberta.id)
                    script+= '$("#botao_imprimir").attr("href", "%s");' %URL('servicos', 'imprimir_nota', args=[q_venda_aberta.id])
                    script+= '$("#botao_imprimir_modal").attr("href", "%s");' %URL('servicos', 'imprimir_nota', args=[q_venda_aberta.id])
                    return script
                else:
                    print cliente
                    if cliente=="avulso":
                        print "cliente avulso"
                        id_venda = db.vendas.insert(vendedor=q_vendedor.id)
                    else:
                        q_cliente = db(db.clientes.id==cliente).select(db.clientes.id).first()
                        if q_cliente:
                            print "cliente %s" %q_cliente.id
                            id_venda = db.vendas.insert(vendedor=q_vendedor.id, cliente=q_cliente.id)
                        else:
                            return "$(\".toast\").text(\"Cliente não Encontrado\").fadeIn();"
                    q_venda_aberta = db((db.vendas.id==id_venda)).select().first()
                    url_ajax = URL('echos', 'pdv', args=['adicionar-produtos', id_venda])
                    script = '$("#quant_pdv").removeAttr("disabled").val("1");'
                    script+= '$("#operacao_pdv").text(%s);' %json.dumps(str(id_venda).zfill(10))
                    script+= '$("#inicio_operacao_pdv").text(%s);' %json.dumps(str(q_venda_aberta.data_venda.strftime('%d/%m/%Y %H:%M:%S')))

                    script+= '$("#cod_barras_pdv").removeAttr("disabled").focus();'
                    script+= '$("#progress_pdv").fadeOut();'
                    script+= '$("#cod_barras_pdv").attr("data-tot-itens","%s");' %(tot_itens)
                    script+= '$("#quant_rod_pdv").text("%s");' %(tot_itens)
                    script+= '$("#cod_barras_pdv").attr("data-tot-preco","%s");' %(total)
                    script+= '$("#total_pdv").text("%s");' %(em_reais(float(total)))
                    script+= '$("#total_pdv_modal").text("%s");' %(0.0)
                    script+= '$("#cod_barras_pdv").attr("url-ajax","%s");' %(url_ajax)
                    script+= '$("#cod_barras_pdv").attr("data-id-venda","%s");' %(id_venda)
                    script+= '$("#botao_imprimir").attr("href", "%s");' %URL('servicos', 'imprimir_nota', args=[id_venda])
                    script+= '$("#botao_imprimir_modal").attr("href", "%s");' %URL('servicos', 'imprimir_nota', args=[id_venda])
                    return script
            else:
                return "$(\".toast\").text(\"Vendedor não Encontrado\").fadeIn();$(\"#pop\")[0].play();"
        elif request.args(0)=="adicionar-produtos" and request.args(1) and request.args(2) and request.args(3) and request.args(4) and request.args(5):
            cod_barra_prod =  request.args(2)
            vendas = request.args(1)
            quantidade = request.args(3)
            ordem = request.args(4)
            total_atual = float(request.args(5))
            q_vendas = db((db.vendas.id==vendas)&(db.vendas.aberta==True)).select().first()
            if q_vendas:
                q_produto = db(db.produtos.cod_barra==str(cod_barra_prod)).select().first()
                html_produtos = CAT()
                if q_produto:
                    id_registro_venda=None
                    url_foto = URL('default', 'download', args=[q_produto.id_imagem.imagem])
                    codigo_barra_prod = q_produto.cod_barra
                    descricao = q_produto.descricao
                    print total_atual, "-->",
                    total_val = q_produto.preco_final*float(quantidade)
                    print total_val
                    q_ver_venda = db(
                                    (db.produto_vendas.vendas==q_vendas.id)&
                                    (db.produto_vendas.quantidade==float(quantidade))&
                                    (db.produto_vendas.ordem==int(ordem)+1)
                                    ).select().first()
                    if not q_ver_venda:
                        id_registro_venda = db.produto_vendas.insert(vendas=q_vendas.id, 
                                                produtos=q_produto.id, 
                                                quantidade=quantidade, 
                                                valor_pago=q_produto.preco_final, 
                                                ordem=int(ordem)+1)
                        db.commit()
                    if id_registro_venda:
                        total_atual+=total_val
                        print "veio"
                        html_produtos.append(LI(
                                                DIV(
                                                    DIV(str(int(request.args(4))+1).zfill(3), _class="item_produto_pdv col-1"),
                                                    DIV(q_produto.produto, _class="nome_produto_pdv col-5"),
                                                    DIV(em_reais(q_produto.preco_final), _class="preco_produto_pdv col-2"),
                                                    DIV(quantidade, _class="qtd_produto_pdv, col-2"),
                                                    DIV(em_reais(q_produto.preco_final*float(quantidade)), _class="subtotal_produto_pdv col-2"),
                                                    _class="row"),
                                                _class="list-group-item")
                        )
                        script= '$("#beep")[0].play(); $("#cod_barras_pdv").attr("data-tot-itens","%s");' %(int(request.args(4))+1)
                        script+= '$("#cod_barras_pdv").attr("data-tot-preco","%s");' %(total_atual)
                        script+= '$("#total_pdv_modal").text("%s");' %(total_atual)
                        script+= '$("#view_item_pdv").css("background-image", "url(\'%s\')");' %url_foto
                        script+= '$("#view_item_pdv").css("background-size", "100% auto");'
                        script+= '$("#codigo_item_pdv").html("<strong>ÚLTIMO ITEM</strong> - CÓDIGO: %s");' %codigo_barra_prod
                        script+= '$("#descricao_item_pdv").text(%s);' %json.dumps(descricao)
                        script+= '$("#total_pdv").text("%s");' %(em_reais(float(total_atual)))
                        script+= '$("#lista_produtos_vendidos").append(%s);' %(json.dumps(html_produtos.xml()))
                        script+= '$("#quant_rod_pdv").text("%s");' %(int(request.args(4))+1)
                        return script
                else:
                    return "$(\".toast\").text(\"Produto não localizado\").fadeIn(); $(\"#pop\")[0].play();"
            else:
                return "$(\".toast\").text(\"Venda não localizada\").fadeIn();"
        elif request.args(0)=="finalizar" and request.args(1) and request.args(2) and request.args(3) and request.args(4) and request.args(5):
            vendas = request.args(1)
            total =  float(request.args(2))
            valor_pago = float(request.args(3))
            troco = request.args(4)
            desconto = request.args(5)
            data_venda_finalizada = request.now
            q_vendas = db((db.vendas.id==vendas)&(db.vendas.aberta==True)).select().first()
            if q_vendas:
                id_resultado = q_vendas.update_record(
                    total=total,
                    desconto=desconto,
                    valor_pago=valor_pago ,
                    troco= troco,
                    data_venda_finalizada=request.now,
                    aberta=False,
                    )
                db.commit()
                script = '$("#botao_imprimir_modal").attr("href", %s);' % json.dumps(URL('servicos', 'imprimir_nota', args=[q_vendas.id]))
                script += '$("#botao_imprimir").attr("href", %s);' % json.dumps(URL('servicos', 'imprimir_nota', args=[q_vendas.id]))
                script += 'finalizando_compra();'
                return script



            else:
                return "$(\".toast\").text(\"Venda não localizada\").fadeIn();"

@auth.requires_membership('funcionario')
def cancelar_venda():
    if request.args(0):
        set_Vendas=db(db.vendas.id==request.args(0))
        q_vendas=set_Vendas.select().first()
        if q_vendas:
            set_Vendas.delete()
            db.commit()
            return "window.location=\"/conexcje/servicos/pdv/avulso\";"


@auth.requires_membership('administrador')
def deletar_mensagem():
    if request.args(0):
        meu_set=db(db.contato.id==request.args(0))
        q_mensagem=meu_set.select().first()
        if q_mensagem:
            meu_set.delete()
            db.commit()
            return '$(".toast").text("Contato Deletado!"); $(".toast").fadeIn();deletado_sucesso();'

@auth.requires_membership('administrador')
def mensagem_vista():
    if request.args(0):
        meu_set=db(db.contato.id==request.args(0))
        q_mensagem=meu_set.select().first()
        if q_mensagem:
            q_mensagem.update_record(visto=True)
            return '$("#linha_contato_%s").removeClass("cabecalho");' %request.args(0)