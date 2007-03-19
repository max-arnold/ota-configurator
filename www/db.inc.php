<?

require_once "DB.php";
// require_once "otkazano.inc.php";

// DisplayShitAndExit();

$DB = DB::Connect("mysql://smpp:smpp@localhost/smpp3", false);

if (!$DB) {
  DisplayShitAndExit();
}

$DB->setfetchmode(DB_FETCHMODE_ASSOC);
$DB->query("set names 'utf8'");
?>
