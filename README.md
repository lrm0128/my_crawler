本工程用于采集小区、成交的相关数据

核心思想：
1.获取URl:
    先将想要采集的数据的URL扒取下来，保存在数据库中
2.获取详情：
    从数据库中取出之前的URL，然后访问。进行爬取信息

小区URL的运行命令：
    scrapy crawl xiaoqu_little -a spider_name=sjz_lianjia1_xiaoqu -s LOG_FILE=自定义log文件
小区详情的运行命令：
    scrapy crawl xiaoqu_lianjia_detail -a spider_name=gz_lianjia1_xiaoqu_detail -s LOG_FILE=自定义log文件
    还可以指定行政区进行爬取：
        scrapy crawl xiaoqu_lianjia_detail -a spider_name=gz_lianjia1_xiaoqu_detail -s LOG_FILE=自定义log文件
成交URL的运行命令：
    这里由于上海、苏州和其他城市不一样，所以特别写了一个文件（仅增加了登录过程）：
        scrapy crawl sh_chengjiao_url -a spider_name=sh_lianjia2_url -s LOG_FILE=自定义log文件
    其他城市：
        scrapy crawl chengjiao_url -a spider_name=cd_lianjia1_url -s LOG_FILE=自定义log文件
成交详情的运行命令：
    这里由于上海、苏州和其他城市不一样，所以特别写了一个文件（取出数据的过程稍微不同）：
        scrapy crawl sh_chengjiao_url -a spider_name=su_lianjia_url -s LOG_FILE=suzhou_lianjia_url.log
    其余城市如下：
        scrapy crawl chengjiao_url -a spider_name=cd_lianjia_url -s LOG_FILE=chengdu_lianjia_url.log
挂牌URL的运行命令：
    对于上海的问题做了一个简单的策略：
    scrapy crawl ershoufang_url -a spider_name=sh_lianjia2_url -s LOG_FILE=shanghaidededed.log
挂牌详情的运行命令：
    scrapy crawl ershoufang_detail -a spider_name=sh_ershoufang_lianjia_house -s LOG_FILE=shanghaidededed.log
