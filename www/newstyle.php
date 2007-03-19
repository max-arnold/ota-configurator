<?

require_once "oma.inc.php";

if ($_POST["kind"]) {
  Header("Location: http://".$_SERVER['HTTP_HOST'] 
                     .dirname($_SERVER['PHP_SELF']) 
                     ."/?u=1");
} else {

$r = OMASendMsg($_POST["number"], $_POST["manufacturer"], $_POST["model"], $_POST["type"]);

if (!$r) {
  ?><html><head><title>Временно не работает</title></head><body><p>Сообщение отправлено не было. Попробуйте повторить через несколько минут.</p><p>Если сегодня рабочий день, позвоните мне (84145)</p></body></html><?
} else {
  $q = "oid=" . $r["oid"];

  Header("Location: http://".$_SERVER['HTTP_HOST'] 
                     .dirname($_SERVER['PHP_SELF']) 
                     ."/sent.php?" . $q); 
}
}
?>
