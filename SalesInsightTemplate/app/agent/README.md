# Sales Insight runtime

Bu süreç, satış ajanının AWS üzerinde çalışan kopyasıdır. Sistemin tamamı depo kökündeki `README.md` dosyasında anlatılır.

`main.py` bir AgentCore giriş noktasıdır. Gelen JSON `parse.py` ile okunur, model `model/load.py` ile açılır ve Strands ajanı iki aracı kullanır:

- `get_sales_data`
- `get_product_sales_ranking`

İki araç da `tools/query_client.py` üzerinden `SALES_QUERY_URL/sales` adresine istek atar. Bu süreç Postgres şifresini kullanmaz. Veritabanı laptopta kalır; buraya dönen kayıt sorgunun toplu sonucudur.

## İstek

Gövde bir JSON nesnesidir.

- `prompt` tek bir kullanıcı cümlesidir. `messages` yoksa bu alan kullanılır.
- `messages` konuşma geçmişidir. Varsa `prompt` yerine geçer. Sondaki `toolUse` blokları atılır.
- `actorId` hafızada kullanıcıyı ayırır. Boşsa `default` kabul edilir.

Oturum kimliği gövdede değildir. `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` başlığından gelir. Aynı kimlik aynı ajan oturumunu sürdürür. Kimlik 33 ile 256 karakter arasında olmalıdır.

```json
{ "prompt": "2026-08-01 ile 2026-10-31 arasında aylık satışları getir", "actorId": "sales-user" }
```

## Ortam

| Değişken | Görevi |
| --- | --- |
| `SALES_QUERY_URL` | Laptopta çalışan sorgu servisinin tünel adresi. Deploy sırasında CDK bu değeri runtime'a yazar. Boşsa satış araçları hata verir |
| `MEMORY_AGENTMEMORY_ID` | Doluysa AgentCore Memory oturumu açılır |

`SALES_QUERY_URL` kaynak kodda durmaz. Tünel yeniden açıldığında adres değişir ve runtime yeni değerle tekrar deploy edilir.

## Çalıştırma

Yerel deneme `agentcore dev` ile `8080` portunda açılır. Deploy ve çağrı `SalesInsightTemplate` klasöründen, bölge `eu-west-1` olacak şekilde yapılır. Ayrıntılı komutlar kök `README.md` içindedir.
