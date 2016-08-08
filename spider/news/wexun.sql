CREATE USER 'wexun'@'localhost' IDENTIFIED BY 'wexun';
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
drop table if exists News;
create table News
(
   news_id              int AUTO_INCREMENT,
   agency_id            int,
   agency_name          varchar(20),
   news_title           varchar(100),
   news_time            char(12),
   news_data            longtext,
   news_type            int,
   news_imgs            varchar(1000),
   news_img_num         int,
   news_keys            varchar(100),
   news_resource_click_num int,
   news_resource_comment_num int,
   news_resource_link   varchar(100),
   primary key (news_id)
);
