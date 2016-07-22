# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'xinhua'

SPIDER_MODULES = ['xinhua.spiders']
NEWSPIDER_MODULE = 'xinhua.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

#ITEM_PIPELINES = {
#    'scrapy.pipelines.images.ImagesPipeline': 1,
#    'xinhua.pipelines.XinhuaPipeline': 300,
#}

#IMAGES_STORE='../data/20160722/xinhua'

ROBOTSTXT_OBEY = True
#DEPTH_LIMIT=3
