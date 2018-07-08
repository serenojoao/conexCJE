// pdv
function ehNumero(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}
function filtrarCeQ(valor, padrao=""){
	var	valor = valor+"";
	var padrao = padrao;
	var novo_valor = "";
	for (var i = 0; i < valor.length; i++) {
		console.log(valor[i])
		if(ehNumero(valor[i])){
			novo_valor=novo_valor+""+valor[i]
		}
	}
	if (novo_valor==""){
		return padrao
	}
	return novo_valor
}
shortcut.add("Ctrl+F",function() {
	$("#btn_localizar_pdv")[0].click();
});
shortcut.add("Ctrl+P",function() {
	$("#botao_imprimir")[0].click();
	$("#btn_imprimir_pdv")[0].click();

});
shortcut.add("F6",function() {
	$("#btn_principal_pdv")[0].click();
});
shortcut.add("F7",function() {
	$("#btn_cancelar_pdv")[0].click();
});
shortcut.add("F8",function() {
	$("#btn_cliente_pdv")[0].click();
});

$("#btn_quantidade_pdv").on('click',function(){
	$("#quant_pdv").focus().select();
});
function pdv_cond_barra_send(cod_barra){
	var url_ajax = $('#cod_barras_pdv').attr("url-ajax")
	var tot_itens = $('#cod_barras_pdv').attr("data-tot-itens")
	var tot_preco = $('#cod_barras_pdv').attr("data-tot-preco")
	var quant = $('#quant_pdv').val();
	$('#quant_pdv').val("1");
	url_ajax=url_ajax+"/"+cod_barra+"/"+quant+"/"+tot_itens+"/"+tot_preco
	console.log(url_ajax)
	ajax(url_ajax,[], ":eval")

};
$("#pdvmodal2").on("shown.bs.modal", function(){
	$('#modal_quant_pdv').focus();
	$('#modal_quant_pdv').select();
});
function adc_cod_barra(cod_barra, url_image){
	$('#view_modal_item_pdv').css("background-image", "url('"+url_image+"')");
	$('#cod_barras_pdv').val(cod_barra);
	$('#pdvmodal').modal('hide');
	$('#pdvmodal2').modal('show');
	$('#modal_quant_pdv').focus();
	$('#modal_quant_pdv').select();
	$("#confirmar_modal").unbind("click").on("click", function(){
		var quant_mo = $("#modal_quant_pdv").val();
		$("#quant_pdv").val(quant_mo);
		pdv_cond_barra_send(cod_barra);
		$('#pdvmodal2').modal('hide');

	});
}

 $('#cod_barras_pdv').on("keyup", function(e){
	var valor =  $('#cod_barras_pdv').val()
	var novo_valor = filtrarCeQ(valor)
 	if(e.keyCode == 13){
 		if (novo_valor!=""){
 			pdv_cond_barra_send(novo_valor);
 		}
 	} else {
 		if (e.keyCode == 81){
 			$("#quant_pdv").focus().select();
 		}
 	}
 	$('#cod_barras_pdv').val(novo_valor);
 });

 $('#quant_pdv').on("keyup", function(e){
 	var valor =  $('#quant_pdv').val()
	var novo_valor = filtrarCeQ(valor, "1")
 	if(e.keyCode == 13){
 		$("#cod_barras_pdv").focus().select();
 	} else {
 		if (e.keyCode == 81){
 			$("#cod_barras_pdv").focus().select();
 		}
 	}
 	$('#quant_pdv').val(novo_valor);
 });
 $("#modal_total_pago").on("keyup", function(e){
 	var a_pagar = parseFloat($("#total_pdv_modal").text());
 	var desconto = parseFloat($("#modal_desconto").val());
 	var pago = parseFloat($("#modal_total_pago").val());
 	var diferenca = pago+desconto-a_pagar
 	console.log(diferenca)
 	if (diferenca>=0.0){
 		$("#troco_pdv_modal").text(diferenca.toFixed(2));
 		$("#confirmar_modal3").removeClass("disabled");
 		$("#confirmar_modal3").addClass("enabled");
 		$("#confirmar_modal3").unbind().on('click', function(){
 			$('#pdvmodal3').modal('hide');
 			var url_base = $("#confirmar_modal3").attr("data-url-base")
 			var id_vendas = $("#cod_barras_pdv").attr("data-id-venda")
 			var url_ajax=url_base+"/"+id_vendas+"/"+a_pagar+"/"+pago+"/"+diferenca+"/"+desconto
 			console.log(url_ajax)
 			ajax(url_ajax,[],":eval")
 		});
 	} else {
 		$("#troco_pdv_modal").text("0.00");
 		$("#confirmar_modal3").addClass("disabled");
 		$("#confirmar_modal3").removeClass("enabled");
 		$("#confirmar_modal3").unbind();
 	}

 });

function finalizando_compra(){
 	$("#pdvmodal4").modal("show");
}
$('#pdvmodal4').on('hidden.bs.modal', function (e) {
  window.location="/conexcje/servicos/pdv/avulso"
});
$('#confirmar_modal4').on('click', function(){
	$("#pdvmodal4").modal("hide");
})
$('#confirmar_cancelamento').on('click', function(){
	var id_vendas = $("#cod_barras_pdv").attr("data-id-venda");
	var url_ajax = "/conexcje/echos/cancelar_venda/"+id_vendas
	console.log(url_ajax)
	ajax(url_ajax, [], ":eval")
	
});
$("#btn_cancelar_pdv").on("click", function(){
	$("#modal_cancelar").modal("show");
});
function fechar_toast_depois(){
    var fechar = function local(){
      $(".toast").fadeOut();
    }
    setTimeout(fechar, 3000);
  }
