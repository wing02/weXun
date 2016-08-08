#CREATE USER 'wexun'@'localhost' IDENTIFIED BY 'wexun';
GRANT ALL ON wexun.* TO 'wexun'@'localhost';
FLUSH PRIVILEGES;
DROP DATABASE IF EXISTS wexun;
CREATE DATABASE wexun;

USE wexun;

CREATE TABLE item0
(
    item SMALLINT UNSIGNED,
    other VARCHAR(20000),
    PRIMARY KEY(item)
);
CREATE TABLE item1
(
    item SMALLINT UNSIGNED,
    other VARCHAR(20000),
    PRIMARY KEY(item)
);
CREATE TABLE item2
(
    item SMALLINT UNSIGNED,
    other VARCHAR(20000),
    PRIMARY KEY(item)
);
CREATE TABLE item3
(
    item SMALLINT UNSIGNED,
    other VARCHAR(20000),
    PRIMARY KEY(item)
);
/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2016/7/22 9:45:12                            */
/*==============================================================*/
/*==============================================================*/
/* Table: News                                                  */
/*==============================================================*/
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` tinyint(4) DEFAULT NULL,
  `agency_name` varchar(30) DEFAULT '',
  `news_time` timestamp NULL DEFAULT NULL,
  `news_data` varchar(50) DEFAULT '',
  `news_type` tinyint(11) DEFAULT '0',
  `news_imgs` varchar(200) DEFAULT '',
  `news_img_num` tinyint(11) DEFAULT '0',
  `news_keys` varchar(100) DEFAULT '',
  `news_resource_link` varchar(100) DEFAULT '',
  `news_title` varchar(100) DEFAULT '',
  `news_abstract` varchar(255) DEFAULT '',
  PRIMARY KEY (`news_id`),
  KEY `FK_Reference_16` (`agency_id`),
  KEY `newstitlIndex` (`news_title`),
  KEY `newstimeIndex` (`news_time`)
) ENGINE=InnoDB AUTO_INCREMENT=598 DEFAULT CHARSET=utf8;
