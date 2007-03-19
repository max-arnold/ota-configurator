<?php

require_once "PEAR.php";

class Layout extends PEAR {

  var $aHttpHeaders = array( "Cache-Control: no-cache, must-revalidate" );
  var $aHtmlDoctype = "HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\"";
  var $aHtmlTitle;
  var $aHtmlCSS = array( "all" => "pre.css" );
  var $aHtmlBodyParams = array( "topmargin" => "1", "leftmargin" => "1" );

  var $aValidContents = array( "Content" );
  var $aContent;

  function ValidClass(&$Class, &$ClassList) {
    while (list( , $value) = each($ClassList)) {
      if (is_subclass_of($Class, $value) || (get_class($Class) == $value))
        return true;
    }
  }

  function Layout(&$Content) {
    if (Layout::ValidClass($Content, $this->aValidContents)) {
      $this->aContent = $Content;
    }
  }

  function HttpHeaders()
  {
    while (list( ,$value) = each($this->aHttpHeaders)) {
      Header($value);
    }
  }

  function HtmlDoctype() {
    ?><!DOCTYPE <?= $this->aHtmlDoctype ?><?
  }

  function HtmlTitle() {
    ?><title><?= $this->aContent->getTitle() ?></title><?
  }

  function HtmlCSS() {
    while (list($key, $value) = each($this->aHtmlCSS)) {
      ?><link rel="STYLESHEET" type="text/css" MEDIA="<?= $key ?>" href="<?= $value ?>"><?
    }
  }

  function HtmlBodyEx() {

    ?><body<?
    while (list($key, $value) = each($this->aHtmlBodyParams)) {
      echo " " . $key . "=\"" . $value . "\"";
    }
    ?>><?

    $this->HtmlBody();

    ?></body><?

  }

  function HtmlBody() {}

  function HtmlHeadEx() {
    ?><head><?
    $this->HtmlHead();
    ?></head><?
  }

  function HtmlHead() {
    $this->HtmlTitle();
    $this->HtmlCSS();
    $this->aContent->HtmlMeta();
  }

  function Display() {

//    HTTP_Compress::start();

    $this->HttpHeaders();
    $this->HtmlDoctype();
    ?><html><?
    $this->HtmlHeadEx();

    $this->HtmlBodyEx();

    ?></html><?

//    HTTP_Compress::output();
  
  }

}

class KgLayout extends Layout {

  var $aValidContents = array( "kgcontent" );

  function HtmlBody() {
    if (is_subclass_of($this->aContent, "KgContent")) {
      $this->aContent->Display();
      ?><div class="MainCopyright">&copy; <a href="http://stingr.net">Stingray</a></div><?
    }
  }

}

class Content extends PEAR {
  function getTitle() {}
}

class KgContent extends Content {
  function MainHeader() {}

  function Display() {}

  function HtmlMeta() {}
}

?>