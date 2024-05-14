import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_currency_data(date):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
        async with session.get(url) as response:
            return await response.json()

async def get_exchange_rates(days):
    tasks = []
    current_date = datetime.now()

    for i in range(days):
        date = (current_date - timedelta(days=i)).strftime("%d.%m.%Y")
        tasks.append(fetch_currency_data(date))

    results = await asyncio.gather(*tasks)
    return results

# Курс валют багатьох країн
# def print_exchange_rates(results):
#     for result in results:
#         print(result)

def print_exchange_rates(results):
    for result in results:
        exchange_date = result.get("date")
        exchange_rates = result.get("exchangeRate")
        for rate in exchange_rates:
            currency = rate.get("currency")
            if currency in ("EUR", "USD"):
                print(f"Date: {exchange_date}, {rate}")



async def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if days > 10:
        print("Error: Maximum number of days allowed is 10")
        return

    exchange_rates = await get_exchange_rates(days)
    print_exchange_rates(exchange_rates)

if __name__ == "__main__":
    asyncio.run(main())
