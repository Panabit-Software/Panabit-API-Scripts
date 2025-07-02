<?php
$ip = "panabitip";
$username = "user";
$password = "pwd";
$file = "path for metrics";
$int = "interface";

$int_up = "${int}_upbps";
$int_down = "${int}_downbps";

while(true) {
	$url = "https://$ip/api/panabit.cgi";
	$data = "api_action=api_login&username=${username}&password=${password}";
	$result = httpPost($url,$data);
	$result = iconv("GBK","UTF-8",$result);
	$jresult = json_decode($result);
	$code = @$jresult->code;
	if($code == 0) {
		$token = @$jresult->data;
	} else {
		die();
	}
	for($i=0;$i<200;$i++) {
		$data = "api_route=system@sys_info&api_action=load_sys_env&api_token=$token";
		$result = httpPost($url,$data);
		$result = iconv("GBK","UTF-8",$result);
		$jresult = json_decode($result, true);
		$up = @$jresult[$int_up];
		$down = @$jresult[$int_down];
		$fp = fopen("$file",'w+');
		fwrite($fp,"panabit_out $up\npanabit_in $down\n");
		fclose($fp);
		sleep(5);
	}
}

function httpPost($url, $data) {
        $ch = curl_init ();
        curl_setopt ( $ch, CURLOPT_URL, $url );
        curl_setopt ( $ch, CURLOPT_POST, 1);
        curl_setopt ( $ch, CURLOPT_HEADER, 0);
        curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt ( $ch, CURLOPT_BINARYTRANSFER, 1);
        curl_setopt ( $ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt ( $ch, CURLOPT_TIMEOUT, 5);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        $return = curl_exec ( $ch );
        curl_close ( $ch );
        return $return;
}
?>
