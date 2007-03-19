-- MySQL dump 10.10
--
-- Host: localhost    Database: smpp3
-- ------------------------------------------------------
-- Server version	5.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Explanations`
--

DROP TABLE IF EXISTS `Explanations`;
CREATE TABLE `Explanations` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Textual` text character set utf8,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Table structure for table `Manufacturers`
--

DROP TABLE IF EXISTS `Manufacturers`;
CREATE TABLE `Manufacturers` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Name` varchar(64) collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Table structure for table `Models`
--

DROP TABLE IF EXISTS `Models`;
CREATE TABLE `Models` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `MID` int(10) unsigned NOT NULL default '0',
  `Model` varchar(64) character set utf8 collate utf8_unicode_ci NOT NULL default '',
  `OTACode` int(11) NOT NULL default '0',
  `TextID` int(11) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 PACK_KEYS=0;

--
-- Table structure for table `delivered`
--

DROP TABLE IF EXISTS `delivered`;
CREATE TABLE `delivered` (
  `ID` bigint(20) unsigned NOT NULL auto_increment,
  `Sent` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `Num` varchar(20) character set ascii collate ascii_bin NOT NULL default '',
  `mo` int(10) unsigned NOT NULL default '0',
  `t` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`ID`),
  KEY `Sent` (`Sent`),
  KEY `Num` (`Num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `delivered_parts`
--

DROP TABLE IF EXISTS `delivered_parts`;
CREATE TABLE `delivered_parts` (
  `OTAID` bigint(20) unsigned NOT NULL default '0',
  `MSGID` varchar(32) character set ascii collate ascii_bin NOT NULL default '',
  `SMSCID` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`MSGID`,`SMSCID`),
  KEY `OTAID` (`OTAID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `dlr`
--

DROP TABLE IF EXISTS `dlr`;
CREATE TABLE `dlr` (
  `tm` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `ID` varchar(32) character set ascii collate ascii_bin NOT NULL default '',
  `SMSCID` int(10) unsigned NOT NULL default '0',
  `Code` int(11) NOT NULL default '0',
  PRIMARY KEY  (`ID`,`SMSCID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Table structure for table `otagroupnames`
--

DROP TABLE IF EXISTS `otagroupnames`;
CREATE TABLE `otagroupnames` (
  `ID` int(10) unsigned NOT NULL default '0',
  `Name` varchar(64) character set utf8 collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `otagroups`
--

DROP TABLE IF EXISTS `otagroups`;
CREATE TABLE `otagroups` (
  `ID` int(10) unsigned NOT NULL default '0',
  `t` int(10) unsigned NOT NULL default '0',
  `ff` varchar(64) NOT NULL default '',
  `fn` varchar(64) NOT NULL default '',
  PRIMARY KEY  (`ID`,`t`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `otatypes`
--

DROP TABLE IF EXISTS `otatypes`;
CREATE TABLE `otatypes` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Name` varchar(64) character set utf8 collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

