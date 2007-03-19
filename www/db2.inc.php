<?php

require_once "PEAR.php";

class DBQuery extends PEAR {

  var $Fields, $Tables, $Where, $Having, $Limit, $Orders, $Groups;

  function DBQuery() {
    $this->Fields = array();
    $this->Tables = array();
    $this->Where = array();
    $this->Having = array();
    $this->Orders = array();
    $this->Groups = array();
  }

  function ListHelper(&$Data, $Delim) {

    foreach ($Data as $Value) {
      if ($Result) {
        $Result .= $Delim;
      }

      $Result .= $Value;
    }

    return $Result;
  }

  function ListHelper2(&$Data, $Prefix) {
    if ($Data) {
      return $Prefix . $Data;
    }
  }

  function PGenerate($a) {
    $Result = $this->Generate();

    if ($Result && $a) {
      foreach ($Name as $Value) {
        $Result = str_replace("%{" . $Name . "}", $Value, $Result);
      }
    }

    return $Result;
  }
  
  function Generate() {
    $Result .= "Select";

    $FieldsList = DBQuery::ListHelper($this->Fields, ", ");
    $TablesList = DBQuery::ListHelper($this->Tables, ", ");
    $WhereList = DBQuery::ListHelper($this->Where, " AND ");
    $HavingList = DBQuery::ListHelper($this->Having, " AND ");
    $OrderList = DBQuery::ListHelper($this->Orders, ", ");
    $GroupList = DBQuery::ListHelper($this->Groups, ", ");

    if ((!$FieldsList) || (!$TablesList)) {
      return;
    }

    $Result .= " " . $FieldsList . " From " . $TablesList;

    $Result .= DBQuery::ListHelper2($WhereList, " Where ") .
      DBQuery::ListHelper2($GroupList, " Group By ") .
      DBQuery::ListHelper2($HavingList, " Having ") .
      DBQuery::ListHelper2($OrderList, " Order By ") .
      DBQuery::ListHelper2($this->Limit, " Limit ");

    return $Result;
  }

  function Add(&$Data, &$Item) {
    if (is_array($Item)) {
      foreach ($Item as $Value) {
        DBQuery::AddEx($Data, $Value);
      }
    } else {
      DBQuery::AddEx($Data, $Item);
    }
  }
  
  function AddEx(&$Data, &$Item) {
    if (!in_array($Item, $Data)) {
      $Data[] = $Item;
    }
  }

  function AddTable($Item) {
    DBQuery::Add($this->Tables, $Item);
  }

  function AddField($Item) {
    DBQuery::Add($this->Fields, $Item);
  }

  function AddWhere($Item) {
    DBQuery::Add($this->Where, $Item);
  }

  function AddHaving($Item) {
    DBQuery::Add($this->Having, $Item);
  }

  function AddOrder($Item) {
    DBQuery::Add($this->Orders, $Item);
  }

  function AddGroup($Item) {
    DBQuery::Add($this->Groups, $Item);
  }

  function SetLimits($Item) {
    $this->Limit = $Item;
  }

  function Delete(&$Data, &$Item) {
    if (is_array($Item)) {
      foreach ($Item as $Value) {
        DBQuery::DeleteEx($Data, $Value);
      }
    } else {
      DBQuery::DeleteEx($Data, $Item);
    }
  }
  
  function DeleteEx(&$Data, &$Item) {
    if ($Key = array_search($Item, $Data)) {
      unset($Data[$Key]);
    }
  }

  function DeleteTable($Item) {
    DBQuery::Delete($this->Tables, $Item);
  }

  function DeleteField($Item) {
    DBQuery::Delete($this->Fields, $Item);
  }

  function DeleteWhere($Item) {
    DBQuery::Delete($this->Where, $Item);
  }

  function DeleteHaving($Item) {
    DBQuery::Delete($this->Having, $Item);
  }

  function DeleteOrder($Item) {
    DBQuery::Delete($this->Orders, $Item);
  }

}

?>