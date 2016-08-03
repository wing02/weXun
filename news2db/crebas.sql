/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2016/7/22 9:45:12                            */
/*==============================================================*/


drop table if exists News;

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
create table News
(
   news_id              int identity,
   agency_id            int,
   agency_name          varchar(20),
   news_title           varchar(100),
   news_time            char(10),
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

/*==============================================================*/
/* Table: NewsAgency                                            */
/*==============================================================*/
create table NewsAgency
(
   agency_id            int not null,
   agency_name          varchar(20),
   agency_rank          int,
   primary key (agency_id)
);

/*==============================================================*/
/* Table: NewsRecord                                            */
/*==============================================================*/
create table NewsRecord
(
   news_record_id       int not null,
   news_id              int,
   news_click_num       int,
   news_recommend_num   int,
   news_share_num       int,
   news_storage_num     int,
   primary key (news_record_id)
);

/*==============================================================*/
/* Table: NewsReportReocrd                                      */
/*==============================================================*/
create table NewsReportReocrd
(
   report_id            int not null,
   user_id              int,
   news_id              int,
   report_time          varchar(10),
   report_describe      varchar(100),
   primary key (report_id)
);

/*==============================================================*/
/* Table: UseScans                                              */
/*==============================================================*/
create table UseScans
(
   scan_id              int not null,
   user_id              int,
   news_id              int,
   scan_time            varchar(10),
   news_other_info      int,
   news_label           int,
   from_ip              char(15),
   is_click             int,
   is_recommend         int,
   is_hate              int,
   is_share             int,
   primary key (scan_id)
);

/*==============================================================*/
/* Table: User                                                  */
/*==============================================================*/
create table User
(
   user_id              int not null,
   user_name            varchar(20),
   user_label           varchar(100),
   user_img             varchar(100),
   user_gender          char(1),
   user_birthday        char(10),
   password             varchar(20),
   account              varchar(10),
   user_type            int,
   primary key (user_id)
);

/*==============================================================*/
/* Table: UserBehavior                                          */
/*==============================================================*/
create table UserBehavior
(
   behavior_id          int not null,
   user_id              int,
   user_reocmmend_news_id varchar(1000),
   user_storage_news_id varchar(1000),
   user_share_news_id   varchar(1000),
   primary key (behavior_id)
);

/*==============================================================*/
/* Table: UserLoginRecord                                       */
/*==============================================================*/
create table UserLoginRecord
(
   record_id            int not null,
   user_id              int,
   from_ip              char(10),
   login_time           varchar(10),
   primary key (record_id)
);

/*==============================================================*/
/* Table: Label                                               */
/*==============================================================*/
create table label
(
   label_id             int not null,
   label_name           varchar(10),
   label_is_show        int,
   primary key (label_id)
);

/*==============================================================*/
/* Table: newsRecommend                                         */
/*==============================================================*/
create table newsRecommend
(
   recommend_id         int not null,
   user_id              int,
   news_id              int,
   primary key (recommend_id)
);

/*==============================================================*/
/* Table: news_label                                            */
/*==============================================================*/
create table news_label
(
   ID                   int not null,
   news_id              int,
   label_id             int,
   primary key (ID)
);

alter table News add constraint FK_Reference_16 foreign key (agency_id)
      references NewsAgency (agency_id) on delete restrict on update restrict;

alter table NewsRecord add constraint FK_Reference_19 foreign key (news_id)
      references News (news_id) on delete restrict on update restrict;

alter table NewsReportReocrd add constraint FK_Reference_14 foreign key (news_id)
      references News (news_id) on delete restrict on update restrict;

alter table NewsReportReocrd add constraint FK_Reference_15 foreign key (user_id)
      references User (user_id) on delete restrict on update restrict;

alter table UseScans add constraint FK_Reference_11 foreign key (user_id)
      references User (user_id) on delete restrict on update restrict;

alter table UseScans add constraint FK_Reference_12 foreign key (news_id)
      references News (news_id) on delete restrict on update restrict;

alter table UserBehavior add constraint FK_Reference_9 foreign key (user_id)
      references User (user_id) on delete restrict on update restrict;

alter table UserLoginRecord add constraint FK_Reference_1 foreign key (user_id)
      references User (user_id) on delete restrict on update restrict;

alter table newsRecommend add constraint FK_Reference_3 foreign key (user_id)
      references User (user_id) on delete restrict on update restrict;

alter table newsRecommend add constraint FK_Reference_4 foreign key (news_id)
      references News (news_id) on delete restrict on update restrict;

alter table news_label add constraint FK_Reference_13 foreign key (label_id)
      references Label (label_id) on delete restrict on update restrict;

alter table news_label add constraint FK_Reference_5 foreign key (news_id)
      references News (news_id) on delete restrict on update restrict;

