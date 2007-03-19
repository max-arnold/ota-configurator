<?
  require_once "layout.inc.php";
  require_once "date.inc.php";

//  require_once "db.inc.php";
//  require_once "user.inc.php";

class MyContent extends KgContent {

  var $Data;

  function MainHeader() {
    echo "cfg";
  }

  function getTitle() {
    return "cfg" . ($this->Data["Short"] ? (" | " . $this->Data["Short"]) : "");
  }

  function Display() {
    global $DB;

    ?><table class="Body"><tr><td>
    <h3>Инструкция по настройке старых моделей сименсов</h3>
      <p>Отправить смс с настройками. После появления на телефоне флэшки "Настройки получены" зайти в меню
"Интернет". Телефон потребует pin-код, ввести маленькую английскую букву m. После этого телефон тут же полезет
в интернет на страницу wap.mts.ru.</p><p>Поскольку прошивки для телефонов Siemens писали недоучки, 
их периодически вставляет. В частности, перестают работать настройки и вообще internet. При таком раскладе по меню
"Интернет" можно перемещаться только стрелочками, кнопочка "Выбор" не работает. В такой ситуации проще всего 
выключить телефон, затем включить его, ответить на вопрос "подтвердите включение" и не трогать после этого минуту.</p>
<hr />
<form method="POST" action="newstyle.php">
<table class="Article"><tr class="header"><td colspan=3><b>Отправка настроек нового образца</b></td></tr>
<tr><select name="model"><?
    q = DBQuery();
    q->AddTable(array( "Manufacturers", "Models" ));
?>
<td rowspan="2">+<input type="text" name="number"></td><td nowrap>
      <input type="radio" name="kind" value="n" checked="checked" /><label>Nokia OTA</label></td><td>(Здесь будет список моделей)</td></tr>
      <tr><td><input type="radio" name="kind" value="s" /><label>Siemens OpenWave</label></td><td>(Здесь будет список моделей)</td></tr>
      <!-- <input type="radio" name="kind" value="o" /><label>Siemens OMA</label>-->
<tr><td colspan="3"><input class="btn" type="submit" value="Отправить"></td></tr></table>
      </form>
    </td></tr>
    </table><?
 
  }

}

$Layout = new KgLayout(new MyContent());
// $Layout->aHttpHeaders[] = "Refresh: 60";

$Layout->Display();

?>
