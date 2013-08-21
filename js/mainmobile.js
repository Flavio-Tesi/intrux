var light = true;
var intrusion = true;
var pwd = true;
var temp = true;
var temp2 = true;
var cam = "";

function query_temproom(){
	rm = selectroom.value;
	di = datepickerinit.value;
	df = datepickerend.value;
	if (rm == "Tutte") rm = "xx"
	if (di == "") di = "xx"
	if (df == "") df = "xx"	
	$.ajax({
		url: "/execute",
		type: "get",
		data: { 
			cmd: "temp_room",
			rm: rm,
			di: di,
			df: df
		},
		success: function (data) {
			if (!temp) $("#log_temperature").hide();
			else if (data == "INSERIRE UNA DATA DI INIZIO" || data == "INSERIRE UNA DATA DI FINE") alert(data);
			else {
				obj = jQuery.parseJSON(data);
				testo="<table class='basic'>";
				testo+="<tr>";
				testo+="<th>";
				testo+="Temperatura";
				testo+="</th>";
				testo+="<th>";
				testo+="Data";
				testo+="</th>";
				testo+="<th>";
				testo+="Ora";
				testo+="</th>";
				testo+="</tr>";
				for (x in obj) {
					testo+="<tr>";
					testo+="<td>";
					testo+=obj[x][2];
					testo+="</td>";
					testo+="<td>";
					testo+=obj[x][3];
					testo+="</td>";
					testo+="<td>";
					testo+=obj[x][4];
					testo+="</td>";
					testo+="</tr>"; 
				}
				testo+="</table>";
				$("#log_temperature").html(testo).hide().slideDown();
				
			}
			temp = !temp
		}
	});
	
}

function query_temproomgraph() {
	rm = selectroom.value;
	di = datepickerinit.value;
	df = datepickerend.value;
	if (rm == "Tutte") rm = "xx"
	if (di == "") di = "xx"
	if (df == "") df = "xx"	
	$.ajax({
		url: "/execute",
		type: "get",
		data: { 
			cmd: "temp_room",
			rm: rm,
			di: di,
			df: df
		},
		success: function (data) {
			if (!temp2) {
				temp2 = !temp2
				document.getElementById("container").innerHTML = "";

			}
			else if (data == "INSERIRE UNA DATA DI INIZIO" || data == "INSERIRE UNA DATA DI FINE") alert(data);
			else {
				
				obj = jQuery.parseJSON(data);
				console.log (obj[0]);
				var j = 0;
				
				for (x in obj) if (obj[x][1]>j) j = obj[x][1];
				
				var array = new Array();
				var temperature = new Array();
				var	tooltips = new Array();
				var i;
				
				for (k=0; k<j; k++) {
					i = 0;
					array[k] = new Array();
					temperature[k] = new Array();
					tooltips[k] = new Array();
					for (x in obj) {
						if (obj[x][1] == k+1) {
							array[k][i] = obj[x];
							i++;
						}
					}
				}
				
				
				for (k=0; k<j; k++) {
					for (z=0; z<array[k].length; z++) {
						temperature[k][z]=array[k][z][2];
						tooltips[k][z]=(array[k][z][3]).toString() + "<br/>" + (array[k][z][4]).toString();
						
					}
				}
				
								
								
				$(function () {
						$('#container').highcharts({
							title: {
								text: 'Temperature',
								x: -20 //center
							},
							xAxis: {
								categories: tooltips[0]
							},
							yAxis: {
								title: {
									text: 'Gradi Celsius'
								},
								plotLines: [{
									value: 0,
									width: 1,
									color: '#808080'
								}]
							},
							tooltip: {
								formatter: function() {
									return Highcharts.numberFormat(this.y, 0) + "gradi" + '<br/>'+'in data: '+ this.x;
								}

							},
							legend: {
								layout: 'vertical',
								align: 'right',
								verticalAlign: 'middle',
								borderWidth: 0
							},
							series: [{
								name: 'Camera',
								data: temperature[0]
							}, {
								name: 'Cameretta',
								data: temperature[1]
							}, {
								name: 'Cucina',
								data: temperature[2]
							}, {
								name: 'Sala',
								data: temperature[3]
							}]
						});
					});
				
				temp2 = !temp2;
			}
		}
	});
}

