CREATE USER 'wing'@'10.198.19.176' IDENTIFIED BY 'wexun';
GRANT ALL ON wexun.* TO 'wing'@'10.198.19.176';
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
DROP TABLE IF EXISTS `tmp_news`;
CREATE TABLE `tmp_news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_name` varchar(30) DEFAULT '',
  `news_time` timestamp NULL DEFAULT NULL,
  `news_data` varchar(100) DEFAULT '',
  `news_imgs` varchar(200) DEFAULT '',
  `news_title` varchar(100) DEFAULT '',
  `news_abstract` varchar(255) DEFAULT '',

  `update_time` timestamp NULL DEFAULT NULL,
  `news_type` varchar(11) DEFAULT '',
  `head1` varchar(11) DEFAULT '',
  `head2` varchar(11) DEFAULT '',
  `keys_data` varchar(200) DEFAULT '',

  `news_resource_link` varchar(100) DEFAULT '',
  `news_flag` varchar(10) DEFAULT '',
  `news_label` varchar(10) DEFAULT '',

  PRIMARY KEY (`news_id`),
  KEY `newstimeIndex` (`news_time`)
) ENGINE=InnoDB AUTO_INCREMENT=598 DEFAULT CHARSET=utf8;
