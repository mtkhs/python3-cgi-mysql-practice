CREATE DATABASE IF NOT EXISTS `bbs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE  IF NOT EXISTS `posts`(
   `id` int unsigned NOT NULL AUTO_INCREMENT,
   `name` varchar(255) NOT NULL,
   `body` varchar(255) NOT NULL,
   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

