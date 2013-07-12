DROP TABLE IF EXISTS `lights`;

CREATE TABLE IF NOT EXISTS `lights` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room` varchar(25) NOT NULL ,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `intrusion` WRITE;*/

INSERT INTO lights (room,status) VALUES ('Camera',0), ('Cameretta',0), ('Cucina',0), ('Sala',0);

UNLOCK TABLES;
