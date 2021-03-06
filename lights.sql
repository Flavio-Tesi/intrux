DROP TABLE IF EXISTS `lights`;

CREATE TABLE IF NOT EXISTS `lights` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_room` int(11) NOT NULL ,
  `status` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (id_room) REFERENCES rooms (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `intrusion` WRITE;*/

INSERT INTO lights (id_room,status) VALUES ('1',0), ('2',0), ('3',0), ('4',0);

UNLOCK TABLES;
