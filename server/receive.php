<?php

function isValidJSON($str) {
    json_decode($str, true);
    echo ("Last ERROR on " . $str . " = " . json_last_error());
    return json_last_error() == JSON_ERROR_NONE;
}

function mylog($str) {
    file_put_contents ("log", date('l jS \of F Y h:i:s A') . "   " . $str . "\n", FILE_APPEND);
}

echo ("Hey there!");

// READ DATA
$json_params = trim (file_get_contents("php://input"));
if (strlen($json_params) > 0 && isValidJSON($json_params)) {
    $decoded_params = json_decode($json_params, true);
    $time=$decoded_params["time"];
    $data=$decoded_params["data"];
    $lat=hexdec(substr($data,0,7))*1.0/100000-90.0;
    $lon=hexdec(substr($data,7,7))*1.0/100000-180.0;
    $pm1=hexdec(substr($data,14,2));
    $pm25=hexdec(substr($data,16,2));
    $pm10=hexdec(substr($data,18,2));
    $no2=hexdec(substr($data,20,2));
    $o3=hexdec(substr($data,22,2));
    $timestamp=$decoded_params["time"];
    $deviceid=$decoded_params["device"];

    mylog ("time = " . $time . ", lat = ".$lat.", lon = ".$lon.", pm1 = ".$pm1.", pm2.5 = ".$pm25.", pm10 = ".$pm10.", no2 = ".$no2.", o3 = ". $o3);

    // WRITE TO DB
    $servername="olivierkjlrespir.mysql.db";
    $username="olivierkjlrespir";
    $password="Respirea1";
    $database="olivierkjlrespir";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $database);

    // Check connection
    if ($conn->connect_error) {
        mylog ("Connection failed: " . $conn->connect_error);
    } else {
        mylog ("Connected successfully");
        $sql = "INSERT INTO airquality (deviceid, timestamp, lat, lng, pm1, pm25, pm10, no2, o3) VALUES ('" . $deviceid . "'," . $timestamp . "," . $lat . "," . $lon . "," . $pm1 . "," . $pm25 . "," . $pm10 . "," . $no2 . "," . $o3 . ")";
        mylog ($sql);
        if ($conn->query($sql) === TRUE) {
            mylog ("New record created successfully");
        } else {
            mylog ("Error: " . $sql . "<br>" . $conn->error);
        }
    }
} else {
    mylog ("Decoding failed");
    mylog ($json_params);
}
?>

