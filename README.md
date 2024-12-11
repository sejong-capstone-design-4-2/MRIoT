# MRIoT
![MRIoT Dashboard](https://github.com/sejong-capstone-design-4-2/MRIoT/blob/main/MRIoT_Dashboard.png?raw=true)

## Installation
 추후 Docker를 통한 통합적인 배포 제공 예정
```
sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https wget curl gnupg
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list'
sudo apt update
sudo apt install elasticsearch
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
curl -X GET "localhost:9200/"
```

```
{
  "name" : "node-1",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "8.x.x",
    ...
  },
  "tagline" : "You Know, for Search"
}
```

```
sudo nano /etc/elasticsearch/elasticsearch.yml
```

```
xpack.security.enabled: false
```

```
sudo apt-get update
sudo apt-get install kibana
sudo systemctl enable kibana
sudo systemctl start kibana
http://localhost:5601
```

```
sudo apt install python3-venv python3-pip
cd ./iotPacketProject
python3 -m venv venv
source venv/bin/activate
pip install django
django-admin startproject iotDashboard
cd iotDashboard
pip install elasticsearch-dsl
```

```
# settings.py

from elasticsearch import Elasticsearch

# Elasticsearch 설정
ES_HOST = 'localhost'
ES_PORT = 9200

# Elasticsearch 연결
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
```

```
# myapp/search_indexes.py

from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections
from .models import Article

connections.create_connection(hosts=['localhost'])

class ArticleDocument(Document):
    title = Text()
    content = Text()

    class Index:
        name = 'articles'

    @classmethod
    def prepare_title(cls, instance):
        return instance.title

    @classmethod
    def prepare_content(cls, instance):
        return instance.content
```

```
# myapp/models.py

from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
```

```
python manage.py shell
```
