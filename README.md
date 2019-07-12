## Tencent News Crawler using Spiderkeeper, Scrapyd, (Supervisor)

### Python dependences 
```pip install``` the following packages:

|         Package        |              For               |
|:----------------------:|:------------------------------:|
|         logging        |              logs              |
|        traceback       |      debug tracing in logs     |
| mysql-connector-python |      python mysql database     |
|         scrapyd        | crawler automation and control |
|       supervisor       | process automation and control |
|      spiderkeeper      |       nice UI for scrapyd      |
|     scrapyd-client     |      a helper for scrapyd      |

### Usage 1: Test crawlling:
```
    cd TencentNews/
    scrapy crawl FinanceSpider
```
- For past news data, pass in the argument ```days_prior``` to specify how many days before do you want the spider to start crawling. This way it will update comment_num of news in the past.
(Drawback: the API weblink available only supports news about 20 days before the current date.) e.g.
```
    scrapy crawl FinanceSpider -a days_prior=3
```
- For current data, don't pass in anything.

Sidenote: the reason to use ```cd``` is to support ```scrapy``` commands, which only works with scrapy.cfg file in the same directory

### Usage 2: Spider automation minotoring

1. Run:
```
    scrapyd
```
2. Open another terminal, then run:
```
    spiderkeeper --server=http://localhost:6800 --username=admin --password=admin
```
3. Go to http://localhost:5000 where hosts spiderkeeper UI
4. Create a project.
5. Deploy an egg file. The.egg file is generated by:
```
    scrapyd-deploy --build-egg output.egg
```
6. click on "Dashboard" on the left panel.
7. click on "RunOnce".
    
Note: [(issue)](https://github.com/DormyMo/SpiderKeeper/issues/87) if you don't see spider on the list of spiders, try running in the same directory:
```
    scrapyd-deploy
```
SideNote: To check current scrapyd projects run:
```
    scrapyd-client projects
```

### Usage 3: more automated usage2 (beta)
1. move the config used by supervisor
```
    sudo mv supervisord.conf /etc/supervisor/
```
2. run supervisor
```
    supervisord -c /etc/supervisor/supervisord.conf
```
Note: 
    i. The socket file and all logs are stored in /tmp/. To check logs:
    ```
        less /tmp/supervisord.log
    ```
    ii. to close supervisor
    ```
        ps aux | grep supervisord
        kill <PID>
    ```
    iii. interactive shell for supervisor
    ```
        supervisorctl
        supervisor> status
    ```

## Spiders:
### FinanceSpider 
This crawler uses API enpoints implemented within Tencent New's auto-scroll feature in order to crawl and store all key information about news related to finance. 

## MySQL database schema
Database name: news
Table name: finance_news

| Field        | Type                  | Null | Key | Default | Extra |
|:------------:|:---------------------:|:----:|:---:|:-------:|:-----:|
| id           | char(14)              | NO   | PRI | NULL    |       |
| title        | char(40)              | NO   |     | NULL    |       |
| publish_time | datetime              | NO   |     | NULL    |       |
| source       | char(20)              | YES  |     | NULL    |       |
| comment_num  | mediumint(8) unsigned | NO   |     | NULL    |       |
| url          | char(60)              | YES  |     | NULL    |       |
| keywords     | tinytext              | YES  |     | NULL    |       |
| content      | text                  | YES  |     | NULL    |       |

## Findings on Tencent News's URLs
1. https://pacaio.match.qq.com/xw/site?&ext=finance&num=20&page=0
    - Returns a list of information-rich json file of news that has "finance" in its "ext" field
    - for exaple, one news can have its "ext" field be:
    ```
        "349+0"+"all":";;;734+9"+"3h":"106587+4680;1447+23;stock:8168+349#finance:51062+2578;674+9"+"day":"361497+15793;8179+104;stock:29103+1240#finance:176307+8396;734+9"
    ```
    - which looks like a result of machine-learned catagory analysis

2. http://pacaio.match.qq.com/openapi/json?key=finance:20190709&num=20&page=0
    - (Accepted)
    - Also used by auto-scroll on the website
    - Returns a concise list of news according to the given date and category
    - Categories of finance:
    ```
    ['finance', # used by 财经网
    'finance_company',
    'finance_startup',
    'finance_economy',
    'finance_consume',
    'finance_estate',
    'finance_investment',
    'finance_mngmoney',
    'finance_people',
    'finance_business',
    'finance_stock',
    'finance_banking',
    'finance_collection']
    ```

## Known bug

1. Spiderkeeper doesn't show up the list of spiders available:
    run scrapyd-deploy in directory to manually deploy
