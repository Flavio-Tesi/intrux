<?
// Gateway PHP per effettuare query SQL verso il DB $db
// Versione che usa le API mysqli


// Converte una stringa di testo in una stringa di testo contenente
// numeri esadecimali
function textstring2hexstring($textstring) {
	$hexstring = "";
	for ($i=0;$i<strlen($textstring);$i++)
		$hexstring.=sprintf("%02x",ord($textstring[$i]));
	return $hexstring;
}

// Converte una stringa di testo di numeri esadecimali in una scringa di testo
// numeri esadecimali
function hexstring2textstring($hexstring) {
	$rtc=var_export(hex2bin2($hexstring),true);
	return(substr($rtc,1,-1));
}


// hex2bin2
// Convert a hex-string to binary-string (the way back from bin2hex)
// Read more: http://www.webmastertalkforums.com/php-functions/17175-php-hex2bin-function-convert-hexadecimal-into-binary.html#ixzz29N3Ac4rB

function hex2bin2($h) {
	if (!is_string($h)) 
		return null;
	$r='';
	for ($a=0; $a<strlen($h); $a+=2) { 
		$r.=chr(hexdec($h{$a}.$h{($a+1)})); 
	}
	return $r;
}  


foreach ( $_POST as $key => $value) $$key=$value;
foreach ( $_GET as $key => $value) $$key=$value;

if (!isset($cmd)) die("Specificare cmd");
$response="";

// Invio di una query a MySQL e risposta in formato json  
if ($cmd=="query") {
	if (!isset($db)) die("Specificare db");

	$mysqli = new mysqli("localhost", "crm", "netusg20", $db);


	if (!isset($query)) {
		$mysqli->close();
		die("Specificare query");
	}
	$single_queries=explode(";",$query);

	foreach($single_queries as $SQL_single_query) {
		if ($result=$mysqli->query($SQL_single_query)) {
			if ($mysqli->affected_rows>0) {
				if (is_object($result)) {
					$response="[";	
					while ($row = $result->fetch_object()) {
						$response.=json_encode($row,JSON_FORCE_OBJECT);
						$response.=",";	
					}
					$response[strlen($response)-1]="]";	
					$result->close();
					$mysqli->next_result();
				}	
			}
		}
	}
	$mysqli->close();
	die($response);
}

// Invio di una query a MySQL i cui campi sono stati trasformati in HEXASCII  
if ($cmd=="queryhex") {
	if (!isset($db)) die("Specificare db");

	$mysqli = new mysqli("localhost", "crm", "netusg20", $db);

	if (!isset($query)) {
		$mysqli->close();
		//die("Specificare query");
		die;	
	}
	if (strlen($query)==0) {
		$mysqli->close();
		//die("Query vuota");
		die;
	}	
	
	//echo "query=$query<br/>";
	$query_text=hexstring2textstring($query);
	//echo "query_text=$query_text<br/>";
	$single_queries=explode(";",$query_text);

	$response="";
	foreach($single_queries as $SQL_single_query) {
		//echo "SQL_single_query=$SQL_single_query<br/>";
		if ($result=$mysqli->query($SQL_single_query)) {
			if ($mysqli->affected_rows>0) {
				if (is_object($result)) { 
					$response="[";	
					while ($row = $result->fetch_object()) {
						$response.=json_encode($row,JSON_FORCE_OBJECT);
						$response.=",";	
					}
					$response[strlen($response)-1]="]";	
					$result->close();
					$mysqli->next_result();
				}	
			}
		}
	}
	$mysqli->close();
	//echo $response;
	die(textstring2hexstring($response));
}


?>
