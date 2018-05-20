# -*- coding: utf-8 -*-
def em_reais(numero):
    if isinstance(numero,(float, int)):
        final=str("%0.2f" %numero).replace(".",",")
        p_inteiro, p_decimal=final.split(",")
        inicio=0
        final=inicio-3
        parte=p_inteiro[final:]
        partes=[parte]
        while len(parte)==3:
            inicio=inicio-3
            final=inicio-3
            parte=p_inteiro[final:inicio]
            if parte:
                partes.append(parte)
        
        numero="".join(["R$ ", ",".join([".".join(partes[::-1]),p_decimal])])
        return numero
    else:
        try:
            numero=float(numero)
        except:
            raise "O valor tem que ser um número válido"
if __name__ == '__main__':
    print em_reais(100000000000.60)