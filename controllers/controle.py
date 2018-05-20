# -*- coding: utf-8 -*-
def index():
    html=DIV(
        DIV(
            DIV(
                a(_href=URL("listas", "associados"), _class="icon fa fa-user-o"),
                _class="col-4"),
            _class="row"),
        _class="container")
    return locals()