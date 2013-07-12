/*DROP TABLE IF EXISTS `intrusions`;*/

CREATE TABLE IF NOT EXISTS `intrusions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room` varchar(25) NOT NULL ,
  `status` BIT(1) NOT NULL,
  PRIMARY KEY (`room`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `intrusions` WRITE;*/

INSERT INTO intrusions (room,status) VALUES, ('Camera','0'), ('Cameretta','0'), ('Cucina','0'), ('Sala','0');

UNLOCK TABLES;
