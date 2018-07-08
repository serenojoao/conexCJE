# -*- coding: utf-8 -*-
# Autor: PhanterJR

def index():
    html=DIV(DIV(H1('Plugin PhanterImages. Seu álbum virtual.')),DIV(BUTTON("INICIAR UPLOADS", _class='btn btn-default', _onclick='window.location="%s"' %URL('upload_images'))), _class='background-teste')
    return locals()

@auth.requires_membership('funcionario')
def upload_images():
    html=MODELS_PHANTERIMAGES_EXAMPLE
    return dict(html=html)

@auth.requires_membership('funcionario')
def echo_phanterimages():
    echo_response=MODELS_PHANTERIMAGES_EXAMPLE.echoPhanterImages()

    if echo_response[0]:

        return response.json(echo_response[1])
    else:
        return echo_response[1]


