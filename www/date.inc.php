<?

class DateFmt {
  var $mk;

  function toString($Format = "d.m.y H:i:s") {
    return date($Format, $this->toMktime());
  }

  function toMktime() {
    return $this->mk;
  }

  function toAssoc() {
    return getdate($this->mk);
  }

  function &Create(&$From) {
    return new DateFmt($From);
  }

  function DateFmt(&$From) {

    if (method_exists($From, "toMktime")) {
      $this->mk = $From->toMktime();
    } elseif (is_array($From)) {
      $this->mk = DateFmt::ParseAssoc($From);
    } elseif (is_integer($From)) {
      $this->mk = $From;
    } elseif (is_string($From)) {
      $this->mk = DateFmt::ParseString($From);
    } else {
      $this->mk = time();
    }

  }

  function ParseAssoc($From) {

    return 
      mktime((int) $From["hours"], 
        (int) $From["minutes"], 
        (int) $From["seconds"], 
        (int) $From["mon"], 
        (int) $From["mday"], 
        (int) $From["year"]);

  }

  function ParseString($From) {

    if ((strlen($From) >= 14)) {
      return DateFmt::ParseMySQLTimestamp($From);
    } elseif ((strlen($From) == 10)) {
      return DateFmt::ParseMySQLDate($From);
    }

  }

  function ParseMySQLTimestamp($From) {
    if (eregi("([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})", $From, $Parsed)) {
      return mktime((int) $Parsed[4], (int) $Parsed[5], (int) $Parsed[6], (int) $Parsed[2], (int) $Parsed[3], (int) $Parsed[1]);
    }
  }

  function ParseMySQLDate($From) {
    if (eregi("([0-9]{4})-([0-9]{2})-([0-9]{2})", $From, $Parsed)) {
      return mktime(0, 0, 0, (int) $Parsed[2], (int) $Parsed[3], (int) $Parsed[1]);
    }
  }

  function ParseGeneralDate($From) {
    return $this->ParseMySQLTimestamp($From);
  }

  function Date2Str($From) {
    if (!$From) {
      return;
    }
    $Value = DateFmt::Create($From);

    return $Value->toString();
  }

  function &StripTime() {
    return DateFmt::Create($this->StripTimeEx());
  }

  function StripTimeEx() {
    $From = $this->toAssoc();

    return mktime(0, 0, 0, (int) $From["mon"], (int) $From["mday"], (int) $From["year"]);
  }

  function &Interval($Against) {
    return new DateInterval($this->StripTimeEx() - $Against->StripTimeEx());
  }

}

class DateInterval extends DateFmt {
  function toString() {
    $of = array(-2 => "Позавчера", -1 => "Вчера", 0 => "Сегодня", 
      1 => "Завтра", 2 => "Послезавтра");

    if (!($result = $of[-($this->mk)]))
    {
      if ($this->mk < 0)
        $result .= "Через ";

      $result .= Abs($this->mk) . " дней";

      if ($this->mk > 0)
        $result .= " назад";
    }

    return $result;
  }
}

?>