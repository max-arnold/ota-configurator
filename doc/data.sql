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
-- Table structure for table `otagroupnames`
--

DROP TABLE IF EXISTS `otagroupnames`;
CREATE TABLE `otagroupnames` (
  `ID` int(10) unsigned NOT NULL default '0',
  `Name` varchar(64) character set utf8 collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `otagroupnames`
--


/*!40000 ALTER TABLE `otagroupnames` DISABLE KEYS */;
LOCK TABLES `otagroupnames` WRITE;
INSERT INTO `otagroupnames` VALUES (1,'Nokia OTA Capable CSD only'),(2,'Siemens/Openwave CSD only'),(3,'Nokia OTA Capable CSD+GPRS'),(4,'Motorola OMA'),(10,'SMS Help Text'),(5,'Test group'),(9,'Generic Text');
UNLOCK TABLES;
/*!40000 ALTER TABLE `otagroupnames` ENABLE KEYS */;

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
-- Dumping data for table `Explanations`
--


/*!40000 ALTER TABLE `Explanations` DISABLE KEYS */;
LOCK TABLES `Explanations` WRITE;
INSERT INTO `Explanations` VALUES (1,'На экране телефона после прихода WAP-настроек появится сообщение: Service settings received (Установки услуги получены)\r\n<br>\r\nВыберите пункт Option (Варианты).<br>\r\nНа дисплее появится список команд:<br>\r\nView (Посмотреть) — вывести на экран имя настроек.<br>\r\nSave (Сохранить) — сохранить настройки (если нет свободных, система спросит, какой набор заменить).<br>\r\nDiscard (Не принимать) — удалить полученных настроек.<br>\r\nЧтобы сохранить полученные настройки, выберите пункт Save (Сохранить).'),(2,'Для сохранения настроек необходимо ввести PIN-код 1234.<br/>\r\nСохранённые настройки нельзя изменить. При попытке обращения к WAP-ресурсам телефон ВСЕГДА будет пытаться сделать это через GPRS, и всегда с грустью будет сообщать о том что GPRS недоступен.');
UNLOCK TABLES;
/*!40000 ALTER TABLE `Explanations` ENABLE KEYS */;

--
-- Table structure for table `otatypes`
--

DROP TABLE IF EXISTS `otatypes`;
CREATE TABLE `otatypes` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Name` varchar(64) character set utf8 collate utf8_unicode_ci NOT NULL default '',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `otatypes`
--


/*!40000 ALTER TABLE `otatypes` DISABLE KEYS */;
LOCK TABLES `otatypes` WRITE;
INSERT INTO `otatypes` VALUES (1,'CSD'),(2,'GPRS'),(3,'MMS-GPRS'),(10,'Text'),(4,'CSD+GPRS+MMS');
UNLOCK TABLES;
/*!40000 ALTER TABLE `otatypes` ENABLE KEYS */;

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
-- Dumping data for table `Manufacturers`
--


/*!40000 ALTER TABLE `Manufacturers` DISABLE KEYS */;
LOCK TABLES `Manufacturers` WRITE;
INSERT INTO `Manufacturers` VALUES (1,'LG'),(2,'SonyEricsson'),(3,'Samsung'),(4,'Nokia'),(5,'Siemens'),(6,'Ericsson'),(100,'-- Generic'),(7,'Motorola'),(8,'MTC'),(9,'Philips'),(256,'-- SMS');
UNLOCK TABLES;
/*!40000 ALTER TABLE `Manufacturers` ENABLE KEYS */;

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
-- Dumping data for table `otagroups`
--


/*!40000 ALTER TABLE `otagroups` DISABLE KEYS */;
LOCK TABLES `otagroups` WRITE;
INSERT INTO `otagroups` VALUES (1,1,'sendNokia','Nokia-csd.bin'),(2,1,'sendSiemens','siemens.txt'),(3,1,'sendNokia','Nokia-csd.bin'),(3,2,'sendNokia','Nokia-gprs.bin'),(3,3,'sendNokia','Nokia-mmsgprs.bin'),(10,10,'sendHelpText','smshelp.txt'),(4,4,'sendOMA','motorola-gsm.bin'),(5,1,'sendOMA','oma2.bin'),(9,1,'sendHelpText','gen-csd.txt'),(9,2,'sendHelpText','gen-gprs.txt'),(9,3,'sendHelpText','gen-mms.txt');
UNLOCK TABLES;
/*!40000 ALTER TABLE `otagroups` ENABLE KEYS */;

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
-- Dumping data for table `Models`
--


/*!40000 ALTER TABLE `Models` DISABLE KEYS */;
LOCK TABLES `Models` WRITE;
INSERT INTO `Models` VALUES (1,1,'G-1600',3,NULL),(2,1,'G-5400',3,NULL),(3,1,'G-5500',3,NULL),(4,1,'G-7030',3,NULL),(5,1,'G-7050',3,NULL),(6,1,'G-7100',3,NULL),(7,1,'L-1100',3,NULL),(8,2,'P800',3,NULL),(9,2,'P900',3,NULL),(10,2,'P910',3,NULL),(11,2,'K500i',3,NULL),(12,2,'K700i',3,NULL),(13,2,'S700i',3,NULL),(14,2,'S710',3,NULL),(15,2,'T68i',3,NULL),(16,2,'T100',1,NULL),(17,2,'T230',3,NULL),(18,2,'T300',3,NULL),(19,2,'T610',3,NULL),(20,2,'T630',3,NULL),(21,2,'Z200',3,NULL),(22,2,'Z500',3,NULL),(23,2,'Z600',3,NULL),(24,3,'SGH-D410',3,NULL),(25,3,'SGH-E100',3,NULL),(26,3,'SGH-E300',3,NULL),(27,3,'SGH-E400',1,NULL),(28,3,'SGH-E600',3,NULL),(29,3,'SGH-E700',3,NULL),(30,3,'SGH-E710',3,NULL),(31,3,'SGH-E800',3,NULL),(32,3,'SGH-E820',3,NULL),(33,3,'SGH-P100',1,NULL),(34,3,'SGH-P400',3,NULL),(35,3,'SGH-P410',3,NULL),(36,3,'SGH-P510',3,NULL),(37,3,'SGH-8300m',1,NULL),(38,3,'SGH-V200',3,NULL),(39,3,'SGH-X100',3,NULL),(40,3,'SGH-X400',3,NULL),(41,3,'SGH-X450',3,NULL),(42,3,'SGH-X460',3,NULL),(43,3,'SGH-X600',3,NULL),(44,4,'2650',3,NULL),(45,4,'3100',3,NULL),(46,4,'3200',3,NULL),(47,4,'3300',3,NULL),(48,4,'3330',1,NULL),(49,4,'3410',1,NULL),(50,4,'3510',3,NULL),(51,4,'3510i',3,NULL),(52,4,'3650',3,NULL),(53,4,'3660',3,NULL),(54,4,'5100',3,NULL),(55,4,'5210',1,NULL),(56,4,'5510',1,NULL),(57,4,'6100',3,NULL),(58,4,'6210',1,NULL),(59,4,'6250',1,NULL),(60,4,'6310',3,NULL),(61,4,'6310i',3,NULL),(62,4,'6510',3,NULL),(63,4,'6610',3,NULL),(64,4,'7110',1,NULL),(65,4,'7210',3,NULL),(66,4,'7250',3,NULL),(67,4,'7250i',3,NULL),(68,4,'7650',3,NULL),(69,4,'8310',1,NULL),(70,4,'8910',1,NULL),(71,4,'8910i',3,NULL),(72,4,'N-Gage',3,NULL),(73,4,'N-Gage QD',3,NULL),(74,5,'C62',3,NULL),(75,5,'ST55',3,NULL),(76,5,'SX1',3,NULL),(77,6,'A2628s',1,NULL),(78,6,'R320s',1,NULL),(79,6,'R380s',1,NULL),(80,6,'R520s',3,NULL),(81,6,'R600',3,NULL),(82,6,'T20s',1,NULL),(83,6,'T29s',1,NULL),(84,6,'T36s',1,NULL),(85,6,'T39',3,NULL),(86,6,'T65',3,NULL),(87,6,'T66',1,NULL),(88,6,'T68',3,NULL),(89,5,'A50',2,NULL),(90,5,'A55',2,NULL),(91,5,'A60',2,NULL),(92,5,'C55',2,NULL),(93,5,'C60',2,NULL),(94,5,'CF62',2,NULL),(95,5,'M50',2,NULL),(96,5,'M55',2,NULL),(97,5,'MC60',2,NULL),(98,5,'S45i',2,NULL),(99,5,'S55',2,NULL),(100,5,'SL55',2,NULL),(101,5,'ME45',2,NULL),(102,5,'C45',2,NULL),(103,100,'Nokia OTA',3,1),(104,100,'Siemens Openwave',2,NULL),(105,8,'i42',1,NULL),(106,8,'i43',1,NULL),(107,9,'530',3,NULL),(108,256,'Nokia OTA',3,NULL),(109,256,'SMS Help Text',10,NULL),(110,100,'Motorola OMA OTA',4,NULL),(111,7,'C250',4,2),(112,256,'Siemens Openwave',2,NULL),(113,256,'Motorola OMA OTA',4,NULL),(114,1,'T1500',3,NULL),(115,7,'V180',4,NULL),(116,4,'6260',3,NULL),(117,4,'6670',3,NULL),(118,4,'6800',3,NULL),(119,3,'D-100',3,NULL),(120,9,'535',3,NULL),(121,5,'CL50',2,NULL),(122,100,'Test',5,NULL),(123,100,'Text',9,NULL);
UNLOCK TABLES;
/*!40000 ALTER TABLE `Models` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

