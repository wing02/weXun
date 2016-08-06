/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2016/7/22 9:45:12                            */
/*==============================================================*/



drop table if exists NewsAgency;

drop table if exists NewsRecord;

drop table if exists NewsReportReocrd;

drop table if exists UseScans;

drop table if exists User;

drop table if exists UserBehavior;

drop table if exists UserLoginRecord;

drop table if exists Label;

drop table if exists newsRecommend;

drop table if exists news_label;

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
