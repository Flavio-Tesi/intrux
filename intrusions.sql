/*DROP TABLE IF EXISTS `intrusions`;*/

CREATE TABLE IF NOT EXISTS `intrusions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_room` varchar(25) NOT NULL ,
  `status` BIT(1) NOT NULL,
  `dat` timestamp (8) DEFAULT NULL, 
  `dattime` timestamp (14) DEFAULT NULL, 
  PRIMARY KEY (`id`)
  FOREIGN KEY (id_room) REFERENCES rooms (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `intrusions` WRITE;*/

INSERT INTO intrusions (room,status) VALUES, ('Camera','0'), ('Cameretta','0'), ('Cucina','0'), ('Sala','0');

UNLOCK TABLES;
