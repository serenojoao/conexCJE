# -*- coding: utf-8 -*-
# Autor: PhanterJR

@auth.requires_membership('funcionario')
def echo_phantersqllistas():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_fornecedores():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_FORNECEDORES.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_FORNECEDORES.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_FORNECEDORES.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_FORNECEDORES.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_FORNECEDORES.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_FORNECEDORES.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_estoque_fornecedores():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_FORNECEDORES.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_estoque_produtos():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_PRODUTOS.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_estoque_disponivel():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_ESTOQUE_DISPONIVEL.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_clientes():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_CLIENTES.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_CLIENTES.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_CLIENTES.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_CLIENTES.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_CLIENTES.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_CLIENTES.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('administrador')
def echo_phantersqllistas_funcionarios():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_FUNCIONARIOS.id_phantersqllistas_container, json.dumps(html.xml()))

def echo_phantersqllistas_caixa_clientes():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_CAIXA_CLIENTES.id_phantersqllistas_container, json.dumps(html.xml()))

@auth.requires_membership('funcionario')
def echo_phantersqllistas_pdv_produtos():
    import json
    ordem=request.vars.ordem
    sentido=request.vars.sentido
    campo=request.vars.campo
    palavra=request.vars.palavra
    num_registros=int(request.vars.num_registros)
    pagina=int(request.vars.pagina)
    if palavra:
        html=MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.echoPhanterSqlListas(ordem, sentido , campo , palavra , num_registros , pagina)
        frase="Pesquisando em \"%s\" por \"%s\"" %(MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.labelsearchfield, palavra)
        return "$(\"#%s\").html(%s); $(\"#%s\").text(%s)" %(MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.id_phantersqllistas_container, json.dumps(html.xml()), MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.id_phantersqllistas_avisos, json.dumps(frase))
    else:
        html=MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.echoPhanterSqlListas(ordem, 'crescente', campo , "", 50 , 1)
        return "$(\"#%s\").html(%s);" %(MODELS_PHANTERSQLLISTAS_PDV_PRODUTOS.id_phantersqllistas_container, json.dumps(html.xml()))
