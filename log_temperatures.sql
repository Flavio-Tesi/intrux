DROP TABLE IF EXISTS `log_temperatures`;

CREATE TABLE IF NOT EXISTS `log_temperatures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_stanza` int(11) DEFAULT NULL,
  `id_temp` int(11) DEFAULT NULL,
  `dat` timestamp (14) DEFAULT NULL, 
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `log_temperatures` WRITE;*/

UNLOCK TABLES;
