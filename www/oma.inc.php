<?

require_once "IXR_Library.inc.php";

define("RPCSERVER", "http://localhost:7080/");

function OMASendMsg($to, $mn, $mo, $t) {
  if ($to[0] == "+") {
    $to = substr($to, 1);
  }

  $client = new IXR_Client(RPCSERVER);

  if ($client->query("uota", '+' . $to, $mn, $mo, $t)) {
    return $client->getResponse();
  }
}

function OMAGetStatus($oid) {
  $client = new IXR_Client(RPCSERVER);
  if ($client->query("status", $oid)) {
    return $client->getResponse();
  }
}

function OMAGetCodes() {
  $client = new IXR_Client(RPCSERVER);
  if ($client->query("codes")) {
    return $client->getResponse();
  }
}


function OMAGetServerStatus() {
  $client = new IXR_Client(RPCSERVER);
  if ($client->query("serverstatus")) {
    return $client->getResponse();
  }
}


function &last(&$a) {
  return $a[count($a) - 1];
}

function OMAGetCodes2() {
  global $DB;

  if ($z = $DB->getAll("SELECT Manufacturers.Name as mn, Models.Model as mo, Models.ID as UID, " .
    "otatypes.Name as t FROM Manufacturers, Models, otagroups, otatypes " .
    "WHERE Manufacturers.ID < 256 AND Manufacturers.ID = Models.MID and Models.OTACode = otagroups.ID and " .
    "otagroups.t = otatypes.id order by Manufacturers.Name, Models.Model, otatypes.Name")) {
    $r1 = array();
    $r2 = array();
    $r3 = array();

    foreach ($z as $r) {
      if ((count($r1) > 0) && (last($r1) == $r["mn"])) {
        if ((count(last($r2)) > 0) && (last(last($r2)) == $r["mo"])) {
          $x =& last(last($r3));
          $x[] = $r["t"];
        } else {
          $x =& last($r2);
          $x[] = $r["mo"];
          $x =& last($r3);
          $x[] = array($r["t"]);
        }
      } else {
        $r1[] = $r["mn"];
        $r2[] = array($r["mo"]);
        $r3[] = array(array($r["t"]));
      }
    }
    return array($r1, $r2, $r3);
  }
}

function &OMALastSubmits() {
  global $DB;

  if ($z = $DB->getAll("SELECT delivered.ID, delivered.Sent, delivered.Num, otatypes.Name as otaname, Manufacturers.Name as mn, Models.Model as mo " .
    "FROM delivered, Manufacturers, Models, otatypes " .
    "WHERE Sent >= curdate() and Manufacturers.ID = Models.MID and Models.ID = delivered.mo and " .
    "delivered.t = otatypes.ID order by Sent desc limit 10")) {
    return $z;
  }
}

function &OMAGetSubmitInfo($oid) {
  global $DB;

  if ($z = $DB->getAll("SELECT delivered.ID, delivered.Sent, delivered.Num, otatypes.Name as otaname, Manufacturers.Name as mn, Models.Model as mo" .
    " FROM delivered, Manufacturers, Models, otatypes  " .
    "WHERE Manufacturers.ID = Models.MID and Models.ID = delivered.mo and " .
    "delivered.t = otatypes.ID and delivered.ID = " . $oid)) {
    return $z[0];
  }
}

function &OMAGetStatus2($oid) {
  global $DB;

  if ($z = $DB->getAll("SELECT MSGID as id, Code as code, tm FROM delivered_parts left join dlr on MSGID = ID WHERE OTAID = " . $oid)) {
    $c = array();
    foreach ($z as $v) {
      $q = array();
      $q["id"] = $v["id"];
      $q["tm"] = $v["tm"];
      if (is_null($v["code"])) {
        $q["code"] = -1;
      } else {
        $q["code"] = (int) $v["code"];
      }
      $c[] = $q;
    }
    return $c;
  }
}

?>
