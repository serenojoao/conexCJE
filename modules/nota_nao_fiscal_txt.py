# -*- coding: utf-8 -*-
from em_reais import em_reais
class CupomNaoFiscal():
    def __init__(self):
        self.linhas=[]
        self.total=0.0
        self.valor_pago=0.0
        self.troco=0.0
        self.desconto=0.0
        self.numero_documento="ID: 0000000000"
        self.data = "00/00/0000 00:00:00"
        self.linha_cliente=""
    def setData(self, data):
        self.data=data

    def setCodigo(self, codigo):
        self.numero_documento = "ID: "+str(int(codigo)).zfill(10)

    def setCliente(self, lista):
        nome = lista[0]
        cpf = str(lista[1])
        validos=['0','1','2','3','4','5','6','7','8','9']
        apenas_numeros=""
        for x in cpf:
            if x in validos:
                apenas_numeros="".join([apenas_numeros, x])
        apenas_numeros = apenas_numeros.zfill(11)
        apenas_numeros = "".join([
            apenas_numeros[:3],
            ".",
            apenas_numeros[3:6],
            ".",
            apenas_numeros[6:9],
            "-",
            apenas_numeros[9:]
            ])
        linha=self.centralizar("CLIENTE (Nome/CPF)")+"\n"
        linha+=self.create_lines()+"\n"
        linha+=self.alinhar_esquerda(nome, 25)+" "
        linha+=self.alinhar_direita(apenas_numeros, 14)+"\n"
        linha+=self.create_lines(caractere="=")+"\n\n"
        self.linha_cliente = linha

    def addLinha(self, valor):
        self.linhas.append(valor)

    def centralizar(self, texto, colunas=40, caractere=" "):
        largura = len(str(texto))
        compensador=""
        if largura >  colunas:
            texto = texto[0:colunas-3]+"..."
        elif largura < colunas-1:
            q_compensador = (colunas-largura)//2
            compensador = caractere*q_compensador
        return compensador+texto+compensador
    def alinhar_esquerda(self, texto, colunas=40, caractere=" "):
        largura = len(str(texto))
        compensador=""
        if largura >  colunas:
            texto = texto[0:colunas-3]+"..."
        elif largura < colunas-1:
            q_compensador = colunas-largura
            compensador = caractere*q_compensador
        return texto+compensador
    def alinhar_direita(self, texto, colunas=40, caractere=" "):
        largura = len(str(texto))
        compensador=""
        if largura >  colunas:
            texto = texto[0:colunas-3]+"..."
        elif largura < colunas-1:
            q_compensador = colunas-largura
            compensador = caractere*q_compensador
        return compensador+texto     

    def create_lines(self, colunas=40, caractere="-"):
        return caractere*40

    def create(self):
        texto=""
        texto+=self.create_lines()+"\n"
        texto+=self.centralizar("CUPOM NAO FISCAL")+"\n"
        texto+=self.centralizar("JE Informática")+"\n"
        texto+=self.create_lines(caractere="=")+"\n"
        texto+=self.alinhar_esquerda(self.numero_documento, 19)+" "
        texto+=self.alinhar_direita(self.data, 20)+"\n"
        texto+=self.create_lines(caractere="=")+"\n"
        texto+="\n"
        texto+=self.linha_cliente
        texto+=self.alinhar_esquerda("DESCRIÇÃO DO PRODUTO", 40)+"\n"
        texto+=self.alinhar_esquerda("ORDEM", 7)
        texto+=self.alinhar_esquerda("CÓDIGO DE BARRAS", 29)+"\n"
        texto+=self.alinhar_esquerda("PREÇO(R$)", 14)
        texto+=" "+self.centralizar("QUANTIDADE", 10)+" "
        texto+=self.alinhar_direita("SUBTOTAL(R$)", 14)
        texto+="\n"
        texto+=self.create_lines(caractere="-")+"\n"
        for x in self.linhas:
            texto+=self.alinhar_esquerda(str(x[0]), 40)+"\n"
            texto+=self.alinhar_esquerda(str(x[1]), 7)
            texto+=self.alinhar_esquerda(str(x[2]), 29)+"\n"
            texto+=self.alinhar_esquerda("%s" %(em_reais(float(x[3]))), 14)
            texto+=" "+self.centralizar("%.4f" %(x[4]), 10)+" "
            texto+=self.alinhar_direita("%s" %(em_reais(float(x[5]))), 14)
            texto+="\n\n"            
        texto+=self.create_lines(caractere="=")+"\n"
        texto+=self.alinhar_direita("TOTAL %s" %em_reais(float(self.total)), 40)+"\n"
        texto+=self.alinhar_direita("DESCONTO %s" %em_reais(float(self.desconto)), 40)+"\n"
        texto+=self.alinhar_direita("VALOR PAGO %s" %em_reais(float(self.valor_pago)), 40)+"\n"
        texto+=self.alinhar_direita("TROCO %s" %em_reais(float(self.troco)), 40)+"\n"
        return texto

    def setTotal(self, total):
        self.total = total

    def setValorPago(self, total):
        self.valor_pago = total

    def setTroco(self, total):
        self.troco = total

    def setDesconto(self, desconto):
        self.desconto = desconto

if __name__ == '__main__':
    teste = CupomNaoFiscal()
    teste.addLinha(["Sabonete bru bru","001","09876543211234", 14.55, 1.0, 14.55])
    teste.addLinha(["Carvao Vegetal","002","09476543211234", 0.55, 2.0, 1.10])
    teste.total = 12.5
    print(teste.create())