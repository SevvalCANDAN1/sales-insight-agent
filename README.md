# Sales Insight Agent

Satış sorularını yanıtlayan bir ajan. Soru ve model Amazon Bedrock AgentCore üzerinde çalışır. PostgreSQL veritabanı laptopta kalır. AWS'ye giden kayıt, sorgunun toplu sonucudur: grup adı, ciro, adet ve işlem sayısı.

## Nasıl çalışır

1. Soru, `SalesInsightTemplate` içindeki `agent` runtime'ına gider.
2. Ajan iki araçtan birini seçer.
3. Araç, `SALES_QUERY_URL` adresindeki `/sales` yoluna JSON gönderir.
4. Cloudflare tüneli bu isteği laptopta `http://127.0.0.1:8081` adresine taşır.
5. `query_server` salt okunur bağlantıyla Postgres'ten özeti alır ve `results` listesini döner.
6. Model bu satırlarla cevabı yazar.

Tünel, sorgu sunucusu veya Docker kapalıysa runtime ayakta kalsa da satış sorusu sonuç getirmez. Tünel her açılışta yeni bir adres alır. Adres değişince `SALES_QUERY_URL` yeni değerle yeniden deploy edilir.

```text
soru
  -> AgentCore runtime (eu-west-1)
    -> get_sales_data / get_product_sales_ranking
      -> tünel
        -> query_server (127.0.0.1:8081)
          -> Postgres (localhost:5433)
```

## Klasörler

| Klasör | Görevi |
| --- | --- |
| `sales-insight-agent` | Veritabanı, salt okunur sorgular, yerel ajan, sorgu sunucusu ve değerlendirmeler |
| `SalesInsightTemplate` | Aynı araçların AgentCore'a deploy edilen kopyası. Araçlar veritabanına doğrudan bağlanmaz; HTTP ile sorgu sunucusunu çağırır |

## Araçlar

`get_sales_data` bir tarih aralığını `month`, `product` veya `region` bazında özetler. İsteğe bağlı ürün ve bölge filtresi vardır.

`get_product_sales_ranking` ürünleri `total_sales` veya `total_quantity` alanına göre sıralar. Sonuçta üst ve alt dilim birlikte döner.

Dönen satırdaki ad alanı `group_name`dir.

## Satış sorusu için açık kalması gerekenler

Üç süreç birden ayakta olmalıdır.

```powershell
cd D:\aws_agentic\sales-insight-agent
docker compose up -d
.\.venv\Scripts\python.exe -u -m query_server
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8081
```

Sorgu sunucusu yalnızca `127.0.0.1:8081` adresini dinler. `GET /health` cevabı `{"status":"ok"}` olmalıdır. `POST /sales` gövdesi `start_date`, `end_date` ve isteğe bağlı `product_name`, `region_name`, `group_by` alanlarını taşır.

## Ortam değişkenleri

Değerler `sales-insight-agent/.env` içindedir. Bu dosya commit edilmez.

| Değişken | Kullanan |
| --- | --- |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker ve veri yükleme |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Salt okunur sorgu bağlantısı |
| `AWS_REGION`, `BEDROCK_MODEL_ID` | Yerel ajanın kullandığı Bedrock modeli |
| `SALES_QUERY_URL` | Deploy sırasında runtime'a yazılan tünel adresi |

## Yerel ajan

Tünel gerekmez. Araçlar Postgres'e doğrudan bağlanır.

```powershell
cd D:\aws_agentic\sales-insight-agent
.\.venv\Scripts\python.exe main.py
```

Değerlendirme, ajanın ilk araç çağrısını beklenen araç ve parametrelerle karşılaştırır:

```powershell
.\.venv\Scripts\python.exe -m evaluations.run_evaluation
```

## AWS üzerinde çalıştırma

Komutlar `SalesInsightTemplate` klasöründen ve `eu-west-1` bölgesiyle çalışır.

```powershell
cd D:\aws_agentic\SalesInsightTemplate
$env:SALES_QUERY_URL = "https://<tünel-adresi>"
agentcore deploy --region eu-west-1
agentcore status --region eu-west-1
```

Deploy öncesinde `app\agent\.env` paketinin dışına alınır. CodeZip, gitignore'da olsa da bu dosyayı arşive koyabilir. Deploy bitince dosya yerine konur.

Çağrı aynı klasörden yapılır. Oturum kimliği 33 ile 256 karakter arasında olmalıdır. Aynı kimlik aynı konuşmayı sürdürür.

```powershell
agentcore invoke --region eu-west-1 --runtime agent --session-id "<33-256 karakter>" --payload '{"prompt":"2026-08-01 ile 2026-10-31 arasında aylık satışları getir"}'
```

PowerShell, JSON içindeki çift tırnakları native komuta geçirirken silebilir. Çağrı `400` ve `Invalid JSON` dönerse payload'ı tırnakları korunacak şekilde vermek gerekir.

Konsolda ajan, Amazon alışveriş hesabında görünmez. AWS konsolunda bölge Europe (Ireland) seçilir ve Amazon Bedrock AgentCore altındaki Agents listesine bakılır.
