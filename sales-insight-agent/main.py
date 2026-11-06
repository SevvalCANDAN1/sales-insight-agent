
from agent.sales_agent import create_sales_agent


def main():
    print("=" * 50)
    print("       SALES INSIGHT AGENT")
    print("=" * 50)
    print("Satış verileriniz hakkında sorularınızı sorabilirsiniz.")
    print("Çıkmak için 'exit' yazın.\n")

    # Agent'ı oluştur
    sales_agent = create_sales_agent()

    while True:
        user_input = input("\nSiz: ").strip()

        if user_input.lower() in ["exit", "quit", "çıkış"]:
            print("\nSales Insight Agent kapatılıyor...")
            break

        if not user_input:
            continue

        try:
            print("\nAgent analiz yapıyor...\n")

            response = sales_agent(user_input)

            print("Sales Agent:")
            print(response)

        except Exception as e:
            print(f"\nBir hata oluştu: {e}")


if __name__ == "__main__":
    main()
