DROP TABLE IF EXISTS `temperatures`;

CREATE TABLE IF NOT EXISTS `temperatures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_room` varchar(25) NOT NULL ,
  `val` int(8) DEFAULT NULL,
  `dat` timestamp (8) DEFAULT NULL, 
  `dattime` timestamp (14) DEFAULT NULL, 
  PRIMARY KEY (`id`)
  FOREIGN KEY (id_room) REFERENCES rooms (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `users` WRITE;*/

INSERT INTO temperatures (room) VALUES ('Camera'), ('Cameretta'), ('Cucina'), ('Sala');

UNLOCK TABLES;
