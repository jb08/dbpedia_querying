
<?php 
	header('Access-Control-Allow-Origin: *');
	header('Access-Control-Allow-Methods-Methods: GET, POST, OPTIONS');
	header("Access-Control-Allow-Headers: X-Requested-With"); 
	
	//Modified from John Wright's code at http://johnwright.me/code-examples/sparql-query-in-code-rest-php-and-json-tutorial.php
	function getURLDBPedia () {
		$format = 'json';

		$query = "
		SELECT ?book 
		WHERE { ?book dbp:pages 1216 }";

		$searchUrl = "http://dbpedia.org/sparql?"."query=".urlencode($query)."&format=".$format;
		return searchUrl;
	}

	function request($url) {
		if (!function_exists('curl_init')) {
			die('Curl is not installed.')
		}

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);

		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		$response = curl_exec($ch);
		curl_close($ch);
		return $response;
	}

	$requestURL = getURLDBPedia();
	$responseArray = json_decode(request($requestURL), true);
	return $responseArray;

	//Look up that tutorial and implement
	//Modify ajax to return json with results


?>

