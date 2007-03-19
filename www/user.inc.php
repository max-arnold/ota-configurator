<?

require_once "db.inc.php";
require_once "db2.inc.php";
@require_once "Form.php";

class User {

  var $Data;

  function StandardQuery() {
    $Result = new DBQuery();

    $Result->AddTable("Users");
    $Result->AddField("*");

    return $Result;
  }

  function displayLoginForm() {

  ?><table class="Login" cellspacing=0 cellpadding=0>
<form class="Login" action="<?
echo $GLOBALS["PHP_SELF"];
?>" method="post">
<tr class="Header">
<td colspan="2"><b>Вход</b></td>
</tr><tr>
<td>Login:&nbsp;</td><td><input name="Login" size="13" class="norm"></td>
</tr><tr>
<td>Пароль:&nbsp;</td><td><input type="password" name="Password" size="13" class="norm"></td>
</tr><tr>
<td colspan=2 align="center"><input type="submit" value="Вход" class="btn"></td>
</tr></form></table><?

  }

  function &tryAuthenticate($Login, $Password) {
    global $DB;

    $Query = User::StandardQuery();
    $Query->AddWhere(array( "Name = '$Login'", "Password = PASSWORD('$Password')" ));

    if ($Data = $DB->getRow($Query->Generate())) {
      return new User($Data["ID"]);
    }
  }

  function &GetData($ID) {
    global $DB;

    $Query = User::StandardQuery();

    if (is_numeric($ID)) {
      $Query->AddWhere("ID = $ID");
    } else {
      $Query->AddWhere("Name = '$ID'");
    }

    return $DB->getRow($Query->Generate());
  }

  function User($ID) {
    $this->Data = User::GetData($ID);
  }

  function &tryLogon($ID) {
    if (User::GetData($ID)) {
      return new User($ID);
    }
  }

  function getID() {
    return $this->Data["ID"];
  }

  function displayLoginInfo() {
    ?><table class="Login" cellspacing=0 cellpadding=0>
<form class="Login" action="<? echo $GLOBALS["PHP_SELF"]; ?>" method="post">
<tr class="Header">
<td><b>Выход</b></td>
</tr><tr>
<td>Добро&nbsp;пожаловать, <q><? echo $this->Data["Name"]; ?></q>&nbsp!</td>
</tr><tr>
<td align="center"><input type="hidden" name="Logoff" value="yes"><input type="submit" value="Выход" class="btn"></td>
</tr></form></table><?
  }

  function logoff() {
    global $HTTP_SESSION_VARS, $ActiveUser;

    unset($HTTP_SESSION_VARS["ActiveUserId"]);
    unset($ActiveUser);
  }

  function ifLogin() {
    global $ActiveUser;

    if (!$ActiveUser) {
      User::displayLoginForm();
    } else {
      $ActiveUser->displayLoginInfo();
    }
  }

  function DisplayData($key, $value) {
    ?><tr><td class="Key"><? 
    echo $key;
    ?>:&nbsp;</td><td class="Value"><? 
    echo $value;
    ?></td></tr><?
  }

  function Display() {
    global $ActiveUser, $DB;

    $Access = $ActiveUser->Data["UserRights"];

    if ($Access) {
      $Access .= ",";
    }

    $FieldListQuery = new DBQuery();
    $FieldListQuery->AddTable("AllowedFields");
    $FieldListQuery->AddField(array( "Field", "Translation" ));
    $FieldListQuery->AddWhere("FIND_IN_SET(Rights, '$Access')");

    if ($Data = $DB->getAll($FieldListQuery->Generate())) {
      ?><table class="UserInfo" cellpadding=0 cellspacing=0><tr class="Header"><td><? echo $this->Data["Name"]; ?></td></tr><tr><td><table class="UserDetail"><?
      foreach ($Data as $Value) {
        User::DisplayData($Value["Translation"], $this->Data[$Value["Field"]]);
      }
      ?></table></td></tr></table><?
    }

  }

  function MakeEditForm() {
    global $ActiveUser, $DB;

    $Access = $ActiveUser->Data["UserRights"];

    if ($Access) {
      $Access .= ",";
    }

    $FieldListQuery = new DBQuery();
    $FieldListQuery->AddTable("AllowedFields");
    $FieldListQuery->AddField(array( "Field", "Translation" ));
    $FieldListQuery->AddWhere("FIND_IN_SET(Rights, '$Access')");

    $FieldTypes = $DB->getAll("show fields from Users");

    foreach ($FieldTypes as $Value) {
      $FTArray[$Value["Field"]] = $Value["Type"];
    }

    $EditForm = new HTML_Form("edit.php", "POST");
    
    if ($Data = $DB->getAll($FieldListQuery->Generate())) {
      foreach ($Data as $Value) {
        $EditForm->addText($Value["Field"], $Value["Translation"], $this->Data[$Value["Field"]]);
      }
    }

    $EditForm->addSubmit();

    ?><table class="UserInfo" cellpadding=0 cellspacing=0><tr class="Header"><td><? echo $this->Data["Name"]; ?></td></tr><tr><td><?
    $EditForm->display();
    ?></td></tr></table><?

  }

}

if ($HTTP_POST_VARS["Login"]) {
  if ($ActiveUser = User::tryAuthenticate($HTTP_POST_VARS["Login"], $HTTP_POST_VARS["Password"])) {
    $HTTP_SESSION_VARS["ActiveUserId"] = $ActiveUser->getID();
  }
}

if ($HTTP_POST_VARS["Logoff"]) {
  User::logoff();
}

if ($HTTP_SESSION_VARS["ActiveUserId"]) {
  $ActiveUser = User::tryLogon($HTTP_SESSION_VARS["ActiveUserId"]);
}

?>