# -*- coding: utf-8 -*-

db.define_table("categorias",
    Field("categoria")
    )
db.define_table("unidades",
    Field("unidade", 'string'),
    format="%(unidade)s"
    )

db.define_table("sobre",
    Field('html', 'text'),
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
    Field("cep", "string"),
    format="%(id)s - %(nome)s (%(cnpj)s)"
    )

db.define_table("produtos",
    Field('id_imagem', 'reference plugin_phanterimages_uploads', label="id_imagem"),
    Field('cod_barra', 'string'),
    Field("produto", "string"),
    Field("descricao", "text", label="Descrição"),
    Field("quantidade", "double", default=0),
    Field("unidades", "reference unidades"),
    Field("preco_final", "double", default=0, label="Preço Final"),
    Field("disponivel", "boolean", default=True, label="Disponível"),
    format="%(id)s - %(produto)s"
    )

db.define_table("categorias_produtos",
    Field("categorias", "reference categorias"),
    Field("produtos", "reference produtos")
    )

db.define_table("fornecedores_produtos",
    Field("quantidade", "double", default=0),
    Field("preco_custo", "double", default=0, label="Preço de Custo"),
    Field("fornecedores", "reference fornecedores", requires=IS_IN_DB(db, db.fornecedores, "%(id)s - %(nome)s")),
    Field("produtos", "reference produtos", requires=IS_IN_DB(db, db.produtos, "%(id)s - %(produto)s"))
    )
db.fornecedores_produtos.quantidade.requires=IS_FLOAT_IN_RANGE(0.0000000001, None, dot=".", error_message='Tem que ser maior que ZERO')

db.define_table("carrinho",
    Field("produtos", "reference produtos"),
    Field("quantidade", "double", default=1),
    auth.signature
    )

db.define_table("clientes",
    Field("nome", "string"),
    Field("cpf", "string", label="CPF"),
    Field("data_de_nascimento", "date", label="Data de Nascimento", requires=IS_DATE(format='%d/%m/%Y')),
    Field("telefone_residencial", "string"),
    Field("telefone_celular", "string"),
    Field("email", "string"),
    format="%(id)s - %(nome)s"
    )


db.define_table('funcionarios',
    Field("nome", "string"),
    Field("cpf", "string", label="CPF"),
    Field("data_de_nascimento", "date", label="Data de Nascimento", requires=IS_DATE(format='%d/%m/%Y')),
    Field("telefone_residencial", "string"),
    Field("telefone_celular", "string"),
    Field("email", "string"),
    Field("salario", "double", label="Salário"),
    Field("cargo", "string", requires=IS_IN_SET(["Atendente", "Gerente"])),
    Field("conta", "reference auth_user", label="Conta de acesso ao site do Funcionário", requires=IS_EMPTY_OR(IS_IN_DB(db, db.auth_user, "%(id)s - %(first_name)s %(last_name)s"))),
    format="%(id)s - %(nome)s",
    )

db.define_table("vendas",
    Field('vendedor', 'reference funcionarios', requires=IS_IN_DB(db, db.funcionarios, "%(id)s - %(nome)s")),
    Field("cliente", "reference clientes", requires=IS_EMPTY_OR(IS_IN_DB(db, db.clientes, "%(id)s - %(nome)s"))),
    Field("total", "double", default=0.0),
    Field("desconto", "double", default=0.0),
    Field("valor_pago", "double", default=0.0),
    Field("troco", "double", default=0.0),
    Field("data_venda", "datetime", default=request.now, requires=IS_DATE(format='%d/%m/%Y %H:%M:%S')),
    Field("data_venda_finalizada", "datetime", requires=IS_EMPTY_OR(IS_DATE(format='%d/%m/%Y %H:%M:%S'))),
    Field("aberta", default=True),
    )

db.define_table("produto_vendas",
    Field("vendas", "reference vendas"),
    Field("produtos", "reference produtos"),
    Field("quantidade", "double"),
    Field("valor_pago", "double"),
    Field("ordem", "integer")
    )
db.define_table("contato",
    Field("nome", 'string'),
    Field("email", 'string', requires=IS_EMAIL()),
    Field("mensagem", 'text'),
    Field("visto", "boolean", default=False)
    )
