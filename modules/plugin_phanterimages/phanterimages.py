# -*- coding: utf-8 -*-
import os


from gluon.html import *
from gluon import current
from PIL import Image as PilImage
import cStringIO
import base64
import json
from remover_acentos import remover_acentos

class PhanterImages(object):
    url_ajax=URL("plugin_phanterimages", "echo_phanterimages")
    def __init__ (self, db, tamanho_corte=(300, 300), url_ajax=url_ajax, **kargs):
        """
            A classe PhanterImages cria um botão de upload que permite via ajax fazer o upload de até multiplas
            imagens, com a opção de cortar antes do armazenamento final. Para seu devido funcionamento é necessário
            definir uma tabela temporária e uma tabela destino para as imagens, ambos na mesma instância db
            @controller: Controler onde estará a função echoPhanterimages responsável pelo upload, corte, etc...
            @multiplo: permite a escolha de multiplas imagens para multiplos uploads. Esta opção será False
        quando for definido um tamanho de corte em tamanho_corte, ou seja, mesmo que esteja True.
            @tamanho_corte: tupla ou lista com o tamanho da largura e altura em pixels do corte. Exemplo.: tamanho_corte=(300,400)
            @tipos_imagens: tipos de imagens permitidas no upload, por padrão são 4, jpg, bmp, gif e png.

        """
        self.url_ajax=url_ajax
        self.kargs=kargs
        self.callbackOnCut="console.log(response);"
        self.db=db
        self.tamanho_corte=tamanho_corte
        self.tipos_imagens=['png', 'jpg', 'gif', 'bmp']
        dict_tipos_imagens={'png':"image/png",
                            'jpg':"image/jpeg",
                            'gif':"image/gif",
                            'bmp':"image/bmp"}
        self.tipos=None
        cont=0
        for x in self.tipos_imagens:
            if x in dict_tipos_imagens:
                if cont==0:
                    self.tipos=dict_tipos_imagens[x]
                else:
                    self.tipos=", ".join([self.tipos, dict_tipos_imagens[x]])
                cont+=1

        self._mapa_script={
            'url':url_ajax
            }
        if '_id' in kargs:
            self._mapa_script['id_input']="-".join(["plugin_phanterimages_upload-area", kargs['_id']])
        else:
            kargs['_id']="plugin_phanterimages_upload-area"
            self._mapa_script['id_input']="-".join(["plugin_phanterimages_upload-area","input"])
        
        self._id_painel_corte="-".join([kargs['_id'],"painel-corte"])
        self._id_alvo_upload="-".join([kargs['_id'],"alvo-upload"])
        self._id_barra_progresso="-".join([kargs['_id'],"barra-de-progesso"])
        self._mapa_script['id_barra_progresso']=self._id_barra_progresso
        self.nome_do_botao="Upload"
        self.texto_lendo="Fazendo Upload"

        self.html_botao=""
        self.icone_fechar="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <g>
            <metadata/>
            <path class="plugin_phanterimages-icone-fechar plugin_phanterimages-cinza" d="M26.0257 2.4c12.8518,0 23.2741,10.4224 23.2741,23.2741 0,12.8518 -10.4224,23.2741 -23.2741,23.2741 -12.8518,0 -23.2741,-10.4224 -23.2741,-23.2741 0,-12.8518 10.4224,-23.2741 23.2741,-23.2741zm-17.0163 31.4963l8.45663 -8.45665 -8.45663 -8.45665 8.2079 -8.2079 8.45665 8.45663 8.45665 -8.45663 8.2079 8.2079 -8.45663 8.45665 8.45663 8.45665 -8.2079 8.2079 -8.45665 -8.45662 -8.45665 8.45662 -8.2079 -8.2079z"/>
            <path class="plugin_phanterimages-icone-fechar plugin_phanterimages-branco plugin_phanterimages-botao-icone" d="M25.5276 2.2535c12.8518,0 23.2741,10.4224 23.2741,23.2741 0,12.8518 -10.4223,23.2741 -23.2741,23.2741 -12.8518,0 -23.2741,-10.4223 -23.2741,-23.2741 0,-12.8518 10.4224,-23.2741 23.2741,-23.2741zm-17.0163 31.4963l8.45663 -8.45665 -8.45663 -8.45665 8.2079 -8.2079 8.45665 8.45663 8.45665 -8.45663 8.2079 8.2079 -8.45662 8.45665 8.45662 8.45665 -8.2079 8.2079 -8.45665 -8.45663 -8.45665 8.45663 -8.2079 -8.2079z"/>
            </g>
            </svg>
        """
        self.icone_visualizar="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink">
            <g>
            <metadata/>
            <path class="plugin_phanterimages-icone-visualizar plugin_phanterimages-cinza" d="M2.7807 15.7311l12.6334 0c0.72175,0.92215 1.5463,1.80063 2.4108,2.59807l-12.4348 0 0 27.5228 34.0236 0 0 -22.9078c0.891375,-0.315725 1.76225,-0.69255 2.60947,-1.12875l0 26.6346 -39.2426 0 0 -32.7189zm19.7982 0l0.619 0c0.058625,0.18215 0.122575,0.362225 0.19165,0.5401 -0.2746,-0.173425 -0.544975,-0.3535 -0.81065,-0.5401zm5.56188 0l0.396175 0c0.898575,1.1787 2.31717,1.9398 3.913,1.9398 1.59587,0 3.01435,-0.7611 3.91293,-1.9398l0.39625 0c-0.945475,1.36543 -2.5228,2.26013 -4.30918,2.26013 -1.78632,0 -3.3637,-0.8947 -4.30917,-2.26013zm13.5612 0l0.32135 0 0 0.1415c-0.159375,0.108925 -0.320225,0.21565 -0.482725,0.3199 0.0576,-0.152225 0.111375,-0.30605 0.161375,-0.4614zm-28.6103 6.94713c1.6349,0 2.9608,1.32585 2.9608,2.96077 0,1.63488 -1.3259,2.96075 -2.9608,2.96075 -1.63485,0 -2.96075,-1.32587 -2.96075,-2.96075 0,-1.63492 1.3259,-2.96077 2.96075,-2.96077zm13.3627 4.69517l5.97793 8.48082 5.97795 8.48083 -11.9559 0 -1.32375 0 -10.6321 0 -7.30175 0 4.4834 -6.3606 4.48348 -6.36063 3.65077 5.1795 0.661975 -0.9391 5.97792 -8.48082zm5.99563 -18.1286c1.93727,0 3.5084,1.5711 3.5084,3.5084 0,1.93722 -1.57113,3.50832 -3.5084,3.50832 -1.93722,0 -3.50832,-1.5711 -3.50832,-3.50832 0,-1.9373 1.5711,-3.5084 3.50832,-3.5084zm-0.0923 -6.27748c-9.48255,0 -15.7365,7.9206 -17.1726,9.8788 1.75418,3.23922 7.69,9.87885 17.1726,9.87885 0.030875,0 0.061475,-0.000525 0.0923,-0.000625 9.48258,0 15.4184,-6.63963 17.1726,-9.8789 -1.436,-1.95823 -7.69,-9.8788 -17.1726,-9.8788 -0.023725,0 -0.0473,0.000475 -0.070775,0.000675l-2.5e-005 0 -0.001375 0 -2.5e-005 0 -0.0014 0 -2.5e-005 0 -0.0014 0 0 0 -0.0015 0 -5e-005 0 -0.0014 0 -2.5e-005 0 -0.00135 0 -5e-005 0 -0.001375 0 -5e-005 0 -0.001525 0 -2.5e-005 0 -0.00135 0 -5e-005 0 -0.0014 0 -5e-005 0 -0.00135 0 -2.5e-005 0 -0.001425 0 -0.00145 0 -0.001375 0 -0.00145 0zm5.7946 3.74298c1.60495,1.5151 2.60703,3.66212 2.60703,6.0429 0,3.11037 -1.71033,5.82157 -4.24128,7.24585 5.6538,-1.64305 9.26288,-5.08183 10.5654,-7.01495 -0.96435,-1.05697 -4.10247,-4.27415 -8.93112,-6.2738zm-9.67088 13.3443c-2.5856,-1.40863 -4.34067,-4.1504 -4.34067,-7.30143 0,-2.41585 1.0319,-4.59095 2.67847,-6.1094 -4.92162,1.99397 -8.11965,5.2721 -9.09488,6.34095 1.31715,1.9549 4.99305,5.4497 10.7571,7.06988zm3.96858 -13.9489c3.67063,0 6.64748,2.97685 6.64748,6.64748 0,3.67055 -2.97685,6.64738 -6.64748,6.64738 -3.67055,0 -6.6474,-2.97683 -6.6474,-6.64738 0,-3.67063 2.97685,-6.64748 6.6474,-6.64748z"/>
            <path class="plugin_phanterimages-icone-visualizar plugin_phanterimages-branco plugin_phanterimages-botao-icone" d="M2.0894 15.155l12.6335 0c0.721725,0.92215 1.54627,1.80062 2.41077,2.59807l-12.4348 0 0 27.5228 34.0236 0 0 -22.9078c0.891375,-0.315725 1.76225,-0.69255 2.60948,-1.12875l0 26.6346 -39.2426 0 0 -32.7189zm19.7982 0l0.619025 0c0.0586,0.18215 0.12255,0.362225 0.191625,0.5401 -0.2746,-0.173425 -0.544975,-0.3535 -0.81065,-0.5401zm5.56188 0l0.3962 0c0.89855,1.1787 2.31715,1.9398 3.913,1.9398 1.59588,0 3.01435,-0.7611 3.9129,-1.9398l0.39625 0c-0.945475,1.36543 -2.5228,2.26013 -4.30915,2.26013 -1.78632,0 -3.3637,-0.8947 -4.3092,-2.26013zm13.5612 0l0.32135 0 0 0.1415c-0.159375,0.108925 -0.320225,0.21565 -0.482725,0.3199 0.0576,-0.152225 0.111375,-0.306075 0.161375,-0.4614zm-28.6103 6.94713c1.6349,0 2.9608,1.32585 2.9608,2.96077 0,1.63488 -1.3259,2.96075 -2.9608,2.96075 -1.63485,0 -2.96075,-1.32587 -2.96075,-2.96075 0,-1.63492 1.3259,-2.96077 2.96075,-2.96077zm13.3627 4.69517l5.9779 8.48082 5.97795 8.4808 -11.9558 0 -1.32375 0 -10.6321 0 -7.30175 0 4.4834 -6.36057 4.48348 -6.36063 3.6508 5.1795 0.66195 -0.9391 5.97795 -8.48082zm5.99563 -18.1286c1.93725,0 3.5084,1.5711 3.5084,3.5084 0,1.93722 -1.57115,3.50832 -3.5084,3.50832 -1.93725,0 -3.50835,-1.5711 -3.50835,-3.50832 0,-1.9373 1.5711,-3.5084 3.50835,-3.5084zm-0.092325 -6.27747c-9.48253,0 -15.7365,7.9206 -17.1726,9.8788 1.75418,3.23922 7.69002,9.87885 17.1726,9.87885 0.030875,0 0.0615,-0.000525 0.092325,-0.000625 9.48255,0 15.4184,-6.63965 17.1726,-9.8789 -1.43597,-1.95823 -7.69,-9.8788 -17.1726,-9.8788 -0.023725,0 -0.047325,0.000475 -0.0708,0.000675l-2.5e-005 0 -0.00135 0 -5e-005 0 -0.001375 0 -2.5e-005 0 -0.0014 0 -2.5e-005 0 -0.0015 0 -5e-005 0 -0.0014 0 -2.5e-005 0 -0.00135 0 -5e-005 0 -0.001375 0 -5e-005 0 -0.001525 0 -2.5e-005 0 -0.00135 0 -5e-005 0 -0.0014 0 -5e-005 0 -0.00135 0 -2.5e-005 0 -0.001425 0 -0.00145 0 -0.001375 0 -0.00145 0zm5.7946 3.74298c1.60495,1.5151 2.60705,3.66212 2.60705,6.0429 0,3.11037 -1.71033,5.82157 -4.2413,7.24585 5.6538,-1.64305 9.26288,-5.08183 10.5654,-7.01498 -0.96435,-1.05695 -4.10247,-4.27415 -8.93112,-6.27377zm-9.67088 13.3443c-2.5856,-1.40863 -4.34068,-4.1504 -4.34068,-7.30142 0,-2.41585 1.0319,-4.59095 2.67847,-6.1094 -4.92162,1.99397 -8.11965,5.2721 -9.09487,6.34095 1.31717,1.9549 4.99305,5.4497 10.7571,7.06987zm3.9686 -13.9489c3.6706,0 6.64745,2.97685 6.64745,6.64748 0,3.67055 -2.97685,6.64738 -6.64745,6.64738 -3.67057,0 -6.64742,-2.97683 -6.64742,-6.64738 0,-3.67063 2.97685,-6.64748 6.64742,-6.64748z"/>
            </g>
            </svg>
        """
        self.icone_cortar="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <g>
            <metadata/>
            <path class="plugin_phanterimages-icone-cortar plugin_phanterimages-cinza" d="M2.67005 15.5113l25.4835 0c-0.4697,0.76165 -0.938425,1.52383 -1.40645,2.2865 -0.85155,0.1104 -1.7032,0.220575 -2.55475,0.330775l-18.8935 0 0 27.7267 34.2757 0 0 -16.6746c0.85485,0.233675 1.7478,0.3432 2.6288,0.32865l0 18.9632 -39.5333 0 0 -32.9613zm34.7325 0l4.80083 0 0 0.2612 -0.19365 0.02575c-0.1262,0.00685 -0.25225,0.016175 -0.378075,0.02805 -0.368175,0.034775 -0.734275,0.090625 -1.09593,0.167575 -1.24662,0.165125 -2.49332,0.329525 -3.74012,0.49335l0.60695 -0.975925zm4.80083 6.4433l0 1.39258c-0.399275,-0.00625 -1.05602,-0.163425 -1.09615,-0.58855 -0.045025,-0.4764 0.732675,-0.76705 1.09615,-0.804025zm-26.6068 5.1028c-0.52545,0.8507 -1.46615,1.41787 -2.53925,1.41787 -0.80105,0 -1.52842,-0.31605 -2.0643,-0.830075 1.53412,-0.19925 3.0687,-0.394775 4.60355,-0.5878zm12.8436 2.90787l4.1011 5.81822 6.02223 8.54365 -12.0444 0 -1.33355 0 -10.7108 0 -7.35585 0 4.51665 -6.40772 4.51667 -6.40772 1.18198 1.6769c-0.93245,1.5129 -1.86823,3.02375 -2.8092,4.5316 -0.3819,0.612 -0.695175,1.2357 -0.428825,1.97815 0.2866,0.798875 0.97915,1.04715 1.69592,1.3063 2.86003,1.03402 6.18995,-0.60055 7.72383,-3.07953 1.64163,-2.65315 3.28268,-5.3067 4.92432,-7.95985zm20.4609 -7.94257c0.2819,2.98645 -2.4562,5.68848 -6.11465,6.03393 -3.65837,0.345475 -6.85405,-1.79628 -7.13597,-4.78288 -0.004425,-0.0467 -0.008025,-0.093325 -0.010975,-0.139875 -1.72635,0.22335 -3.39738,0.435025 -5.03595,0.639775 -2.83028,4.56865 -5.6608,9.14718 -8.295,13.4044 -0.986825,1.59488 -3.55725,3.38672 -6.0337,2.49137 -0.977775,-0.353525 -1.05627,-0.3788 -0.54535,-1.19755 3.1421,-5.03502 5.83725,-9.46237 8.55348,-13.9186 -5.1801,0.634025 -10.3253,1.26065 -16.2085,2.04355 -0.95665,0.1273 -0.94725,0.045375 -0.86555,-0.99115 0.207025,-2.6252 2.9003,-4.22645 4.76032,-4.46675 4.96502,-0.64145 10.3038,-1.32895 15.6334,-2.02042 0.863025,-1.40785 1.74573,-2.84248 2.66193,-4.32257 -0.041175,-0.0219 -0.08215,-0.04445 -0.122875,-0.06775 -2.60373,-1.4899 -3.23497,-5.28478 -1.40982,-8.4741 1.82515,-3.18945 5.41663,-4.56762 8.02025,-3.07785 2.4205,1.38507 3.13593,4.76197 1.75838,7.79272 0.0121,0.006975 0.024475,0.013625 0.036225,0.0211l-0.20585 0.32995c-0.05675,0.11075 -0.116325,0.220925 -0.178925,0.330325 -0.168125,0.2938 -0.35135,0.5721 -0.5473,0.834325 -1.17635,1.8875 -2.38423,3.83007 -3.60725,5.79992 2.2991,-0.3006 4.56703,-0.5987 6.77183,-0.890775 0.31975,-0.0702 0.64885,-0.122175 0.985875,-0.154 0.125475,-0.01185 0.250425,-0.0206 0.374725,-0.02655l0.3855 -0.051275c0.001975,0.0138 0.0029,0.027825 0.004275,0.041725 3.3291,-0.0033 6.10938,2.04255 6.37145,4.81898zm-19.0063 -0.957525c0.329625,0.51135 0.18225,1.19335 -0.3291,1.52297 -0.511325,0.329625 -1.19332,0.18225 -1.52295,-0.3291 -0.329625,-0.511325 -0.18225,-1.19332 0.329075,-1.52295 0.51135,-0.329625 1.19335,-0.18225 1.52297,0.329075zm4.8403 -14.3639c-1.01475,-0.5808 -2.4144,-0.0436 -3.1258,1.1994 -0.7112,1.24295 -0.4652,2.72192 0.549425,3.30255 1.01475,0.5808 2.4144,0.0436 3.1258,-1.1994 0.7112,-1.24295 0.465225,-2.72192 -0.549425,-3.30255zm10.1227 15.7031c0.110025,1.16403 -0.95715,2.217 -2.38298,2.3517 -1.4257,0.134575 -2.67115,-0.700125 -2.78105,-1.86397 -0.110025,-1.16402 0.95715,-2.217 2.38298,-2.35173 1.4257,-0.13455 2.67115,0.700125 2.78105,1.864z"/>
            <path class="plugin_phanterimages-icone-cortar plugin_phanterimages-branco plugin_phanterimages-botao-icone" d="M48.1976 21.5537c0.281875,2.98643 -2.45622,5.68845 -6.11467,6.03395 -3.65837,0.34545 -6.85403,-1.7963 -7.13598,-4.78288 -0.0044,-0.0467 -0.00805,-0.09335 -0.01095,-0.139875 -1.72637,0.22335 -3.3974,0.435 -5.03597,0.639775 -2.83028,4.56863 -5.6608,9.14715 -8.29503,13.4044 -0.9868,1.59485 -3.55722,3.38675 -6.0337,2.49138 -0.97775,-0.353525 -1.05625,-0.3788 -0.545325,-1.19755 3.14213,-5.03502 5.83723,-9.4624 8.55348,-13.9186 -5.1801,0.634025 -10.3253,1.26063 -16.2084,2.04352 -0.9567,0.127325 -0.947275,0.045375 -0.865575,-0.9911 0.207025,-2.62523 2.9003,-4.22648 4.76033,-4.46677 4.96505,-0.64145 10.3038,-1.32895 15.6334,-2.02043 0.863025,-1.40785 1.7457,-2.84247 2.6619,-4.3226 -0.041175,-0.021875 -0.08215,-0.044425 -0.122875,-0.067725 -2.60373,-1.48992 -3.23495,-5.28475 -1.40983,-8.4741 1.82512,-3.18943 5.41662,-4.56763 8.02022,-3.07783 2.4205,1.38502 3.13593,4.76192 1.75838,7.79267 0.012125,0.007 0.0245,0.01365 0.03625,0.021125l-0.205875 0.329925c-0.0567,0.1108 -0.1163,0.220975 -0.178875,0.330375 -0.16815,0.2938 -0.35135,0.572075 -0.547325,0.8343 -1.17632,1.88753 -2.3842,3.83005 -3.60722,5.79993 2.29905,-0.3006 4.567,-0.5987 6.7718,-0.890775 0.31975,-0.0702 0.648875,-0.1222 0.98585,-0.154 0.1255,-0.011825 0.250425,-0.020625 0.37475,-0.02655l0.385475 -0.05125c0.001975,0.013775 0.00295,0.0278 0.004275,0.0417 3.32912,-0.0033 6.10938,2.04255 6.3715,4.81898zm-19.0063 -0.957525c0.3296,0.51135 0.182225,1.19333 -0.329075,1.52297 -0.51135,0.329625 -1.19335,0.18225 -1.52298,-0.3291 -0.329625,-0.511325 -0.18225,-1.19333 0.3291,-1.52295 0.511325,-0.329625 1.19333,-0.18225 1.52295,0.329075zm4.8403 -14.3639c-1.01478,-0.580825 -2.41443,-0.043625 -3.12578,1.19937 -0.711225,1.24292 -0.465225,2.72193 0.5494,3.30255 1.01473,0.580775 2.41437,0.0436 3.1258,-1.1994 0.711225,-1.24295 0.4652,-2.72193 -0.549425,-3.30253zm10.1227 15.7031c0.109975,1.16405 -0.957175,2.21702 -2.383,2.35177 -1.4257,0.1345 -2.67115,-0.700175 -2.78105,-1.86403 -0.110025,-1.16402 0.95715,-2.21702 2.38295,-2.3517 1.42572,-0.134575 2.67117,0.700125 2.7811,1.86395zm-42.1877 -6.89305l25.4835 0c-0.469725,0.76165 -0.93845,1.52383 -1.40647,2.28648 -0.851525,0.110425 -1.7032,0.2206 -2.55475,0.3308l-18.8935 0 0 27.7267 34.2757 0 0 -16.6746c0.85485,0.2337 1.7478,0.3432 2.6288,0.328675l0 18.9632 -39.5333 0 0 -32.9613zm34.7325 0l4.8008 0 0 0.261175 -0.19365 0.025775c-0.1262,0.006825 -0.25225,0.016175 -0.37805,0.028025 -0.3682,0.034775 -0.7343,0.09065 -1.09595,0.167575 -1.24663,0.16515 -2.49335,0.32955 -3.74012,0.493375l0.606975 -0.975925zm4.8008 6.44332l0 1.39255c-0.399275,-0.006275 -1.056,-0.163425 -1.09615,-0.588575 -0.045025,-0.476375 0.732675,-0.767025 1.09615,-0.803975zm-26.6068 5.10278c-0.52545,0.8507 -1.46612,1.4179 -2.53927,1.4179 -0.801025,0 -1.52838,-0.316075 -2.06428,-0.8301 1.53412,-0.199275 3.0687,-0.394775 4.60355,-0.5878zm12.8435 2.9079l4.10112 5.81818 6.02222 8.54368 -12.0444 0 -1.33355 0 -10.7109 0 -7.35585 0 4.51662 -6.4077 4.5167 -6.40775 1.18198 1.67693c-0.93245,1.51288 -1.86823,3.02375 -2.8092,4.53157 -0.381925,0.612025 -0.69515,1.2357 -0.42885,1.97815 0.286625,0.79885 0.97915,1.04715 1.69593,1.3063 2.86005,1.03402 6.18995,-0.60055 7.72383,-3.07952 1.64167,-2.65315 3.2827,-5.30667 4.92432,-7.95983z"/>
            </g>
            </svg>
        """
        self.icone_aumentar="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="25px" height="25px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 25 25"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <g>
            <metadata/>
            <path class="plugin_phanterimages-resize-aumentar plugin_phanterimages-preto" d="M0.528325 0.704187l5.33004 0 -2.23099 2.23099 2.23099 2.23099 0 0.95345 -0.95345 0 -2.23099 -2.23099 -2.1456 2.1456 0 -5.33004zm23.9984 0l-5.33004 0 2.23099 2.23099 -2.23099 2.23099 0 0.95345 0.95345 0 2.23099 -2.23099 2.1456 2.1456 0 -5.33004zm0 24.1692l-5.33004 0 2.23099 -2.23099 -2.23099 -2.23099 0 -0.95345 0.95345 0 2.23099 2.23099 2.1456 -2.1456 0 5.33004zm-23.9984 0l5.33004 0 -2.23099 -2.23099 2.23099 -2.23099 0 -0.95345 -0.95345 0 -2.23099 2.23099 -2.1456 -2.1456 0 5.33004zm6.40421 -6.48961l11.19 0 0 -11.19 -11.19 0 0 11.19zm-0.915437 0.915437l13.0209 0 0 -13.0209 -13.0209 0 0 13.0209zm3.91202 -10.724c0.919913,0 1.66595,0.746025 1.66595,1.66595 0,0.919875 -0.746037,1.66589 -1.66595,1.66589 -0.919862,0 -1.66591,-0.746012 -1.66591,-1.66589 0,-0.919925 0.74605,-1.66595 1.66591,-1.66595zm4.43246 2.03993l3.50132 7.27025 -4.05855 0 -0.449362 0 -3.60916 0 -2.47865 0 2.36728 -4.55717 1.91591 1.99705 0.224712 -0.318775 2.5865 -4.39135z"/>
            </g>
            </svg>
        """
        self.icone_diminuir="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="25px" height="25px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 25 25"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <g>
            <metadata/>
            <path class="plugin_phanterimages-resize-diminuir plugin_phanterimages-preto" d="M14.3616 10.6152l3.50132 7.27025 -4.05855 0 -0.449362 0 -3.60916 0 -2.47865 0 2.36728 -4.55717 1.91591 1.99705 0.224712 -0.318775 2.5865 -4.39135zm-4.43246 -2.03993c0.919913,0 1.66595,0.746025 1.66595,1.66595 0,0.919875 -0.746037,1.66589 -1.66595,1.66589 -0.919862,0 -1.66591,-0.746012 -1.66591,-1.66589 0,-0.919925 0.74605,-1.66595 1.66591,-1.66595zm-3.91202 10.724l13.0209 0 0 -13.0209 -13.0209 0 0 13.0209zm0.915437 -0.915437l11.19 0 0 -11.19 -11.19 0 0 11.19zm-1.07419 1.07419l-5.33004 0 2.23099 2.23099 -2.23099 2.23099 0 0.95345 0.95345 0 2.23099 -2.23099 2.1456 2.1456 0 -5.33004zm13.3384 0l5.33004 0 -2.23099 2.23099 2.23099 2.23099 0 0.95345 -0.95345 0 -2.23099 -2.23099 -2.1456 2.1456 0 -5.33004zm0 -13.3384l5.33004 0 -2.23099 -2.23099 2.23099 -2.23099 0 -0.95345 -0.95345 0 -2.23099 2.23099 -2.1456 -2.1456 0 5.33004zm-13.3384 0l-5.33004 0 2.23099 -2.23099 -2.23099 -2.23099 0 -0.95345 0.95345 0 2.23099 2.23099 2.1456 -2.1456 0 5.33004z"/>
            </g>
            </svg>
        """
        self.botao_simples="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="25px" height="25px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 25 25"
             xmlns:xlink="http://www.w3.org/1999/xlink">
             <g>
              <metadata/>
              <polygon class="plugin_phanterimages-icone-fechar-simples plugin_phanterimages-branco" points="1.6889,8.57921 8.27049,1.99762 12.7873,6.5144 17.3041,1.99762 23.8856,8.57921 19.3689,13.096 23.8856,17.6128 17.3041,24.1944 12.7873,19.6776 8.27049,24.1944 1.6889,17.6128 6.20567,13.096 "/>
              <polygon class="plugin_phanterimages-icone-fechar-simples plugin_phanterimages-preto plugin_phanterimages-botao-icone" points="1.38339,7.84772 7.96497,1.26614 12.4818,5.78291 16.9985,1.26614 23.5801,7.84772 19.0634,12.3645 23.5801,16.8813 16.9985,23.4629 12.4818,18.9461 7.96497,23.4629 1.38339,16.8813 5.90016,12.3645 "/>
             </g>
            </svg>
        """
        self.botao_upload="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50"
             xmlns:xlink="http://www.w3.org/1999/xlink">
             <g>
              <metadata/>
              <path class="plugin_phanterimages-icone-upload plugin_phanterimages-cinza" d="M30.2258 49.0363l0 -11.8596 4.44725 0 -8.8945 -11.8596 -8.89475 11.8596 4.44728 0 0 11.8596 8.89473 0zm-18.535 -15.7406c2.02332,0 3.90212,-0.5159 5.46185,-1.39878 0.114775,0.069675 0.230575,0.1386 0.348075,0.205325l8.27778 -11.0371 9.2794 12.3725 0.2134 0.0017c7.86005,0 14.234,-5.3431 14.234,-11.9314 0,-6.58833 -6.3739,-11.9314 -14.234,-11.9314 -0.340475,0 -0.678775,0.011275 -1.01312,0.030875 -2.08735,-3.91418 -6.77255,-6.6435 -12.2172,-6.6435 -7.38657,0 -13.3766,5.02128 -13.3766,11.2127 0,1.04283 0.171725,2.05325 0.48965,3.01145 -4.16808,0.936825 -7.2384,4.1249 -7.2384,7.91372 0,4.52453 4.37732,8.1939 9.77518,8.1939z"/>
              <path class="plugin_phanterimages-icone-upload plugin_phanterimages-gelo plugin_phanterimages-botao-icone" d="M29.4307 48.4302l0 -11.8595 4.44725 0 -8.8945 -11.8596 -8.89472 11.8596 4.44722 0 0 11.8595 8.89475 0zm-18.535 -15.7407c2.02332,0 3.9022,-0.515875 5.46185,-1.39872 0.114825,0.06965 0.230625,0.1386 0.3481,0.205325l8.2778 -11.0371 9.27938 12.3725 0.21345 0.001725c7.86,0 14.2339,-5.34315 14.2339,-11.9315 0,-6.5883 -6.3739,-11.9315 -14.2339,-11.9315 -0.340525,0 -0.678825,0.0113 -1.01317,0.030925 -2.08735,-3.91418 -6.77253,-6.64353 -12.2172,-6.64353 -7.38658,0 -13.3766,5.02127 -13.3766,11.2127 0,1.04283 0.171725,2.05328 0.48965,3.01145 -4.16807,0.93685 -7.2384,4.12493 -7.2384,7.91375 0,4.5245 4.37735,8.19385 9.77515,8.19385z"/>
             </g>
            </svg>
        """
        self.icone_lixeira="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50"
             xmlns:xlink="http://www.w3.org/1999/xlink">
             <g>
              <metadata/>
              <path class="plugin_phanterimages-icone-lixeira plugin_phanterimages-preto" d="M46.422 19.099l-3.54275 25.4634c-0.35805,2.57343 -2.75648,4.6789 -5.32985,4.6789l-0.8035 0 -22.2196 0 -0.803525 0c-2.57337,0 -4.9718,-2.10548 -5.32982,-4.6789l-3.54277 -25.4634 41.5719 0zm-37.5934 2.94073l0 0c0.69845,0 1.33935,0.5714 1.4243,1.26985l2.58485 21.2533c0.08495,0.698425 -0.416975,1.26985 -1.1154,1.26985l0 0c-0.69845,0 -1.33935,-0.571425 -1.4243,-1.26985l-2.58485 -21.2533c-0.084975,-0.69845 0.41695,-1.26985 1.1154,-1.26985zm6.79785 0c0,0 0,0 0,0 0.698425,0 1.31122,0.5714 1.36183,1.26985 0.51315,7.0844 1.02627,14.1689 1.53942,21.2533 0.0506,0.698425 -0.479425,1.26985 -1.17788,1.26985 0,0 0,0 0,0 -0.69845,0 -1.31123,-0.571425 -1.36182,-1.26985 -0.51315,-7.08445 -1.02628,-14.1689 -1.53945,-21.2533 -0.050575,-0.69845 0.47945,-1.26985 1.1779,-1.26985zm6.7978 0c0,0 0,0 0,0 0.698425,0 1.28312,0.5714 1.29937,1.26985 0.16465,7.0844 0.329325,14.1689 0.493975,21.2533 0.01625,0.698425 -0.541875,1.26985 -1.24033,1.26985 0,0 0,0 0,0 -0.69845,0 -1.28312,-0.571425 -1.29937,-1.26985 -0.16465,-7.08445 -0.329325,-14.1689 -0.493975,-21.2533 -0.01625,-0.69845 0.541875,-1.26985 1.24033,-1.26985zm6.79778 0c0,0 0,0 0,0 0.69845,0 1.25502,0.5714 1.2369,1.26985 -0.1838,7.0844 -0.367625,14.1689 -0.551425,21.2533 -0.0181,0.698425 -0.60435,1.26985 -1.3028,1.26985 0,0 0,0 0,0 -0.69845,0 -1.255,-0.571425 -1.2369,-1.26985 0.1838,-7.08445 0.367625,-14.1689 0.551425,-21.2533 0.018125,-0.69845 0.60435,-1.26985 1.3028,-1.26985zm6.7978 0c0,0 0,0 0,0 0.69845,0 1.22695,0.5714 1.17448,1.26985 -0.532325,7.0844 -1.0646,14.1689 -1.5969,21.2533 -0.05245,0.698425 -0.6668,1.26985 -1.36525,1.26985 0,0 0,0 0,0 -0.69845,0 -1.2269,-0.571425 -1.17445,-1.26985 0.5323,-7.08445 1.06458,-14.1689 1.5969,-21.2533 0.05245,-0.69845 0.6668,-1.26985 1.36522,-1.26985zm6.79783 0l0 0c0.698425,0 1.19882,0.5714 1.11198,1.26985l-2.6423 21.2533c-0.086825,0.698425 -0.729275,1.26985 -1.42772,1.26985l0 0c-0.698425,0 -1.1988,-0.571425 -1.11198,-1.26985l2.6423 -21.2533c0.08685,-0.69845 0.729275,-1.26985 1.42772,-1.26985zm-35.9012 -16.6852l12.348 0 0 -1.26585c0,-0.891375 0.7294,-1.62087 1.62053,-1.62087l8.91368 0c0.89115,0 1.62055,0.7295 1.62055,1.62087l0 1.26585 12.348 0c2.62945,0 4.7808,2.15135 4.7808,4.78083l0 7.17122 -46.4124 0 0 -7.17122c0,-2.62947 2.15135,-4.78083 4.7808,-4.78083zm-3.14742 8.79875l42.373 0 0 0.802 -42.373 0 0 -0.802z"/>
              <path class="plugin_phanterimages-icone-lixeira plugin_phanterimages-branco plugin_phanterimages-botao-icone" d="M46.0118 18.7767l-3.54275 25.4634c-0.35805,2.57343 -2.75648,4.6789 -5.32985,4.6789l-0.8035 0 -22.2196 0 -0.803525 0c-2.57338,0 -4.9718,-2.10547 -5.32982,-4.6789l-3.54277 -25.4634 41.5718 0zm-37.5934 2.94073l0 0c0.69845,0 1.33935,0.5714 1.4243,1.26985l2.58485 21.2533c0.08495,0.698425 -0.416975,1.26985 -1.1154,1.26985l0 0c-0.69845,0 -1.33935,-0.571425 -1.4243,-1.26985l-2.58485 -21.2533c-0.084975,-0.69845 0.41695,-1.26985 1.1154,-1.26985zm6.79785 0c0,0 0,0 0,0 0.698425,0 1.31123,0.5714 1.36182,1.26985 0.51315,7.0844 1.02628,14.1689 1.53943,21.2533 0.0506,0.698425 -0.479425,1.26985 -1.17788,1.26985 0,0 0,0 0,0 -0.69845,0 -1.31123,-0.571425 -1.36182,-1.26985 -0.51315,-7.08445 -1.02628,-14.1689 -1.53945,-21.2533 -0.050575,-0.69845 0.47945,-1.26985 1.1779,-1.26985zm6.7978 0c0,0 0,0 0,0 0.698425,0 1.28312,0.5714 1.29937,1.26985 0.16465,7.0844 0.329325,14.1689 0.493975,21.2533 0.01625,0.698425 -0.541875,1.26985 -1.24033,1.26985 0,0 0,0 0,0 -0.69845,0 -1.28312,-0.571425 -1.29938,-1.26985 -0.16465,-7.08445 -0.329325,-14.1689 -0.493975,-21.2533 -0.01625,-0.69845 0.541875,-1.26985 1.24033,-1.26985zm6.79777 0c0,0 0,0 0,0 0.69845,0 1.25503,0.5714 1.2369,1.26985 -0.1838,7.0844 -0.367625,14.1689 -0.551425,21.2533 -0.0181,0.698425 -0.60435,1.26985 -1.3028,1.26985 0,0 0,0 0,0 -0.69845,0 -1.255,-0.571425 -1.2369,-1.26985 0.1838,-7.08445 0.367625,-14.1689 0.551425,-21.2533 0.018125,-0.69845 0.60435,-1.26985 1.3028,-1.26985zm6.7978 0c0,0 0,0 0,0 0.69845,0 1.22695,0.5714 1.17448,1.26985 -0.532325,7.0844 -1.0646,14.1689 -1.5969,21.2533 -0.05245,0.698425 -0.6668,1.26985 -1.36525,1.26985 0,0 0,0 0,0 -0.69845,0 -1.2269,-0.571425 -1.17445,-1.26985 0.5323,-7.08445 1.06457,-14.1689 1.5969,-21.2533 0.05245,-0.69845 0.6668,-1.26985 1.36523,-1.26985zm6.79782 0l0 0c0.698425,0 1.19882,0.5714 1.11198,1.26985l-2.6423 21.2533c-0.086825,0.698425 -0.729275,1.26985 -1.42773,1.26985l0 0c-0.698425,0 -1.1988,-0.571425 -1.11197,-1.26985l2.6423 -21.2533c0.08685,-0.69845 0.729275,-1.26985 1.42772,-1.26985zm-35.9012 -16.6852l12.348 0 0 -1.26585c0,-0.891375 0.7294,-1.62088 1.62053,-1.62088l8.91368 0c0.89115,0 1.62055,0.7295 1.62055,1.62088l0 1.26585 12.348 0c2.62945,0 4.7808,2.15135 4.7808,4.78082l0 7.17123 -46.4124 0 0 -7.17123c0,-2.62948 2.15135,-4.78082 4.7808,-4.78082zm-3.14742 8.79875l42.373 0 0 0.802 -42.373 0 0 -0.802z"/>
             </g>
            </svg>
        """
        self.mudar_imagem="""
            <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
            viewBox="0 0 50 50"
             xmlns:xlink="http://www.w3.org/1999/xlink">
             <g>
              <metadata/>
              <path class="plugin_phanterimages-icone-mudar-imagem plugin_phanterimages-preto" d="M27.5232 29.7809l7.00265 14.5405 -8.1171 0 -0.898725 0 -7.21833 0 -4.9573 0 4.73455 -9.11435 3.83182 3.9941 0.449425 -0.63755 5.173 -8.7827zm-8.86492 -4.07985c1.83983,0 3.3319,1.49205 3.3319,3.3319 0,1.83975 -1.49207,3.33178 -3.3319,3.33178 -1.83973,0 -3.33183,-1.49202 -3.33183,-3.33178 0,-1.83985 1.4921,-3.3319 3.33183,-3.3319zm-7.82405 21.4479l26.0418 0 0 -26.0418 -26.0418 0 0 26.0418zm1.83088 -1.83087l22.38 0 0 -22.38 -22.38 0 0 22.38zm5.76638 -42.1615c11.5071,-3.0833 23.3393,3.74808 26.4227,15.2551 0.7239,2.70168 0.899675,5.42083 0.59825,8.04093l3.3201 0.4323 -3.2085 4.1936 -3.20832 4.19353 -2.0276 -4.8754 -2.0275 -4.8753 2.5651 0.334c0.225625,-2.03675 0.084275,-4.14852 -0.477975,-6.24688 -2.42245,-9.04072 -11.7187,-14.4079 -20.7594,-11.9855 -9.04073,2.42245 -14.4079,11.7187 -11.9855,20.7594 0.12435,0.4641 0.267,0.9184 0.426675,1.36252l-4.40485 1.41427c-0.181175,-0.516125 -0.34435,-1.04293 -0.488275,-1.58002 -3.0833,-11.5071 3.74808,-23.3394 15.2551,-26.4227z"/>
              <path class="plugin_phanterimages-icone-mudar-imagem plugin_phanterimages-branco plugin_phanterimages-botao-icone" d="M27.1357 29.5639l7.00265 14.5405 -8.1171 0 -0.898725 0 -7.21833 0 -4.9573 0 4.73455 -9.11435 3.83182 3.9941 0.449425 -0.63755 5.173 -8.7827zm-8.86492 -4.07985c1.83983,0 3.3319,1.49205 3.3319,3.3319 0,1.83975 -1.49207,3.33178 -3.3319,3.33178 -1.83973,0 -3.33183,-1.49202 -3.33183,-3.33178 0,-1.83985 1.4921,-3.3319 3.33183,-3.3319zm-7.82405 21.4479l26.0418 0 0 -26.0418 -26.0418 0 0 26.0418zm1.83087 -1.83087l22.38 0 0 -22.38 -22.38 0 0 22.38zm5.76638 -42.1615c11.5071,-3.0833 23.3394,3.74808 26.4227,15.2551 0.7239,2.70168 0.899675,5.42083 0.59825,8.04093l3.3201 0.4323 -3.2085 4.1936 -3.20833 4.19352 -2.0276 -4.8754 -2.0275 -4.8753 2.5651 0.334c0.225625,-2.03675 0.084275,-4.14852 -0.477975,-6.24687 -2.42245,-9.04073 -11.7187,-14.4079 -20.7594,-11.9855 -9.04072,2.42245 -14.4079,11.7187 -11.9855,20.7594 0.12435,0.4641 0.267,0.9184 0.426675,1.36252l-4.40485 1.41427c-0.181175,-0.516125 -0.34435,-1.04292 -0.488275,-1.58002 -3.0833,-11.5071 3.74808,-23.3394 15.2551,-26.4227z"/>
             </g>
            </svg>
        """
        self.html_btn_padrao=DIV(XML(self.botao_upload), DIV(self.nome_do_botao, _class='plugin_phanterimages_titulo_botao_padrao'),_class='plugin_phanterimages_botao_padrao')


    def _botaoUpload(self):
        nome_do_botao=self.nome_do_botao
        botao_upload=self.botao_upload
        html_botao=DIV(DIV(XML(botao_upload), DIV(nome_do_botao, _class='plugin_phanterimages_titulo_botao_padrao'),_class='plugin_phanterimages_botao_padrao'), _class="plugin_phanterimages_botao_padrao-container")
        return html_botao

    def _botaoUploadImage(self, id_imagem):
        db=self.db
        icone_lixeira=self.icone_lixeira
        mudar_imagem=self.mudar_imagem

        plugin_phanterimages_uploads=db.plugin_phanterimages_uploads
        url_imagem_response=URL('default', 'download', args=plugin_phanterimages_uploads[id_imagem].imagem)
        attr_imagem_response={"_data-id": id_imagem}
        html_imagem_response=DIV(
            DIV(
           
                IMG(_src=url_imagem_response, _alt="Visualizar imagem do upload", _width=self.tamanho_corte[0], _height=self.tamanho_corte[1], **attr_imagem_response), 
                DIV(
                    DIV(XML(icone_lixeira), _title="Apagar imagem", _id="plugin_phanterimages_botao-deletar-imagem", _class='plugin_phanterimages_imagem_visualizar-painel-botoes-deletar'),
                    DIV(XML(mudar_imagem), _title="Mudar imagem", _id="plugin_phanterimages_botao-mudar-imagem", _class='plugin_phanterimages_imagem_visualizar-painel-botoes-mudar'),
                    _class="plugin_phanterimages_imagem_visualizar-painel-botoes"),
                _class="plugin_phanterimages_imagem-visualizada", _style="width:%spx; height:%spx; position:relative; min-height:200px; min-width:200px;margin-left: auto; margin-right: auto;" %(self.tamanho_corte[0], self.tamanho_corte[1])),
            _class="plugin_phanterimages_botao_image-container")
        return html_imagem_response

    def _uploadArea(self):
        
        id_painel_corte=self._id_painel_corte
        id_alvo_upload=self._id_alvo_upload
        id_barra_progresso=self._id_barra_progresso
        mapa_script=self._mapa_script
        
        mapa_script['id_painel_corte']=id_painel_corte
        kargs=self.kargs
        tipos=self.tipos
        class_padrao='plugin_phanterimages_botao_pega_imagem'
        if '_class' in kargs:
            kargs['_class']=class_padrao+' '+kargs['_class']
        else:
            kargs['_class']=class_padrao

        self.html_btn_padrao=self._botaoUpload()
        texto_lendo=self.texto_lendo
        mapa_script['script_botao']="$('.plugin_phanterimages_titulo_botao_padrao').text('%s');" %(texto_lendo)
        mapa_script['botao_padrao']='+"&botao_padrao=Sim"'
        self.html_botao=CAT()

        html_adicional=CAT(DIV(self.html_btn_padrao, **kargs),
            DIV(INPUT(_name='imagem', _accept=tipos, _type='file', _id=mapa_script['id_input'], _class="upload input-file", _onchange='fazer_upload()'), _id="plugin_phanterimages_formulario", _style='display:none;'),  
            DIV(_id=id_painel_corte),
            DIV(_id=id_alvo_upload),
            DIV(
                DIV(
                    DIV(_class="plugin_phanterimages_indeterminate"),
                    _class="plugin_phanterimages_progress"),
                _id=id_barra_progresso, _class="plugin_phanterimages_barra_de_progresso")
            )
        script="""
            $('.plugin_phanterimages_botao_pega_imagem').click(function(){
                $("#%(id_painel_corte)s").html("");
                $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived'); 
                $('#%(id_input)s').trigger('click');
            });
            function verifique_extensao(nome_do_arquivo){
                var array_ext=['jpg', 'jpeg', 'bmp', 'gif', 'png']
                var tamanho_array=nome_do_arquivo.split('.').length;
                if (tamanho_array>1){
                    var extensao=nome_do_arquivo.split('.').pop();
                    extensao=extensao.toLowerCase();
                    if (array_ext.indexOf(extensao)<0){
                        $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O arquivo não parece ser uma imagem válida.</div>");
                        return false
                    } else{
                        if(nome_do_arquivo.length<40){
                            %(script_botao)s;
                            return true;
                        } else{
                            $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O nome do arquivo é muito longo! Diminua antes do upload (máximo de 40 caracteres).</div>");
                            return false;
                        }
                    }
                } else{
                    $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O arquivo não parece ser uma imagem válida.</div>");
                    return false
                }
            };
            function uploadFile(form, blobFile, fileName) {

                var fd = new FormData();
                fd.append("fileToUpload", blobFile);
                var nome_do_arquivo=fileName;
                if(verifique_extensao(nome_do_arquivo)){
                    $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').addClass('actived');    
                    $.ajax({
                        url: "%(url)s",
                        type: "POST",
                        data: fd,
                        processData: false,
                        contentType: false,
                        async: true,
                        success: function(response) {
                            $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived');
                            var url_echo=response["url_echo"];
                            ajax(url_echo, [], ':eval');
                        },
                        error: function(jqXHR, textStatus, errorMessage) {
                           $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived');
                           console.log(errorMessage);
                        }
                    });  
                }

            }
            function fazer_upload(){
                blob = $("#%(id_input)s")[0].files;
                var quantidade_arq=blob.length;
                for (var i = quantidade_arq - 1; i >= 0; i--) {
                  var tipo = blob[i]['type'];
                  var nome_img= blob[i]['name'];
                  if (tipo=="image/png"||tipo=="image/bmp"||tipo=="image/gif"||tipo=="image/jpeg"){
                   uploadFile($("#plugin_phanterimages_formulario")[0], blob[i], nome_img);
                  } else{
                    alert("Não foi possível fazer o upload do arquivo "+nome_img);
                  }
                }
            }
        """ %mapa_script
        self.html_botao.append(CAT(html_adicional,SCRIPT(script)))
        return self.html_botao

    def _uploadAreaImagem(self, id_imagem):
        db=self.db
        plugin_phanterimages_uploads=db.plugin_phanterimages_uploads
        if not plugin_phanterimages_uploads[id_imagem]:
            return self._uploadArea()
        id_painel_corte=self._id_painel_corte
        id_alvo_upload=self._id_alvo_upload
        id_barra_progresso=self._id_barra_progresso
        mapa_script=self._mapa_script
        
        mapa_script['id_painel_corte']=id_painel_corte
        kargs=self.kargs
        tipos=self.tipos
        class_padrao='plugin_phanterimages_botao_pega_imagem'
        if '_class' in kargs:
            kargs['_class']=class_padrao+' '+kargs['_class']
        else:
            kargs['_class']=class_padrao

        self.html_btn_padrao=self._botaoUploadImage(id_imagem)
        mapa_script['botao_padrao']='+"&botao_padrao=Sim"'
        self.html_botao=CAT()

        html_adicional=CAT(DIV(self.html_btn_padrao, **kargs),
            DIV(INPUT(_name='imagem', _accept=tipos, _type='file', _id=mapa_script['id_input'], _class="upload input-file", _onchange='fazer_upload()'), _id="plugin_phanterimages_formulario", _style='display:none;'),  
            DIV(_id=id_painel_corte),
            DIV(_id=id_alvo_upload),
            DIV(
                DIV(
                    DIV(_class="plugin_phanterimages_indeterminate"),
                    _class="plugin_phanterimages_progress"),
                _id=id_barra_progresso, _class="plugin_phanterimages_barra_de_progresso")
            )
        script="""
            $('#plugin_phanterimages_botao-mudar-imagem').click(function(){
                $("#%(id_painel_corte)s").html("");
                $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived'); 
                $('#%(id_input)s').trigger('click');
            });
            $("#plugin_phanterimages_botao-deletar-imagem").on('click', function(){
                var id_imagem=$(".plugin_phanterimages_imagem-visualizada>img").attr("data-id");
                deletar_imagem(id_imagem);
            });
            function verifique_extensao(nome_do_arquivo){
                var array_ext=['jpg', 'jpeg', 'bmp', 'gif', 'png']
                var tamanho_array=nome_do_arquivo.split('.').length;
                if (tamanho_array>1){
                    var extensao=nome_do_arquivo.split('.').pop();
                    extensao=extensao.toLowerCase();
                    if (array_ext.indexOf(extensao)<0){
                        $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O arquivo não parece ser uma imagem válida.</div>");
                        return false
                    } else{
                        if(nome_do_arquivo.length<40){
                            return true;
                        } else{
                            $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O nome do arquivo é muito longo! Diminua antes do upload (máximo de 40 caracteres).</div>");
                            return false;
                        }
                    }
                } else{
                    $("#%(id_painel_corte)s").html("<div style='color:red; text-align: center;'>O arquivo não parece ser uma imagem válida.</div>");
                    return false
                }
            };
            function uploadFile(form, blobFile, fileName) {

                var fd = new FormData();
                fd.append("fileToUpload", blobFile);
                var nome_do_arquivo=fileName;
                if(verifique_extensao(nome_do_arquivo)){
                    $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').addClass('actived');    
                    $.ajax({
                        url: "%(url)s",
                        type: "POST",
                        data: fd,
                        processData: false,
                        contentType: false,
                        async: true,
                        success: function(response) {
                            $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived');
                            var url_echo=response["url_echo"];
                            ajax(url_echo, [], ':eval');
                        },
                        error: function(jqXHR, textStatus, errorMessage) {
                           $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').removeClass('actived');
                           console.log(errorMessage);
                        }
                    });  
                }

            }
            function fazer_upload(){
                blob = $("#%(id_input)s")[0].files;
                var quantidade_arq=blob.length;
                for (var i = quantidade_arq - 1; i >= 0; i--) {
                  var tipo = blob[i]['type'];
                  var nome_img= blob[i]['name'];
                  if (tipo=="image/png"||tipo=="image/bmp"||tipo=="image/gif"||tipo=="image/jpeg"){
                   uploadFile($("#plugin_phanterimages_formulario")[0], blob[i], nome_img);
                  } else{
                    alert("Não foi possível fazer o upload do arquivo "+nome_img);
                  }
                }
            }
            function deletar_imagem(id_imagem){
                $('#%(id_barra_progresso)s>.plugin_phanterimages_progress').addClass('actived');
                var url_echo="%(url)s/deletar/"+id_imagem
                console.log(url_echo)
                ajax(url_echo, [], ":eval")
            }
        """ %mapa_script
        self.html_botao.append(CAT(html_adicional,SCRIPT(script)))
        return self.html_botao

    def urlAJAX(self, url):
        self.url_ajax=url

    def echoPhanterImages(self, _id="", campo="imagem"):
        import os
        import json
        id_painel_corte=self._id_painel_corte
        id_alvo_upload=self._id_alvo_upload
        request = current.request
        db=self.db
        plugin_phanterimages_uploads_temp=db.plugin_phanterimages_uploads_temp
        plugin_phanterimages_uploads=db.plugin_phanterimages_uploads
        icone_fechar=self.icone_fechar
        icone_visualizar=self.icone_visualizar
        icone_cortar=self.icone_cortar
        icone_aumentar=self.icone_aumentar
        icone_diminuir=self.icone_diminuir
        botao_simples=self.botao_simples
        """
        @plugin_phanterimages_uploads_temp: tabela de imagens temporárias. Necessário caso seja configurado um tamanho para corte. Nela será armazenada a imagem
            antes de ser cortada para ser armazenada definitivamente. exemplo.: db.temp_imagem
        @plugin_phanterimages_uploads: tabela onde as imagens serão armazenadas. exemplo.: db.imagens
        @_id: irá armazenar em um registro específico.
        """
        if request.args(0)=='painel_corte' and request.args(1):
            import os
            import json
            from PIL import Image
            if request.vars.redirecionar:
                url_redirecionamento=request.vars.redirecionar
            else:
                url_redirecionamento=""
            if request.vars.largura_corte and request.vars.altura_corte and request.vars.altura and request.vars.largura:
                q_imagem=plugin_phanterimages_uploads_temp[request.args(1)]
                url_imagem=URL('default','download', args=[q_imagem.imagem])
                if request.vars.botao_padrao:
                    url_cancelar=URL(args=['cancelar', request.args(1)])
                    url_echo_cortar_imagem=URL(args=['cortar', request.args(1)])
                else:
                    url_cancelar=URL(args=['cancelar', request.args(1)])
                    url_echo_cortar_imagem=URL(args=['cortar', request.args(1)])                    
                
                formato={
                    'url_imagem':url_imagem, 
                    'largura':request.vars.largura, 
                    'altura':request.vars.altura, 
                    'largura_corte': request.vars.largura_corte,
                    'altura_corte': request.vars.altura_corte,
                    'url_cancelar': url_cancelar, 
                    'url_echo_cortar_imagem': url_echo_cortar_imagem, 
                    'url_redirecionamento':url_redirecionamento
                    }

                if q_imagem:
                    html=DIV(IMG(_src=url_imagem, _id='imagem_escolhida', _style="display:none;"),
                            DIV(XML(icone_fechar), _class='plugin_phanterimages_botao_fechar'),
                            DIV(_class='plugin_phanterimages_alvo_visualizar_imagem', _style='display:none'),
                            DIV(XML(icone_visualizar), _class='plugin_phanterimages_botao_visualizar'),
                            DIV(XML(icone_cortar), _class='plugin_phanterimages_botao_upload'),
                            DIV(
                                DIV(_class='plugin_phanterimages_caixacorte'), 
                                _class='plugin_phanterimages_caixaimage'),
                            DIV(
                                DIV(
                                    DIV(
                                        DIV(_class="plugin_phanterimages_indeterminate"),
                                        _class="plugin_phanterimages_progress"),
                                    _id="plugin_phanterimages_barra_de_progresso_painel", _class="plugin_phanterimages_barra_de_progresso"),
                                _class='plugin_phanterimages_caixa_barraprogresso'),
                            DIV(
                                DIV(
                                    DIV(XML(icone_diminuir),_class="diminuir_figura"),
                                    DIV(I(_class="glyphicon glyphicon-backward"),_class="detalhe_esquerdo"),
                                    DIV(
                                        DIV(XML("&#160;"),_id="fundo_deslizante"),
                                        DIV(XML("&#160;"),_id="marcador_controle"),
                                        
                                        _class="caixa_controle_zoom"),
                                    DIV(I(_class="glyphicon glyphicon-forward"),_class="detalhe_direito"),
                                    DIV(XML(icone_aumentar),_class="aumentar_figura"),
                                    _class='plugin_phanterimages_comandosrezise'),
                                _class='plugin_phanterimages_caixazoom'),
                            _class="plugin_phanterimages_principal")
                    script="""
                            $(document).ready(function(){
                                    $('.plugin_phanterimages_principal').css('background-image', 'url("%(url_imagem)s"');
                                    $('.plugin_phanterimages_caixacorte').css('background-image', 'url("%(url_imagem)s"');
                                    $('.plugin_phanterimages_caixacorte').width(%(largura_corte)s);
                                    $('.plugin_phanterimages_caixacorte').height(%(altura_corte)s);
                                    $('.plugin_phanterimages_botao_fechar').click(function(){
                                        $('#plugin_phanterimages_barra_de_progresso_painel>.plugin_phanterimages_progress').addClass('actived');
                                        var url_echo_del="%(url_cancelar)s";
                                        ajax(url_echo_del, [], ':eval');
                                    })
                                    var posicao_ini_imagem_principal_x=0;
                                    var posicao_ini_imagem_principal_y=0;
                                    var posicao_ini_imagem_x=0;
                                    var posicao_ini_imagem_y=0;
                                    var iniciar_movimento=false;
                                    var posicao_do_mouse_x=0;
                                    var posicao_do_mouse_y=0;
                                    var movimento_do_mouse_x=0;
                                    var movimento_do_mouse_y=0;
                                    var deslocamento_x=0;
                                    var deslocamento_y=0;
                                    var srcImagem=$('#imagem_escolhida').attr('src');
                                    var largura_imagem=parseInt(%(largura)s);
                                    var altura_imagem=parseInt(%(altura)s);
                                    var largura_corte=0
                                    var altura_corte=0
                                    var novo_tamanho_altura=parseInt(%(altura)s);
                                    var novo_tamanho_largura=parseInt(%(largura)s);
                                    var zoom=1
                                    function construir_janela(){
                                        var largura_principal=$('.plugin_phanterimages_principal').width();
                                        var altura_principal=$('.plugin_phanterimages_principal').height();
                                        if (largura_imagem<largura_principal){
                                            var desconto_largura=(largura_principal-largura_imagem)/2.;
                                            posicao_ini_imagem_principal_x=desconto_largura;
                                        }
                                        if (altura_imagem<altura_principal){
                                            var desconto_altura=(largura_principal-largura_imagem)/2.;
                                            posicao_ini_imagem_principal_y=desconto_altura;
                                        }
                                        largura_corte=$('.plugin_phanterimages_caixacorte').width();
                                        altura_corte=$('.plugin_phanterimages_caixacorte').height();
                                        posicao_ini_imagem_x=(((largura_principal/2.)-(largura_corte/2.))*(-1))+posicao_ini_imagem_principal_x;
                                        posicao_ini_imagem_y=(((altura_principal/2.)-(altura_corte/2.))*(-1))+posicao_ini_imagem_principal_y;
                                        $('.plugin_phanterimages_caixacorte').css('background-position-x', posicao_ini_imagem_x);
                                        $('.plugin_phanterimages_caixacorte').css('background-position-y', posicao_ini_imagem_y);
                                        $('.plugin_phanterimages_principal').css('background-position-x', posicao_ini_imagem_principal_x);
                                        $('.plugin_phanterimages_principal').css('background-position-y', posicao_ini_imagem_principal_y);
                                    }
                                    construir_janela();
                                    $(window).resize(function(){construir_janela()});

                                    $('.plugin_phanterimages_caixaimage').mousedown(function(event){
                                        $('.plugin_phanterimages_caixaimage').css('cursor', 'grabbing');
                                        iniciar_movimento = true;
                                        posicao_do_mouse_x = event.pageX;
                                        posicao_do_mouse_y = event.pageY;
                                    });
                                    $('.plugin_phanterimages_caixaimage').mousemove(function(event){
                                        if (iniciar_movimento==true){
                                            movimento_do_mouse_x = event.pageX;
                                            movimento_do_mouse_y = event.pageY;
                                            deslocamento_x = (movimento_do_mouse_x-posicao_do_mouse_x);
                                            deslocamento_y = (movimento_do_mouse_y-posicao_do_mouse_y);
                                            $('.plugin_phanterimages_caixacorte').css('background-position-x', posicao_ini_imagem_x+deslocamento_x);
                                            $('.plugin_phanterimages_caixacorte').css('background-position-y', posicao_ini_imagem_y+deslocamento_y);
                                            $('.plugin_phanterimages_principal').css('background-position-x', posicao_ini_imagem_principal_x+deslocamento_x);
                                            $('.plugin_phanterimages_principal').css('background-position-y', posicao_ini_imagem_principal_y+deslocamento_y);
                                        } 
                                    });
                                    $('.plugin_phanterimages_caixaimage').mouseup(function(event){
                                        $('.plugin_phanterimages_caixaimage').css('cursor', 'grab');
                                        if (iniciar_movimento==true){
                                            posicao_ini_imagem_x=posicao_ini_imagem_x+deslocamento_x;
                                            posicao_ini_imagem_y=posicao_ini_imagem_y+deslocamento_y;
                                            posicao_ini_imagem_principal_x=posicao_ini_imagem_principal_x+deslocamento_x;
                                            posicao_ini_imagem_principal_y=posicao_ini_imagem_principal_y+deslocamento_y;
                                        }
                                        iniciar_movimento = false; 
                                    });
                                    $('.plugin_phanterimages_caixaimage').mouseleave(function(event){
                                        $('.plugin_phanterimages_caixaimage').css('cursor', 'grab');
                                        if (iniciar_movimento==true){
                                            posicao_ini_imagem_x=posicao_ini_imagem_x+deslocamento_x;
                                            posicao_ini_imagem_y=posicao_ini_imagem_y+deslocamento_y;
                                            posicao_ini_imagem_principal_x=posicao_ini_imagem_principal_x+deslocamento_x;
                                            posicao_ini_imagem_principal_y=posicao_ini_imagem_principal_y+deslocamento_y;
                                        }
                                        iniciar_movimento = false;
                                    });
                                    var mexer_marca=false;
                                    var posicao_marca= $("#marcador_controle").css("left");
                                    var posicao_marca_left=parseInt(posicao_marca.replace("px",""));
                                    var posicao_inicial_mouse_x=0;
                                    var cem_por_cento = posicao_marca_left;
                                    function porcentagem (valor, cem_por_cento) {
                                        var valor = valor;
                                        var cem_por_cento = cem_por_cento;
                                        var coeficiente = parseFloat(valor/cem_por_cento);
                                        return coeficiente
                                    }
                                    $('#marcador_controle').mousedown(function(event){
                                        posicao_marca= $("#marcador_controle").css("left");
                                        posicao_marca_left=parseInt(posicao_marca.replace("px",""));
                                        posicao_inicial_mouse_x = event.pageX;
                                        mexer_marca=true;
                                        event.preventDefault();       
                                    })
                                    $(document).mousemove(function(event){
                                        var posicao_x_atualizada=parseInt($("#marcador_controle").css("left").replace("px",""));

                                        if(posicao_x_atualizada<0){
                                            mexer_marca=false;
                                            $("#marcador_controle").css("left", "0px");

                                        } else if(posicao_x_atualizada>250){
                                            mexer_marca=false;
                                            $("#marcador_controle").css("left", "250px");
                                        }
                                        if(mexer_marca==true){
                                            zoom=(porcentagem(posicao_x_atualizada, cem_por_cento));
                                            novo_tamanho_altura=altura_imagem*zoom
                                            novo_tamanho_largura=largura_imagem*zoom
                                            $(".plugin_phanterimages_caixacorte").css("backgroundSize", largura_imagem*zoom+"px "+altura_imagem*zoom+"px" );
                                            $(".plugin_phanterimages_principal").css("backgroundSize", largura_imagem*zoom+"px "+altura_imagem*zoom+"px" );

                                            movimento_mouse_x = event.pageX;
                                            deslocamento_marca = ((posicao_marca_left)+(movimento_mouse_x-posicao_inicial_mouse_x));

                                            $("#marcador_controle").css("left", deslocamento_marca+"px");

                                        }
                                    })
                                    $(document).mouseup(function(event){
                                        mexer_marca=false;
                                    })
                                    
                                    function ajax_crop_imagem(gravar=false, redirecionar=false){

                                        
                                        if(gravar==false){
                                            var gravar="";
                                        } else{
                                            var gravar="&gravar='sim'";
                                        }
                                        var redirecionar=redirecionar;
                                        if (redirecionar==false){
                                            var redirecionamento="";
                                        } else {
                                            var redirecionamento="&redirecionar="+redirecionar;
                                        }
                                        var url_echo_gravar_visualizar="%(url_echo_cortar_imagem)s?novo_tamanho_altura="+novo_tamanho_altura+"&novo_tamanho_largura="+novo_tamanho_largura+"&altura_corte="+altura_corte+"&largura_corte="+largura_corte+"&left_corte="+posicao_ini_imagem_x+"&top_corte="+posicao_ini_imagem_y+redirecionamento+gravar
                                        var id_para_substituir=$(".plugin_phanterimages_imagem-visualizada>img").attr("data-id");
                                        if (id_para_substituir==undefined){
                                        } else{
                                            url_echo_gravar_visualizar=url_echo_gravar_visualizar+"&substituir="+id_para_substituir
                                        }
                                        console.log(url_echo_gravar_visualizar)
                                        ajax(url_echo_gravar_visualizar,[],':eval')
                                        };
                                    $('.plugin_phanterimages_botao_visualizar').click(function(){
                                        $('#plugin_phanterimages_barra_de_progresso_painel>.plugin_phanterimages_progress').addClass('actived');
                                        ajax_crop_imagem(false, false);
                                    });
                                    $('.plugin_phanterimages_botao_upload').click(function(){
                                         $('#plugin_phanterimages_barra_de_progresso_painel>.plugin_phanterimages_progress').addClass('actived');

                                        ajax_crop_imagem(true, '%(url_redirecionamento)s');
                                    });
                            });
                    """ %formato
                    html.append(SCRIPT(script))
                    html_botao_padrao=self.html_btn_padrao
                    script_botao_padrao="$('.plugin_phanterimages_botao_padrao').html(%s);" %json.dumps(html_botao_padrao.xml())
                    return [False, "$('#%s').html(%s);%s" %(id_painel_corte, json.dumps(html.xml()), script_botao_padrao)]
            else:
                q_imagem=plugin_phanterimages_uploads_temp[request.args(1)]
                imagem_temp=q_imagem.imagem
                nome_da_imagem=plugin_phanterimages_uploads_temp.imagem.retrieve(imagem_temp)[0]
                if _id:
                    id_upload=plugin_phanterimages_uploads[_id]={campo:plugin_phanterimages_uploads.imagem.store(open(os.path.join(request.folder, 'uploads', 'plugin_phanterimages_uploads_temp', imagem_temp), 'rb'), nome_da_imagem)}
                else:
                    id_upload=plugin_phanterimages_uploads[0]={campo:plugin_phanterimages_uploads.imagem.store(open(os.path.join(request.folder, 'uploads', 'plugin_phanterimages_uploads_temp', imagem_temp), 'rb'), nome_da_imagem)}
                del plugin_phanterimages_uploads_temp[request.args(1)]
                q_imagem_fixa=id_upload
                html=DIV(IMG(_src=URL('default','download',args=[q_imagem_fixa['imagem']])), _class="plugin_phanterimages_imagem_para_cortar")
                script_botao_padrao=''
                if request.vars.botao_padrao:
                    html_botao_padrao=self.html_btn_padrao
                    script_botao_padrao="$('.plugin_phanterimages_botao_padrao').html(%s);" %json.dumps(html_botao_padrao.xml())
                return [False, '$("#id_alvo_upload").append(%s);%s' %(id_alvo_upload, json.dumps(html.xml()), script_botao_padrao)]
        
        elif request.args(0)=='cortar' and request.args(1):
            from PIL import Image as PilImage
            import cStringIO
            import base64
            import json
            import os
            if request.args(1):
                q_imagem=plugin_phanterimages_uploads_temp[request.args(1)]
                if q_imagem:
                    
                    imagem_temp=q_imagem.imagem
                    nome_da_imagem=plugin_phanterimages_uploads_temp.imagem.retrieve(imagem_temp)[0]
                    nome_da_imagem=nome_da_imagem.encode('utf-8')
                    im = PilImage.open(os.path.join(request.folder, 'uploads', 'plugin_phanterimages_uploads_temp', imagem_temp)) 
                    novo_tamanho_altura = int(float(request.vars.novo_tamanho_altura))
                    novo_tamanho_largura = int(float(request.vars.novo_tamanho_largura))
                    tamanho_corte_altura = float(request.vars.altura_corte)
                    tamanho_corte_largura = float(request.vars.largura_corte)
                    postopo_caixa_corte = float(request.vars.top_corte)*(-1)
                    posleft_caixa_corte = float(request.vars.left_corte)*(-1)
                    extensao = os.path.splitext(imagem_temp)[1]
                    im = im.resize((novo_tamanho_largura, novo_tamanho_altura), PilImage.ANTIALIAS)
                    im = im.crop((posleft_caixa_corte, postopo_caixa_corte, posleft_caixa_corte+tamanho_corte_largura, postopo_caixa_corte+tamanho_corte_altura))
                    jpeg_image_buffer = cStringIO.StringIO()

                    if extensao.lower()=='.png':
                        im.save(jpeg_image_buffer, 'png')
                    else:
                        im.save(jpeg_image_buffer, format='JPEG', quality=100)
                    if request.vars.gravar:
                        jpeg_image_buffer.seek(0)
                        if _id:
                            id_upload=_id
                            plugin_phanterimages_uploads[_id]={campo:plugin_phanterimages_uploads.imagem.store(jpeg_image_buffer, nome_da_imagem)}
                        else:
                            file=plugin_phanterimages_uploads.imagem.store(jpeg_image_buffer, remover_acentos(nome_da_imagem, maiusculo=False))
                            if  request.vars.substituir:
                                plugin_phanterimages_uploads[request.vars.substituir].update_record(imagem=file)
                                id_upload=request.vars.substituir
                            else:
                                id_upload=plugin_phanterimages_uploads.insert(imagem=file)
                        url=plugin_phanterimages_uploads[id_upload].imagem
                            #id_upload=plugin_phanterimages_uploads[0]={campo:file}
                        url_imagem_response=URL('default', 'download', args=[url])
                        html_imagem_response=self._uploadAreaImagem(id_upload)
                        script_callback='var response={"id":"%s", "url":"%s"};function plugin_phanterimage_callbackAfterCut(response){$("#plugin_phanterimages_main-container").html(%s);%s};plugin_phanterimage_callbackAfterCut(response);' %(id_upload, url_imagem_response, json.dumps(html_imagem_response.xml()), self.callbackOnCut)
                        del plugin_phanterimages_uploads_temp[request.args(1)]
                        return [False, '$("#plugin_phanterimages_barra_de_progresso_painel>.plugin_phanterimages_progress").removeClass("actived"); $(".plugin_phanterimages_principal").fadeOut();%s' %script_callback]
                    imgStr = base64.b64encode(jpeg_image_buffer.getvalue())
                    html_visualizar=DIV(DIV(IMG(_src="%s%s"%("data:image/jpg;base64,",imgStr)), _class='plugin_phanterimages_imagem_cortada'),DIV(I(_class='glyphicon glyphicon-play'),_class='plugin_phanterimages_arranjo_caixa_visualizar'), DIV(XML(botao_simples), _class="plugin_phanterimages_botao_fechar_visualizar"),_class='plugin_phanterimages_caixa_visualizar')
                    return [False, '$("#plugin_phanterimages_barra_de_progresso_painel>.plugin_phanterimages_progress").removeClass("actived"); $(".plugin_phanterimages_alvo_visualizar_imagem").html(%s).fadeIn(); $(\'.plugin_phanterimages_botao_upload\').html(%s); $(\'.plugin_phanterimages_botao_visualizar\').html(%s); $(".plugin_phanterimages_botao_fechar_visualizar").click(function(){$(".plugin_phanterimages_alvo_visualizar_imagem").fadeOut();});' %(json.dumps(html_visualizar.xml()), json.dumps(self.icone_visualizar), json.dumps(self.icone_cortar))]

        elif request.args(0)=='cancelar' and request.args(1):
            q_imagem=plugin_phanterimages_uploads_temp[request.args(1)]
            if q_imagem:
                try:
                    del plugin_phanterimages_uploads_temp[request.args(1)]
                except Exception as e:
                    print e
                return [False, "$('.plugin_phanterimages_principal').fadeOut();" ]
            else:
                return [False, "$('.plugin_phanterimages_principal').fadeOut();"]
        
        elif request.args(0)=="deletar" and request.args(1):
            q_imagem=plugin_phanterimages_uploads[request.args(1)]
            if q_imagem:
                try:
                    del plugin_phanterimages_uploads[request.args(1)]
                except Exception as e:
                    print e
                html_botao_padrao=self._uploadArea()
                return [False, "$('#plugin_phanterimages_main-container').html(%s);" %(json.dumps(html_botao_padrao.xml()))]
            else:
                return [False, "console.log(\"Nada a fazer...\")"]
            
        else:

            arquivo=request.vars.fileToUpload
            nomeArquivoExt = arquivo.filename
            nomeArquivo, Ext = os.path.splitext(nomeArquivoExt)
            if Ext in ['.png', '.jpg', '.gif', '.jpeg', '.PNG', '.JPG', '.GIF', '.JPEG']:
                id_upload=plugin_phanterimages_uploads_temp.insert(imagem=plugin_phanterimages_uploads_temp.imagem.store(arquivo.file, nomeArquivoExt))
                from PIL import Image
                file = arquivo.file
                img = Image.open(file)
                size = img.size
            return [True, dict(
                url_echo=URL(
                    args=['painel_corte', id_upload], 
                    vars={
                        'largura':size[0], 
                        'altura':size[1], 
                        "largura_corte": self.tamanho_corte[0], 
                        "altura_corte": self.tamanho_corte[1]
                        }, 
                    extension=False)
                )
            ]

    @staticmethod
    def css(humano=False):
        meucss="/*Inicio Plugin_PhanterImages*/\n\t"+\
                ".plugin_phanterimages_botao_padrao-container {"+\
                    "cursor: pointer;"+\
                    "text-align: center;"+\
                    "margin-left: auto;"+\
                    "margin-right: auto;"+\
                    "width: 175px;"+\
                    "background-color: #f0f0f0;"+\
                    "padding: 11px;"+\
                    "border-radius: 28px;}"+\
                ".plugin_phanterimages_titulo_botao_padrao {"+\
                    "text-transform:uppercase;"+\
                    "color:black;"+\
                    "font-size: 0.8rem;"+\
                    "margin-left: 10px;}"+\
                ".plugin_phanterimages_botao_fechar:hover {"+\
                    "color: orange;"+\
                    "text-shadow: 0px 0px 5px white;}"+\
                ".plugin_phanterimages_botao_fechar {"+\
                    "color: red;"+\
                    "width: 60px;"+\
                    "text-align: center;"+\
                    "position: fixed;"+\
                    "top: 10px;"+\
                    "right: 10px;"+\
                    "text-shadow: 0px 0px 10px black;"+\
                    "z-index: 1005;"+\
                    "cursor: pointer;}"+\
                ".plugin_phanterimages_botao_fechar>i {"+\
                    "font-size: 29pt;}"+\
                ".plugin_phanterimages_botao_visualizar:hover {"+\
                    "color: orange;"+\
                    "text-shadow: 0px 0px 5px white;}"+\
                ".plugin_phanterimages_caixa_visualizar {"+\
                    "border: solid 1px grey;}"+\
                ".plugin_phanterimages_botao_fechar_visualizar {"+\
                    "position: absolute;"+\
                    "padding-top: 5px;"+\
                    "top: 10px;"+\
                    "right: 14px;"+\
                    "color: red;"+\
                    "text-shadow: 1px 1px 2px black;"+\
                    "cursor: pointer;}"+\
                ".plugin_phanterimages_botao_visualizar {"+\
                    "width: 60px;"+\
                    "text-align: center;"+\
                    "color: #37307b;"+\
                    "position: fixed;"+\
                    "top: 60px;"+\
                    "right: 10px;"+\
                    "text-shadow: 0px 0px 10px black;"+\
                    "z-index: 1005;"+\
                    "cursor: pointer;}"+\
                ".plugin_phanterimages_botao_visualizar>i {"+\
                    "font-size: 29pt;}"+\
                ".plugin_phanterimages_botao_upload:hover {"+\
                    "color: orange;"+\
                    "text-shadow: 0px 0px 5px white;}"+\
                ".plugin_phanterimages_botao_upload {"+\
                    "color: #37307b;"+\
                    "position: fixed;"+\
                    "width: 60px;"+\
                    "text-align: center;"+\
                    "top: 108px;"+\
                    "right: 10px;"+\
                    "text-shadow: 0px 0px 10px black;"+\
                    "z-index: 1005;"+\
                    "cursor: pointer;}"+\
                ".plugin_phanterimages_botao_upload>i {"+\
                    "font-size: 29pt;}"+\
                ".plugin_phanterimages_principal {      "+\
                    "position: fixed;"+\
                    "top: 0px;"+\
                    "width: 100%;"+\
                    "height: 100%;"+\
                    "left: 0;"+\
                    "z-index: 1003;"+\
                    "background-color: rgba(19, 11, 51, 0.84);"+\
                    "background-repeat: no-repeat;}"+\
                ".plugin_phanterimages_caixaimage {"+\
                    "cursor: move;"+\
                    "background-color: rgba(0, 0, 0, 0.7);"+\
                    "position: fixed;"+\
                    "top: 0px;"+\
                    "width: 100%;"+\
                    "height: 100%;"+\
                    "left: 0;"+\
                    "z-index: 1004;}"+\
                ".plugin_phanterimages_caixacorte {"+\
                    "background-color: rgba(255,255,255,0.7);"+\
                    "width: 75px;"+\
                    "height: 100px;"+\
                    "position: absolute;"+\
                    "top: 50%;"+\
                    "transform: translate(-50%,-50%);"+\
                    "left: 50%;"+\
                    "background-repeat: no-repeat;}"+\
                ".plugin_phanterimages_caixazoom {"+\
                    "position: fixed;"+\
                    "width: 100%;"+\
                    "height: 50px;"+\
                    "background-color: rgba(255,255,255,0.7);"+\
                    "bottom: 0px;"+\
                    "margin-left: auto;"+\
                    "margin-right: auto;"+\
                    "z-index: 1004;}"+\
                ".plugin_phanterimages_comandosrezise{"+\
                    "text-align: center;"+\
                    "margin-left: auto;"+\
                    "margin-right: auto;"+\
                    "display: table;"+\
                    "color: #1b1b1b;"+\
                    "text-shadow: 1px 1px 1px #d2d2d2;}"+\
                ".caixa_controle_zoom{"+\
                    "float: left;"+\
                    "height: 21px;"+\
                    "margin-top: 11px;"+\
                    "position: relative;"+\
                    "width: 300px;"+\
                    "background-color: grey;}"+\
                "#marcador_controle {"+\
                    "height: 13px;"+\
                    "top: 4px;"+\
                    "position: absolute;"+\
                    "width: 50px;"+\
                    "background-color: #352C2C;"+\
                    "cursor: pointer;"+\
                    "border-radius: 14px;"+\
                    "left: 125px;}"+\
                "#fundo_deslizante {"+\
                    "height: 19px;"+\
                    "top: 1px;"+\
                    "position: absolute;"+\
                    "background-color: rgb(134, 126, 126);}"+\
                ".diminuir_figura {"+\
                    "float:left;"+\
                    "font-size: 14pt;"+\
                    "margin-top: 9px;"+\
                    "margin-right: 10px;}"+\
                ".aumentar_figura {"+\
                    "float:left;"+\
                    "font-size: 19pt;"+\
                    "margin-top: 6px;"+\
                    "margin-left: 10px;}"+\
                ".detalhe_esquerdo {"+\
                    "float:left;"+\
                    "background-color: grey;"+\
                    "margin-top: 11px;"+\
                    "margin-left: 10px;"+\
                    "padding-right: 5px;"+\
                    "padding-left: 5px;"+\
                    "border-radius: 10px 0 0 10px;"+\
                    "font-size: 10pt;"+\
                    "height: 21px;}"+\
                ".detalhe_direito {"+\
                    "float:left;"+\
                    "background-color: grey;"+\
                    "margin-top: 11px;"+\
                    "margin-right: 10px;"+\
                    "padding-right: 5px;"+\
                    "padding-left: 5px;"+\
                    "border-radius: 0px 10px 10px 0;"+\
                    "font-size: 10pt;"+\
                    "height: 21px;}"+\
                ".plugin_phanterimages_alvo_visualizar_imagem {"+\
                    "position: fixed;"+\
                    "z-index: 1005;"+\
                    "right: 68px;"+\
                    "top: 66px;"+\
                    "background-color: white;"+\
                    "padding: 10px;}"+\
                ".plugin_phanterimages_arranjo_caixa_visualizar {"+\
                    "position: absolute;"+\
                    "right: -16px;"+\
                    "top: 1px;"+\
                    "color: white;"+\
                    "font-size: 16pt;}"+\
                ".plugin_phanterimages_barra_de_progresso {"+\
                    "padding: 10px 20px 0 20px;"+\
                    "height: 28px;}"+\
                ".plugin_phanterimages_progress {"+\
                    "position: relative;"+\
                    "height: 6px;"+\
                    "display: none;"+\
                    "width: 100%;"+\
                    "background-color: #acece6;"+\
                    "border-radius: 2px;"+\
                    "background-clip: padding-box;"+\
                    "margin: 0.5rem 0 1rem 0;"+\
                    "overflow: hidden;}"+\
                ".plugin_phanterimages_progress .plugin_phanterimages_determinate {"+\
                    "position: absolute;"+\
                    "background-color: inherit;"+\
                    "top: 0;"+\
                    "bottom: 0;"+\
                    "background-color: #26a69a;"+\
                    "transition: width .3s linear; }"+\
                ".plugin_phanterimages_progress .plugin_phanterimages_indeterminate {"+\
                    "background-color: #26a69a; }"+\
                ".plugin_phanterimages_progress .plugin_phanterimages_indeterminate:before {"+\
                    "content: '';"+\
                    "position: absolute;"+\
                    "background-color: inherit;"+\
                    "top: 0;"+\
                    "left: 0;"+\
                    "bottom: 0;"+\
                    "will-change: left, right;"+\
                    "-webkit-animation: indeterminate 2.1s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite;"+\
                    "animation: indeterminate 2.1s cubic-bezier(0.65, 0.815, 0.735, 0.395) infinite; }"+\
                ".plugin_phanterimages_progress .plugin_phanterimages_indeterminate:after {"+\
                    "content: '';"+\
                    "position: absolute;"+\
                    "background-color: inherit;"+\
                    "top: 0;"+\
                    "left: 0;"+\
                    "bottom: 0;"+\
                    "will-change: left, right;"+\
                    "-webkit-animation: indeterminate-short 2.1s cubic-bezier(0.165, 0.84, 0.44, 1) infinite;"+\
                    "animation: indeterminate-short 2.1s cubic-bezier(0.165, 0.84, 0.44, 1) infinite;"+\
                    "-webkit-animation-delay: 1.15s;"+\
                    "animation-delay: 1.15s; }"+\
                "@-webkit-keyframes indeterminate {"+\
                    "0% {left: -35%; right: 100%; }"+\
                    "60% {left: 100%; right: -90%; }"+\
                    "100% {left: 100%; right: -90%; } }"+\
                "@keyframes indeterminate {"+\
                    "0% {left: -35%; right: 100%; }"+\
                    "60% {left: 100%; right: -90%; }"+\
                    "100% {left: 100%; right: -90%; } }"+\
                "@-webkit-keyframes indeterminate-short {"+\
                    "0% {left: -200%; right: 100%; }"+\
                    "60% {left: 107%; right: -8%; }"+\
                    "100% {left: 107%; right: -8%; } }"+\
                "@keyframes indeterminate-short {"+\
                    "0% {left: -200%; right: 100%; }"+\
                    "60% {left: 107%; right: -8%; }"+\
                    "100% {left: 107%; right: -8%; } }"+\
                ".plugin_phanterimages_progress.actived{"+\
                    "display: block;}"+\
                ".plugin_phanterimages_caixa_barraprogresso {"+\
                    "position: absolute;"+\
                    "bottom: 56px;"+\
                    "width: 100%;"+\
                    "z-index: 1004;}"+\
                ".plugin_phanterimages-branco {fill: white;}"+\
                ".plugin_phanterimages-preto {fill: black;}"+\
                ".plugin_phanterimages-cinza {fill: grey;}"+\
                ".plugin_phanterimages-gelo {fill: #dedada;}"+\
                "svg:hover .plugin_phanterimages-botao-icone {fill: orange;}"+\
                ".plugin_phanterimages_botao_padrao-container:hover {background-color: #f5edcd;}"+\
                ".plugin_phanterimages_botao_padrao-container:hover .plugin_phanterimages-botao-icone {fill: orange;}"+\
                ".plugin_phanterimages_imagem-visualizada img {box-shadow: 2px 2px 10px grey;}"+\
                ".plugin_phanterimages_imagem_visualizar-painel-botoes {"+\
                    "position: absolute;"+\
                    "top: 5px;"+\
                    "right: 5px;"+\
                    "cursor: pointer;}"+\
                "\n/*Fim plugin_PhanterImages*/\n"

        if humano:
            meucss=meucss.replace("{", "{\n\t\t").replace(";", ";\n\t\t").replace(";\n\t\t}", ";\n\t}\n\t").replace(";\n\t}\n\t\n/*", ";\n\t}\n/*")
        return XML(meucss)

    def execJSDepoisdeCortar(self, javascript):
        self.callbackOnCut=javascript

    def mudarNomeBotao(self, nome, texto_lendo='Fazendo Upload'):
        self.texto_lendo=texto_lendo
        self.nome_do_botao=nome
        self.html_btn_padrao=DIV(XML(self.botao_upload), DIV(self.nome_do_botao, _class='plugin_phanterimages_titulo_botao_padrao'),_class='plugin_phanterimages_botao_padrao')

    def uploadArea(self):
        return DIV(self._uploadArea(), _id="plugin_phanterimages_main-container")

    def visualizarImagem(self, id_imagem):
        return DIV(self._uploadAreaImagem(id_imagem), _id="plugin_phanterimages_main-container")

    def xml(self):
        if self.html_botao:
            return "%s" %DIV(self.html_botao, _id="plugin_phanterimages_main-container")
        else:
            return "%s" %DIV(self._uploadArea(), _id="plugin_phanterimages_main-container")



