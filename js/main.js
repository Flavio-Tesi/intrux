var user = true;
var light = true;
var intrusion = true;
var pwd = true;

function query_readtemperatures() {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_temp" },
		success: function (data) {
			obj = jQuery.parseJSON(data);
			testo="<table class='basic'>";
			testo+="<tr>";
			testo+="<th>";
			testo+="Stanza";
			testo+="</th>";
			testo+="<th>";
			testo+="Valore";
			testo+="</th>";
			testo+="<th>";
			testo+="Data";
			testo+="</th>";
			testo+="</tr>";
			for (x in obj) {
				testo+="<tr>";
				testo+="<td>";
				testo+="<button id = \"visual_roomTemp";
				number_id = obj[x][1];
				testo+=number_id.toString();
				testo+= "\""
				testo+= ">"
				testo+= query_readroom([x][1]);
				testo+= "</button>";
				testo+="</td>";
				testo+="<td>";
				testo+=obj[x][2];
				testo+="</td>";
			
				testo+="<td>";
				testo+="<button id = \"visual_dateTemp";
				number_id = obj[x][3];
				testo+=number_id.toString();
				testo+= "\""
				testo+= ">"
				testo+= query_readroom([x][3]);
				testo+= "</button>";
				testo+="</td>";
			
				testo+="</tr>"; 
			}
			$("#tab_temperature").html(testo).hide().slideDown();
		}
	});
}

function query_readroom(i) {
	$.ajax({
		url: "/execute",
		type: "get",
		data: { cmd: "read_room",
			id: i },
		success: function(data) { return data; }
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
	/*	testo+= "<input type=\"text\" readonly id = \"pwd_txt\" size=\"25\"/>"		*/
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
	/*		$("#pwd_txt").val(data);		*/
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
					testo+=obj[x][1];
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
	$("#temperatures_button").click(function(){query_readtemperatures(); });
});
