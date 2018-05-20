# -*- coding: utf-8 -*-

db.define_table("categorias",
    Field("categoria")
    )
db.define_table("unidades",
    Field("unidade", 'string'),
    format="%(unidade)s"
    )

db.define_table("fornecedores",
    Field("cnpj", "string", label='CNPJ (apenas números)'),
    Field("fantasia", 'string', label="Nome de fantasia"),
    Field("nome", "string", label="Razão Social"),
    Field("telefone", 'string'),
    Field("email", 'string'),
    Field("logradouro", "string"),
    Field("bairro", "string"),
    Field("numero", "string"),
    Field("municipio", "string"),
    Field("uf", "string"),
    Field("cep", "string")
    )

db.define_table("produtos",
    Field('id_imagem', 'reference plugin_phanterimages_uploads', label="id_imagem"),
    Field('cod_barra', 'string'),
    Field("produto", "string"),
    Field("descricao", "text"),
    Field("quantidade", "double", default=0),
    Field("unidades", "reference unidades"),
    Field("preco_final", "double", default=0),
    Field("disponivel", "boolean", default=True)
    )

db.define_table("categorias_produtos",
    Field("categorias", "reference categorias"),
    Field("produtos", "reference produtos")
    )

db.define_table("fornecedores_produtos",
    Field("quantidade", "double", default=0),
    Field("preco_custo", "double", default=0),
    Field("fornecedores", "reference fornecedores", requires=IS_IN_DB(db, db.fornecedores)),
    Field("produtos", "reference produtos", requires=IS_IN_DB(db, db.produtos))
    )
db.fornecedores_produtos.quantidade.requires=IS_FLOAT_IN_RANGE(0.0000000001, None, dot=".", error_message='Tem que ser maior que ZERO')

db.define_table("carrinho",
    Field("produtos", "reference produtos"),
    Field("quantidade", "double", default=1),
    auth.signature
    )

db.define_table("clientes",
    Field("nome", "string"),
    Field("cpf", "string"),
    Field("telefone_residencial", "string"),
    Field("telefone_celular", "string"),
    Field("email", "string")
    )

db.define_table("vendas",
    Field("cliente", "reference clientes"),
    Field("valor_pago", "double"),
    Field("data_venda", "datetime", default=request.now, requires=IS_DATE(format='%d/%m/%Y %H:%M:%S'))
    )

db.define_table("produto_vendas",
    Field("vendas", "reference vendas"),
    Field("produtos", "reference produtos"),
    Field("quantidade", "double"),
    Field("valor_pago", "double")
    )
db.define_table("contato",
    Field("nome", 'string'),
    Field("email", 'string', requires=IS_EMAIL()),
    Field("mensagem", 'text')
    )

db.define_table('funcionarios',
    Field("nome", "string"),
    Field("cpf", "string"),
    Field("telefone_residencial", "string"),
    Field("telefone_celular", "string"),
    Field("email", "string"),
    Field("salario", "double"),
    Field("cargo", "string", requires=IS_IN_SET(["Atendente", "Gerente"])),
    Field("conta", "reference auth_user", label="Conta de acesso ao site do Funcionário", requires=IS_EMPTY_OR(IS_IN_DB(db, db.auth_user, "%(id)s - %(first_name)s %(last_name)s"))),
    )