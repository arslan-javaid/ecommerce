# E-commerce Scrapy


* Clone the repository using `git clone https://github.com/arslan-javaid/ecommerce.git` ;
* Go to `ecommerce` and execute these lines:
```
cd ecommerce

sudo pip install scrapy
sudo pip install ipython
```

#### Generate new Spider
```
scrapy genspider blueplusyellow blueplusyellow.ca
scrapy genspider grasscity www.grasscity.eu
```

#### Generate Json/CSV
```
scrapy crawl blueplusyellow -o blueplusyellow.json
scrapy crawl blueplusyellow -o blueplusyellow.csv

scrapy crawl grasscity -o grasscity.json
scrapy crawl grasscity -o grasscity.csv


scrapy crawl site -a config=config/grasscity.json -o output/grasscity.json
scrapy crawl site -a config=config/well.json -o output/well.xml
```