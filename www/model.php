<?
  require_once "db.inc.php";
  require_once "layout.inc.php";
  require_once "date.inc.php";
  require_once "oma.inc.php";


function genModelIndex() {
  global $DB;

  if ($z = $DB->getAll("select Models.ID, Models.Model, Manufacturers.Name from Models, Manufacturers where Models.MID = Manufacturers.ID order by Manufacturers.Name, Models.Model")) {
    ?><table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><td><table class="Article"><tr class="header"><td colspan="2">Models</td></tr><?
    $d0 = count($z) / 3;
    $d = $d0;
    $i = 0;
    foreach ($z as $v) {
      $i++;
      if ($i > $d) {
        $d += $d0;
        $n = "";
        ?></table></td><td><table class="Article"><tr class="header"><td colspan="2">Models</td></tr><?
      }
      if ($n != $v["Name"]) {
        $n = $v["Name"];
        ?><tr><td><?=$v["Name"]?></td><td><a href="?id=<?=$v["ID"]?>"><?=$v["Model"]?></a></td></tr><?
      } else {
        ?><tr><td></td><td><a href="?id=<?=$v["ID"]?>"><?=$v["Model"]?></a></td></tr><?
      }
    }
    ?></table></td></tr></table><?
  }
}


function showModel($id) {
  global $DB;
  $oc = array( 1 => "Nokia", 2 => "Siemens", 3 => "Nokia", 4 => "Motorola" );

  if ($z = $DB->getRow("select Manufacturers.Name, Models.Model, Models.OTACode, Models.TextID, otagroupnames.Name as ogn from Models, Manufacturers, otagroupnames where Models.MID = Manufacturers.ID and otagroupnames.ID = OTACode and Models.ID = " . $id)) {
    ?><table class="Article"><tr class="header"><td colspan=2><b>Информация о модели</b></td></tr>
    <tr><td><b>Название</b></td><td><?=($z["Name"] . " " . $z["Model"])?></td></tr>
    <tr><td><b>SMS-профиль</b></td><td><?=$oc[$z["OTACode"]]?></td></tr></table><?
  }


}

class MyContent extends KgContent {

  var $Data;

  function MainHeader() {
    echo "OTA-конфигуратор";
  }

  function getTitle() {
    return "OTA-Конфигуратор";
  }

  function Display() {

    ?><table class="Body">
<tr><td><? 
      if ($_GET["id"]) {
        showModel($_GET["id"]);
      } else {
        genModelIndex(); 
      } ?></td></tr>
    </table><?
 
  }

}

$Layout = new KgLayout(new MyContent());
$Layout->Display();

?>
