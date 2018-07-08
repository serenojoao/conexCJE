# -*- coding: utf-8 -*-
import os

FOLDER_UPLOADS_TEMP=os.path.join(request.folder, 'uploads', 'plugin_phanterimages_uploads_temp')
if not os.path.exists(FOLDER_UPLOADS_TEMP):
	 os.makedirs(FOLDER_UPLOADS_TEMP)
	 
db.define_table('plugin_phanterimages_uploads_temp', 
    Field('imagem', 'upload', autodelete=True, uploadfolder=FOLDER_UPLOADS_TEMP),
    auth.signature
    )


FOLDER_UPLOADS=os.path.join(request.folder, 'uploads',  'plugin_phanterimages_uploads')
if not os.path.exists(FOLDER_UPLOADS):
	 os.makedirs(FOLDER_UPLOADS)

db.define_table('plugin_phanterimages_uploads',
    Field('imagem', 'upload', autodelete=True, uploadfolder=FOLDER_UPLOADS),
    Field('uploader', 'string', uploadfolder=FOLDER_UPLOADS),
    auth.signature
    )

from plugin_phanterimages.phanterimages import PhanterImages

# o método estático PhanterImages.css() retorna o css original sem modificações, ou seja, caso seja alterado o plugingphanterimage.css
# pode-se retornar aos valores defaults com esse método.
response.css=PhanterImages.css()

# O tamanho do corte deve ser uma tupla com a largura e a altura respectivamente
MODELS_PHANTERIMAGES_EXAMPLE=PhanterImages(db, tamanho_corte=(700, 400))

# É aceito 2 parâmetros, o primeiro muda a nome do botão, o segundo muda a mensagem "fazendo upload" do mesmo botão.
MODELS_PHANTERIMAGES_EXAMPLE.mudarNomeBotao("Adicionar Imagem")


# Depois de cortar é enviado um objeto javascript com o atributo id e o atributo url da imagem que pode ser utilizado no stript do callback


MODELS_PHANTERIMAGES_EXAMPLE.execJSDepoisdeCortar('if($("#produtos_id_imagem option[value=\'"+response.id+"\']").length > 0){$("#produtos_id_imagem").val(response.id);}else{$("#produtos_id_imagem").append("<option value=\'"+response.id+"\' selected=\'selected\'>"+response.id+"</option>")};')

