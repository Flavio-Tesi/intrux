DROP TABLE IF EXISTS `log_intrusions`;

CREATE TABLE IF NOT EXISTS `log_intrusions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_stanza` int(11) DEFAULT NULL,
  `id_intrusion` int(11) DEFAULT NULL,
  `dat` timestamp (14) DEFAULT NULL, 
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `log_intrusions` WRITE;*/

UNLOCK TABLES;
