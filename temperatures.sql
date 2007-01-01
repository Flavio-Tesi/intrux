DROP TABLE IF EXISTS `temperatures`;

CREATE TABLE IF NOT EXISTS `temperatures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_room` int(11) NOT NULL,
  `val` int(8) NOT NULL,
  `dat` date,
  `ora` time,
   
  PRIMARY KEY (`id`),
  FOREIGN KEY (id_room) REFERENCES rooms (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*LOCK TABLES `users` WRITE;*/

INSERT INTO temperatures (id_room, val, dat, ora) VALUES ('1','12','2012-10-08', '12:00:38'), ('2','20','1990-11-23', '00:55:15'), ('3','35','2009-05-17', '17:10:00'), ('4','10','1993-03-02', '14:00:17');

UNLOCK TABLES;