function query_readrooms() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_rooms"},
		success: function (data) {
			obj = jQuery.parseJSON(data);
			testo ="Stanza: <select id = \"selectroom\"> <option>Tutte</option>";
			for (x in obj) {
				testo+="<option>";
				testo+=obj[x][0];
				testo+=". "
				testo+=obj[x][1];
				testo+="</option>";
			}
			testo+="</select>";
			
			testo+="<label for=\"datepickerinit\">Da Data:</label>"
			testo+="<input type=\"date\" data-clear-btn=\"false\" name=\"date-1\" id=\"datepickerinit\" value=\"\">"
			testo+="<label for=\"datepickerend\">A Data:</label>"
			testo+="<input type=\"date\" data-clear-btn=\"false\" name=\"date-2\" id=\"datepickerend\" value=\"\">"
			
			
			$("#par_temp").html(testo).hide().slideDown();
		
			$("#show_temp").click(function(){query_temproom(); });
			$("#show_tempGraph").click(function(){query_temproomgraph(); });
		}
	});
}

function query_readusers() {	
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_users" },
		success: function(data) {
				obj = jQuery.parseJSON(data);
				testo="<table class='basic'>";
				testo+="<tr>";
				testo+="<th>";
				testo+="Nome";
				testo+="</th>";
				testo+="<th>";
				testo+="Codice";
				testo+="</th>";
				testo+="</tr>";
				for (x in obj) {
					testo+="<tr>";
					testo+="<td>";
					testo+=obj[x][1];
					testo+="</td>";
					testo+="<td>";
					testo+=obj[x][2];
					testo+="</td>";
					testo+="<td>";
					testo+="<button id = \"change_code_";
					number_id = obj[x][0];
					testo+=number_id.toString();
					testo+= "\""
					testo+= ">cambia password</button>";
					testo+="</td>";
					testo+="</tr>"; 
				}
				testo+="</table>";
				$("#tab_utenti").html(testo).hide().slideDown();
				
				$("#change_code_1").click(function(){ setusercode(1); });
				$("#change_code_2").click(function(){ setusercode(2); });
		}
	});
}	

function setusercode(i) {
	if (pwd) {
		testo = "inserisci la tua vecchia password <input id=\"pwd0\" type=\"password\" size=\"17\" maxlength=\"10\" /> <br>";
		testo+= "inserisci la tua nuova password <input id=\"pwd1\" type=\"password\" size=\"17\" maxlength=\"10\" /> <br>";
		testo+= "inserisci nuovamente la tua nuova password <input id=\"pwd2\" type=\"password\" size=\"17\" maxlength=\"10\" /> <br>";
		testo+= "<button id=\"conferma\">conferma</button>"
		$("#pwd_mod").html(testo).hide().slideDown();
		$("#conferma").click(function(){ query_setusercode(i); });
	}
	else $("#pwd_mod").hide();
	pwd = !pwd;
}

function query_setusercode(i) {
	x = $("#pwd0").val();
	y = $("#pwd1").val();
	z = $("#pwd2").val();
	if (!Number(x)) x = "a";
	if (!Number(y)) y = "a";
	if (!Number(z)) z = "a";
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "set_usercode",
		id: i,
		pwd0: x,
		pwd1: y,
		pwd2: z 
		},
		success: function(data) { 
			query_readusers();
			query_readusers();
			$("#pwd0").val("");
			$("#pwd1").val("");
			$("#pwd2").val("");
			alert(data);
		}
	});
}
	
function query_readlights() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_lights" },
		success: function(data) {
			
				obj = jQuery.parseJSON(data);
				testo="<table class='basic'>";
				testo+="<th>";
				testo+="Stanza";
				testo+="</th>";
				testo+="<th>";
				testo+="Stato";
				testo+="</th>";
				testo+="</tr>";
				for (x in obj) {
					testo+="<tr>";
					testo+="<td>";
					testo+=obj[x][4];
					testo+="</td>";
					testo+="<td>";				
					testo+="<button id = \"change_light_";
					number_id = obj[x][0];
					status = obj[x][2];
					testo+=number_id.toString();
					testo+= "\""
					if (status == 0) {
						testo+= "style=\"background-color:red\"";
					}
					else {
						testo+= "style=\"background-color:green\"";
					}
					testo+= ">on/off</button>"; 
					testo+="</td>";
					testo+="</tr>"; 
				} 
				testo+="</table>";
				$("#tab_luci").html(testo).hide().slideDown();
				$("#change_light_1").click(function(){ query_changelight(1); });
				$("#change_light_2").click(function(){ query_changelight(2); });
				$("#change_light_3").click(function(){ query_changelight(3); });
				$("#change_light_4").click(function(){ query_changelight(4); });
			
		}
	});
}

function query_changelight(i) {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "change_light",
		id: i },
		success: function(data) { query_readlights(); query_readlights(); }
	});
}

