<?
  require_once "db.inc.php";
  require_once "layout.inc.php";
  require_once "date.inc.php";
  require_once "oma.inc.php";

function xxarray($a) {
  if (!is_array($a)) {
    echo "\"" . $a . "\"";
  } else {
    echo "new Array(";
    $i = 0;
    foreach ($a as $v) {
      if ($i == 0) {
        $i = 1;
      } else {
        echo ",";
      }
      if (!is_array($v)) {
        echo "\"" . $v . "\"";
      } else {
        xxarray($v);
      }
    }
    echo ")\n";
  }
}

function genStats() {
  global $DB;

?>
<table class="Article"><tr class="header"><td colspan="3"><b>Некоторая статистика</b></td></tr>
<?
  if ($r = $DB->getAll("select date(sent) as ds, count(*) as c, count(DISTINCT Num) as cd from delivered where DATE_SUB(CURDATE(),INTERVAL 5 DAY) <= sent group by ds order by ds desc limit 5")) {
    foreach ($r as $v) {
      ?><tr><td><?=$v["ds"]?></td><td><?=$v["c"]?></td><td><?=$v["cd"]?></td></tr><?
    }
  } else {
    ?><tr><td colspan=2>Сегодня запросов не было</td></tr><?
  }
?>
</table>
<?

}

function genPopIndex() {
  global $DB;

  ?><table class="Article"><tr class="header"><td colspan="2"><b>Индекс популярности</b></td></tr><?
  if ($r = $DB->getAll("SELECT  Manufacturers.Name, Models.Model, count(*) as co from delivered, Models, Manufacturers where Sent >= curdate() and mo = Models.ID and Manufacturers.ID = Models.MID and Manufacturers.ID < 100 group by mo order by co desc limit 10")) {
    foreach ($r as $v) {
      ?><tr><td><?=($v["Name"] . " " . $v["Model"])?></td><td><?=$v["co"]?></td></tr><?
    }
  } else {
    ?><tr><td colspan=2>Сегодня запросов не было</td></tr><?
  }
  ?></table><?
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

    ?><table class="Body"><tr><td>
<table class="Article"><tr class="header"><td colspan="4"><b>!</b></td></tr>
<tr><td>Если модели, на которую вы хотите отправить настройки, нет в списке, выбирайте Generic, тип настроек, и тип соединения на которое хотите настроить</td></tr></table>
<form name="main" method="POST" action="newstyle.php" onSubmit="return testnum()">
<table class="Article"><tr class="header"><td colspan="3"><b>Отправка настроек нового образца</b></td></tr>
<tr><td>+<input type="text" name="number"></td><td>
<select name="manufacturer" onChange="filla2(this.selectedIndex)">
<option value="N/A">N/A</option>
</select>
<select name="model" onChange="filla3(manufacturer.selectedIndex, this.selectedIndex)">
</select>
<select name="type" onChange="">
</select>


</td><td><input class="btn" type="submit" value="Отправить"></td></tr></table>
      </form>
<? $m = OMAGetCodes2(); ?>
<script type="text/javascript">

<!--

var a1 = <? xxarray($m[0]); ?>;
var a2 = <? xxarray($m[1]); ?>;
var a3 = <? xxarray($m[2]); ?>;

function adde(lst, opt, ind) {
  if (document.createElement) {
    var n = document.createElement("OPTION");
    n.text = opt;
    n.value = opt;
    (lst.options.add) ? lst.options.add(n) : lst.add(n, null);
  } else {
    lst.options[i] = new Option(opt, opt, false, false);
  }
}

function filla1() {
  nl = document.forms["main"].elements["manufacturer"];
  nl.length = 0;
  for (i = 0; i < a1.length; i++) {
    adde(nl, a1[i], i);
  }
  filla2(0);
}

function filla2(idx) {
  nl = document.forms["main"].elements["model"];
  nl.length = 0;
  aa = a2[idx]
  for (i = 0; i < aa.length; i++) {
    adde(nl, aa[i], i);
  }
  filla3(idx, 0);
}

function filla3(idx1, idx2) {
  nl = document.forms["main"].elements["type"];
  nl.length = 0;
  aa = a3[idx1][idx2];
  for (i = 0; i < aa.length; i++) {
    adde(nl, aa[i], i);
  }
}


filla1();

function testnum() {
  num = document.forms["main"].elements["number"];
  if (num.value.length != 11) {
    alert("на номер +" + num.value + " нельзя отправить SMS!");
    return false;
  }
  return true;
}

//-->
</script>
    <table class="Article"><tr class="header"><td><b>Как сохранить настройки в Siemens/Openwave</b></td></tr><tr><td>
При появлении оповещения "Настройки получены", абоненту нужно зайти в меню "Интернет", на запрос pin-кода ввести маленькую англйискую букву m. После этого телефон сразу попытается установить соединение с 0885, заранее предупреждайте абонентов об этом!
<br/>Из-за ошибок в прошивках телефон может повести себя неадекватно: перестают работать настройки, по меню "Интернет" можно перемещаться только стрелочками, кнопочка "Выбор" не доступна. В таких случаях абоненту следует выключить телефон, включить его, подождать 2-3 минуты, попробовать снова зайти в меню "Интернет".</td></tr></table>
    <table class="Article"><tr class="header"><td><b>Как сохранить настройки OMA</b></td></tr><tr><td>Для сохранения настроек необходимо ввести PIN-код 1234</td></tr></table>

<? genStats(); ?>
<table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><td>
<table class="Article"><tr class="header"><td colspan="4"><b>Последние 10 заказов</b></td></tr>
<? $d = OMALastSubmits(); 
foreach ($d as $v) {
  ?><tr><td><?=$v["Sent"]?></td><td><a href="sent.php?oid=<?=$v["ID"]?>"><?=$v["Num"]?></a></td><td><?=($v["mn"] . " " . $v["mo"])?></td><td><?=$v["otaname"]?></td></tr><?
}
?>
</td></tr></table></td><td><? genPopIndex(); ?></td></tr></table>

    </td></tr>
    </table><?
 
  }

}

$Layout = new KgLayout(new MyContent());
$Layout->Display();

?>
