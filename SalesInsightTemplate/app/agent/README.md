# Sales Insight runtime

AgentCore üzerinde çalışan satış ajanı. Sistemin tamamı depo kökündeki `README.md` dosyasında.

`main.py` gelen isteği alır. `parse.py` gövdeyi okur, `model/load.py` Bedrock modelini açar, Strands ajanı iki aracı kullanır: `get_sales_data` ve `get_product_sales_ranking`. Araçlar `tools/query_client.py` ile `SALES_QUERY_URL/sales` adresine gider.

## İstek

- `prompt`: kullanıcının cümlesi.
- `messages`: konuşma geçmişi. Doluysa ajan bu geçmişi kullanır.
- `actorId`: hafızada kullanıcıyı ayırır. Boşsa `default` olur.

Oturum kimliği `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` başlığından gelir. Aynı kimlik aynı konuşmayı sürdürür.

`SALES_QUERY_URL` deploy sırasında runtime ortamına yazılır. Tünel adresi değişince runtime bu değerle yeniden deploy edilir.
