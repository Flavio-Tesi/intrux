var user = true;
var light = true;
var intrusion = true;
var pwd = true;
var temp = true;
var temp2 = true;

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
			if (!temp) {
				$("#tab_log_temperature").hide();
				temp = !temp
				temp2 = true;
			}
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
				$("#tab_log_temperature").html(testo).hide().slideDown();
				temp = !temp
				temp2 = true;
			}
			
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
				temp = true;
				var canvas = document.getElementById('grafico');
				var ctx = canvas.getContext('2d');
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				ctx.beginPath();
		//		canvas.width = canvas.width;

			}
			else if (data == "INSERIRE UNA DATA DI INIZIO" || data == "INSERIRE UNA DATA DI FINE") alert(data);
			else {
				
				
				
				obj = jQuery.parseJSON(data);
				var j = 0;
				
				for (x in obj) if (obj[x][1]>j) j =obj[x][1];
				
				var colors = new Array (["black"], ["blue"], ["red"], ["green"], ["orange"], ["light blue"], ["brown"], ["yellow"], ["pink"], ["violet"]);
				var array = new Array();
				var asseY = new Array();
				var asseX = new Array();
				var	tooltips = new Array();
				var keys = new Array();
				var i;
				
				for (k=0; k<j; k++) {
					i = 0;
					array[k] = new Array();
					asseY[k] = new Array();
					asseX[k] = new Array();
					tooltips[k] = new Array();
					for (x in obj) {
						if (obj[x][1] == k+1) {
							array[k][i] = obj[x];
							i++;
						}
					}
				}
				
				
				for (k=0; k<j; k++) {
					if (typeof(array[k][0])!="undefined") {
						var i = k+1;
						keys[k]= ["stanza numero " + i];
					}
					for (z=0; z<array[k].length; z++) {
						asseY[k][z]=array[k][z][2];
						asseX[k][z]=array[k][z][3];
						tooltips[k][z]=(array[k][z][2]).toString() +" gradi, il giorno "+ (array[k][z][3]).toString() +", alle ore "+ (array[k][z][4]).toString();
						
					}
				}
				
				var max = 100;
								
				for (k=0; k<j; k++) { 									
					var graphTemp = new RGraph.Line('grafico', asseY[k]);
					graphTemp.Set('ylabels', false);
					graphTemp.Set('background.grid', true);
					graphTemp.Set('colors', colors[k]);
					graphTemp.Set('linewidth', 5);
					graphTemp.Set('hmargin', 5);
					graphTemp.Set('labels', asseX[k]);
					graphTemp.Set('tooltips', tooltips[k]);
					graphTemp.Set('tooltips.event', 'onmousemove');
					graphTemp.Set('chart.key', keys[k]);
					graphTemp.Set('chart.key.position', 'gutter');
					graphTemp.Set('chart.key.position.gutter.boxed', false);
					graphTemp.Set('chart.key.position.x', ((graphTemp.canvas.width - 115 + 250*k) / 2) - 25);
					
					graphTemp.Draw();
			//		RGraph.Effects.Line.Trace2(graphTemp);
					
					if (typeof(array[k][0])!="undefined") {
						var yaxis = new RGraph.Drawing.YAxis('grafico', 20*(k+1));
						yaxis.Set('colors', colors[k]);
						yaxis.Set('text.color', 'black');
						yaxis.Set('chart.max', max);
						yaxis.Draw();
					}
				}

				
				temp2 = !temp2;
				temp = true;
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
			testo+="<p>Da Data: <input type=\"text\" id=\"datepickerinit\" /></p>";
			testo+="<p>A Data: <input type=\"text\" id=\"datepickerend\" /></p>";
			testo+="<button id=\"show_temp\">mostra log temperature</button>";
			testo+="<button id=\"show_tempGraph\">mostra grafico temperature</button>";
			testo+="<script> $(function() { $( \"#datepickerinit\" ).datepicker();	});	</script>";
			testo+="<script> $(function() { $( \"#datepickerend\" ).datepicker();	});	</script>";
			
			$("#tab_temperature").html(testo).hide().slideDown();
		
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
			if (user) {
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
			else $("#tab_utenti").hide();
			user = !user
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
			if (light) {
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
			else $("#tab_luci").hide();
			light = !light;
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

$(document).ready(function() {
    $("#tabs").tabs();
	$("#readusers_button").click(function(){ query_readusers(); });
	$("#readintrusions_button").click(function(){ query_readintrusions(); });
	$("#readlights_button").click(function(){ query_readlights(); });
	query_readrooms();
});
