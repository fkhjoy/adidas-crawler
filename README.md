# Purpose:
To obtain information of the product details pages of the men’s section of the
ADIDAS EC website ( https://shop.adidas.jp/ ) by crawling.
# Environment setup:
1. Create a virtual environment using
```python
python3 -m venv venv
```
2. Activate the virtual environment using following command<br>

<br>
for Ubuntu

```
source venv/bin/activate
```
3. Install the required dependencies
```
pip install -r requirements.txt
```
4. Install chromium and others
```
playwright install
```
4. Run the project
```
python3 main.py
```

# Data Format:
Multiple params in one cell are stored using separators.
e.g. `chest_size` =
`"3XS=110cm >> 2XS=114cm >> XS=118cm >> S=120cm >> M=126cm >> L=129cm >> XL=135cm >> 2XL=141cm >> 3XL=148cm"`
different items are separated by `" >> "`. key and value are separated by `=`.
so that we can extract the information based on those sepration symbols.

e.g. `user_reviews` = 

`"date=2024年4月8日 ; rating=5 / 5 ; title=過去最高傑作（試着必須） ; description= 175cm53kg【Sサイズ】今までもadidasのジャージは買ってきたが、これは最高傑作だと思う。着心地の良さと何よりはシルエットが綺麗。良すぎて色違いで二着買いました。ただサイズ選びが難しい。自分の身長でSでゆるくきられる。他でオーバーサイズで着ようとすると身幅がデカすぎたり、着丈が長すぎたりとちょうどいいゆるさにならないが、これは元からオーバーシルエットに作ってくれてあるぶん本当にちょうどいいゆるさ。ただ試着してみないとサイズ感は全くわからないと思うのが難点‥。購入を考えてる人は実店舗かもしくは一度返品する覚悟でサイズ選びをした方がいい。定期的に異なるカラーを出してくれたら毎回購入する。
（非表示） ; reviewer_id=rudo16  >> date=2023年11月3日 ; rating=5 / 5 ; title=デザイン&機能性が ; description= デザイン共に機能性が最高です。着心地もgood。162センチで骨格大きめ女子ですが、Ｍサイズでもルーズに着こなせます。
 ; reviewer_id=pussan"`
 
 Here different `user_review` are separated by `" >> "`.
 And multiple key-value pairs are separated by `" ; "`.
 Finally key and value are separated by `"="`.