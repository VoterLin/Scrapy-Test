import scrapy


class itemSpider(scrapy.Spider):
    name = 'itemSpider'
    start_urls = ['http://lab.scrapyd.cn']

    def parse(self, response):
        mingyan = response.css('div.quote')[0]

        text = mingyan.css('.text::text').extract_first()
        # 提取名言
        autor = mingyan.css('.author::text').extract_first()
        # 提取作者
        tags = mingyan.css('.tags .tag::text').extract()
        # 提取标签
        tags = ','.join(tags)
        # 数组转换为字符串
        fileName = '%s-语录.txt' % autor
        # 爬取的内容存入文件，文件名为：作者-语录.txt
        f = open(fileName, "a+")
        # 追加写入文件
        f.write(text)  # 写入名言内容
        f.write('\n')  # 换行
        f.write('标签：' + tags)  # 写入标签
        f.close()  # 关闭文件操作
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
