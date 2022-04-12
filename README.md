# 洋ナシの等級判定システム(API)
<span>
<a href="https://docs.python.org/3.8/">
  <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=plastic">
</a>

<img src="https://img.shields.io/badge/-Flask-000000.svg?logo=flask&style=plastic">

<img src="https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=plastic">

<img src="https://img.shields.io/badge/-Mysql-4479A1.svg?logo=mysql&style=plastic">

<a href="">
  <img src="https://img.shields.io/badge/-Redis-D82C20.svg?logo=redis&style=plastic">
</a>

<a href="https://www.docker.com/">
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=plastic">
</a>

<img src="https://img.shields.io/badge/-Amazon%20aws-232F3E.svg?logo=amazon-aws&style=plastic">

</span>

洋ナシの等級を判定するために、外観汚損の検査を行うためのAPI

※ 研究で作成したコードの公開版

## 環境構築
DockerとDocker for Mac か Docker for windowsをインストールする。  
下記コマンドを実行する
> docker-compose up -d

APIのMockだけ使いたい時
> docker-compose up -d swagger-api  
> docker-compose up -d swagger-ui

- [swagger-ui(http://localhost:8002/)](http://localhost:8002/)でAPIのインターフェースを確認
- [swagger-api(http://localhost:8003/)](http://localhost:8003/)で対象のエンドポイントに対してリクエスト
