INSERT INTO news(news_id,agency_name,news_time,news_data,news_imgs,news_title,news_abstract) SELECT news_id,agency_name,news_time,news_data,news_imgs,news_title,news_abstract FROM tmp_news;
INSERT INTO news(id,title,update_time,type,agency,head1,head2,key_data,label_data) SELECT news_id,news_title,update_time,news_type,agency_name,head1,head2,keys_data,news_label FROM tmp_news;
