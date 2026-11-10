# Sales Insight Agent

Satış verisine soru soran bir ajan. Ajan döngüsü Python'da [Strands](https://strandsagents.com) ile yazılır. Cümleyi Amazon Bedrock üzerindeki model kurar. Süreç laptopta ya da Amazon Bedrock AgentCore üzerinde çalışır.

PostgreSQL Docker'da durur. Sorgular ay, ürün veya bölgeye göre toplanır. Her satırda `group_name`, `total_sales`, `total_quantity` ve `transaction_count` vardır.

## Strands ve AgentCore

Strands ajanın kendisidir. Soruyu modele gönderir. Model bir araç istediyse o fonksiyonu çalıştırır, dönen satırları modele geri verir ve cevabı tamamlar. Yerel giriş `sales-insight-agent/main.py` dosyasıdır.

AgentCore bu Python sürecinin AWS üzerindeki çalışma yeridir. Çağrı HTTP ile gelir. Oturum kimliği `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` başlığından okunur. İçeride yine bir Strands ajanı açılır. Model isteği yine Bedrock'a gider. Giriş `SalesInsightTemplate/app/agent/main.py` dosyasıdır.

## Verinin izlediği yol

Yerel çalışmada araçlar `database/queries.py` ile Postgres'e doğrudan bağlanır.

AgentCore üzerindeki araçlar `SALES_QUERY_URL/sales` adresine JSON gönderir. Bu adres, laptopta `127.0.0.1:8081` portunu dinleyen `query_server` sürecine bir tünelle ulaşır. Sunucu salt okunur bağlantıyla özeti alır ve `results` listesini döner.

Bu yolun işlemesi için Docker, `query_server` ve tünel açık kalır. Tünel yeniden açılınca adres değişir. Yeni adres `SALES_QUERY_URL` olarak verilip runtime tekrar deploy edilir.

```text
soru
  -> Strands ajanı (laptop veya AgentCore)
    -> Bedrock modeli
      -> get_sales_data veya get_product_sales_ranking
        -> Postgres
           yerel çalışmada doğrudan
           AgentCore çalışmasında query_server üzerinden
```

## Araçlar

`get_sales_data` bir tarih aralığını özetler. İsteğe bağlı ürün ve bölge filtresi vardır. `group_by` değeri `month`, `product` veya `region` olur.

`get_product_sales_ranking` ürünleri `total_sales` veya `total_quantity` alanına göre sıralar. Sonuçta üst ve alt dilim birlikte döner.

## Klasörler

| Yol | İçerik |
| --- | --- |
| `sales-insight-agent` | Şema, salt okunur sorgular, Strands ajanı, `query_server`, testler ve değerlendirme |
| `SalesInsightTemplate` | Aynı ajanın AgentCore paketi. Araçlar HTTP ile sorgu sunucusunu çağırır |

Bağlantı değerleri `sales-insight-agent/.env` içindedir. `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` ve `DB_PASSWORD` salt okunur sorgu içindir. `POSTGRES_DB`, `POSTGRES_USER` ve `POSTGRES_PASSWORD` Docker ile veri yükleme içindir. `AWS_REGION` ve `BEDROCK_MODEL_ID` modeli seçer.

## Çalıştırma

Yerel ajan, `sales-insight-agent` klasöründe:

```powershell
docker compose up -d
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe -m evaluations.run_evaluation
```

Sorgu sunucusu aynı klasörde `python -u -m query_server` ile açılır. `GET /health` cevabı `{"status":"ok"}` olur. `POST /sales` gövdesinde `start_date`, `end_date` ve isteğe bağlı `product_name`, `region_name`, `group_by` vardır.

AgentCore deploy ve çağrıları `SalesInsightTemplate` klasöründen, bölge `eu-west-1` ile yapılır. Deploy öncesinde tünel adresi ortama yazılır:

```powershell
$env:SALES_QUERY_URL = "https://<tünel-adresi>"
agentcore deploy --region eu-west-1
agentcore invoke --region eu-west-1 --runtime agent --session-id "<oturum-kimliği>" --payload '{"prompt":"..."}'
```