function query_readintrusions() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_intrusions" },
		success: function(data) {
			obj = jQuery.parseJSON(data);
			testo="<table class='basic'>";
			testo+="<th>";
			testo+="Stanza";
			testo+="</th>";
			testo+="<th>";
			testo+="Stato";
			testo+="</th>";
			testo+="</tr>";
			for (x in obj) {
				testo+="<tr>";
				testo+="<td>";
				testo+=obj[x][6];
				testo+="</td>";
				testo+="<td>";		
				testo+="<div align=\"center\"><div style=\"display: table-cell; text-align: center; vertical-align: middle; font-size: 12px; font-weight: bold;" 
				status = obj[x][2];
				if (status == 1) {
					testo+= "background-color:red;";
				}
				else {
					testo+= "background-color:green;";
				}
				testo+= "width: 25px; height: 25px; -moz-border-radius: 200px; border-radius: 200px; -webkit-border-radius: 200px;\"></div></div>"; 
				testo+="</td>";
				testo+="</tr>"; 
			} 
			testo+="</table>";
			$("#tab_intrusioni").html(testo).hide().slideDown();
		}
	});
}

function stop_allarme() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "stop_allarme" },
		success: function(data) { 
			query_readintrusions();
			alert ("allarme fermato"); }
	});
}

function start_allarme() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "start_allarme" },
		success: function(data) {
			alert ("allarme avviato");
		 }
	});
}

function on_cam() {
	h = $(window).height();
	w = $(window).width();
	if (h > w) alert("ruotare lo schermo!")
	else {
		$.ajax({
			url: "/execute",
			type: "get",
			data: { cmd: "on_cam" },
			success: function(data) { 
				cam = "lq"
				visualizza_cam(480, 640);
			}
		});
	}
}
	
function on_cam_hd() {
	h = $(window).height();
	w = $(window).width();
	if (h > w) alert("ruotare lo schermo!")
	else {
		$.ajax({
			url: "/execute",
			type: "get",
			data: { cmd: "on_cam_hd" },
			success: function(data) { 
				cam = "hd"
				visualizza_cam(720, 1280);
			}
		});
	}
}
	
function off_cam(){
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "off_cam" },
		success: function(data) {
			$("#frame_cam").hide();
		}
	});
}
	
function visualizza_cam(height, width) {
		testo = "<div><button id=\"record\">registra</button></div>"
		testo+= "<iframe src=\"http://192.168.1.104:8181/stream_simple.html\" scrolling=\"auto\" frameborder=\"1\" align=center	marginheight=\"0px\" marginwidth=\"0px\"";
		testo+= "height=\"";
		testo+=	height;
		testo+= "\" width=\"";
		testo+= width;
		testo+= "\"></iframe>";
		$("#frame_cam").html(testo).hide().slideDown();
		$("#record").click(function(){ registra(); });
}

function registra() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "record_video" },
		success: function(data) {
			testo = "<div><button id=\"stop_record\">ferma la registrazione</button></div>"
			$("#frame_cam").html(testo).hide().slideDown();
			$("#stop_record").click(function(){ stop_registrazione(); });
		}
	});
}

function stop_registrazione() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "stop_record_video" },
		success: function(data) {
			console.log (cam);
			if (cam == "lq") on_cam();
			else if (cam == "hd") on_cam_hd();
		}
	});
}

function video() {	
	testo = "<iframe src=\"http://192.168.1.104/video\" scrolling=\"auto\" frameborder=\"1\" align=center	marginheight=\"0px\" marginwidth=\"0px\"";
	testo+= "height=\"";
	testo+=	640;
	testo+= "\" width=\"";
	testo+= 1200;
	testo+= "\"></iframe>";
	$("#directory").html(testo).hide().slideDown();
}

function logout() {
	window.location = "/login.html";
	document.cookie = "nome_autenticazione=";
}

$(document).ready(function() {
	$("#utenti").click(function(){ query_readusers(); });
	$("#intrusioni").click(function(){ query_readintrusions(); });
	$("#luci").click(function(){ query_readlights(); });
	$("#confermaLogin").click(function(){ query_verifyuser(); });
	$("#button_log_temperature").click(function(){ query_temproom(); });
	$("#button_graph_temperature").click(function(){ query_temproomgraph(); });
	$("#ferma_allarme").click(function(){ stop_allarme(); });
	$("#avvia_allarme").click(function(){ start_allarme(); });
	$("#on_cam").click(function(){ on_cam(); });
	$("#on_cam_hd").click(function(){ on_cam_hd(); });
	$("#off_cam").click(function(){ off_cam(); });
	$("#video").click(function(){ video(); });
	$("#logout").click(function(){ logout(); });
	query_readrooms();
});
