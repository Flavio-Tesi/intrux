DROP TABLE IF EXISTS `rooms`;

CREATE TABLE IF NOT EXISTS `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
  UNIQUE (name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `rooms` WRITE;*/

INSERT INTO rooms (name) VALUES ('Camera'), ('Cameretta'), ('Cucina'), ('Sala');

UNLOCK TABLES;
