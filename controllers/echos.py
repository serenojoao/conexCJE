def dados_cnpj():
	if request.args(0):
		import urllib2
		import json
		aberto = urllib2.urlopen("https://www.receitaws.com.br/v1/cnpj/%s" %request.args(0))
		html=aberto.read()
		return response.json(json.loads(html))