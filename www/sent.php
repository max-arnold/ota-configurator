<?
  require_once "layout.inc.php";
  require_once "date.inc.php";

  require_once "oma.inc.php";

  require_once "db.inc.php";
//  require_once "user.inc.php";

function check() {
  global $NeedRefresh;
  $NeedRefresh = 1;

  if ($r = OMAGetStatus2($_GET["oid"])) {
    $f = 1;
    foreach ($r as $v) {
      if ($v["code"] < 0) {
        $f = 0;
        break;
      }
    }
    if ($f == 1) {
      $NeedRefresh = 0;
    }
    return $r;
  }
}

class MyContent extends KgContent {

  var $Data;

  function HtmlMeta() {
    global $NeedRefresh;

    if ($NeedRefresh) {
      ?><META HTTP-EQUIV="Refresh" Content="5"><?
    }
  }

  function MainHeader() {
    echo "Сообщение отправлено";
  }

  function getTitle() {
    return "Сообщение отправлено";
  }

  function Display() {
    global $OMACheck;

    $oid = $_GET["oid"];

    if (!$OMACheck) {
      ?><table class="Article"><tr class="Header"><td colspan="2"><b>База временно недоступна</b></td></tr></table><?
    } else {
      $x = OMAGetSubmitInfo($oid);
      ?><table class="Article"><tr class="Header"><td colspan="2"><b>Сообщение отправлено</b></td></tr>
      <tr><td>ID</td><td><?=$x["ID"]?></td></tr>
      <tr><td>Отправлено</td><td><?=$x["Sent"]?></td></tr>
      <tr><td>Номер абонента</td><td><?=$x["Num"]?></td></tr>
      <tr><td>Модель телефона</td><td><?=($x["mn"] . " " . $x["mo"])?></td></tr>
      <tr><td>Тип настроек</td><td><?=$x["otaname"]?></td></tr>
      </table><?
      ?><table class="Article"><tr class="Header"><td colspan="2"><b>Сообщение разбито на нижеперечисленные части</b></td></tr>
      <? 
      foreach ($OMACheck as $v) {
        if ($v["code"] < 0) {
          $res = "<div style=\"color: red;\">Не доставлено</div>";
        } else {
          $res = "<div style=\"color: green;\"><b>Доставлено " . $v["tm"] . "</b></div>";
        }
        echo "<tr><td>" . $v["id"] . "</td><td>" . $res . "</td></tr>";
      }
      ?><tr class="Header"><td colspan="2"><b><a href="index.php">Отправить ещё одно сообщение</a></b></td></tr>
      </table><?
      if ($x["Textual"]) {
        ?><table class="Article"><tr class="Header"><td><b>Как сохранить настройки</b></td></tr><tr><td><?=$x["Textual"]?></td></tr></table><?
      }
      
    }
  }

}

$OMACheck = check();

$Layout = new KgLayout(new MyContent());
// $Layout->aHttpHeaders[] = "Refresh: 60";

$Layout->Display();


?>
