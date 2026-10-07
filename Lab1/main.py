import requests
import matplotlib.pyplot as plt
from datetime import date, timedelta

CURRENCIES = ["USD", "EUR"]
DAYS = 7

days = [date.today() - timedelta(days=i) for i in range(DAYS, 0, -1)]
labels = [d.strftime("%d.%m") for d in days]


def get_rate(currency, day):
    url = (
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
        f"?valcode={currency}&date={day.strftime('%Y%m%d')}&json"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[0]["rate"] if data else None
    except Exception as e:
        print(f"Помилка {currency} {day}: {e}")
        return None


plt.figure(figsize=(10, 5))

for cur in CURRENCIES:
    rates = [get_rate(cur, d) for d in days]
    print(cur, rates)
    plt.plot(labels, rates, marker="o", linewidth=2, label=f"{cur}/UAH")
    for x, y in zip(labels, rates):
        if y is not None:
            plt.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                         xytext=(0, 8), ha="center", fontsize=8)

plt.title("Курс валют НБУ за останній тиждень")
plt.xlabel("Дата")
plt.ylabel("Курс, грн")
plt.grid(True, alpha=0.3)
plt.legend()
plt.margins(y=0.15)
plt.tight_layout()
plt.savefig("rates.png", dpi=150)
plt.show()