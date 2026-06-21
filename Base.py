import requests
import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd

TWELVE_API_KEY = "f57a1d26e5bf4789b9b12116c37124b5"
BASE_URL = "https://api.twelvedata.com/time_series"
def fetch_twelve_data(symbol, interval="1day", outputsize=1260):
        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVE_API_KEY,
            "format": "JSON"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if "values" not in data:
            print(f"No valid data for ticker {symbol}.")
            return None
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna(subset=["close"])
        return df

def plot_and_compare(simulations, steps, n, ticker, median_path, benchmark_data, benchmark_annualized_return, benchmark_volatility, dt):
        plt.figure(figsize=(10, 6))
        for i in range(n):
            plt.plot(simulations[:, i], color='blue', alpha=0.01)
        plt.plot(median_path, color='orange', linewidth=2, label='Median Path')
        plt.fill_between(np.arange(steps), median_path, median_path[0], color='orange', alpha=0.2)
        stock_pct = (median_path[-1] - median_path[0]) / median_path[0] * 100
        benchmark_simulations = np.zeros((steps, n))
        benchmark_current_price = float(benchmark_data["close"].iloc[-1])
        for i in range(n):
            prices = [benchmark_current_price]
            for _ in range(steps):
                Z = np.random.normal()
                new_price = prices[-1] * np.exp((benchmark_annualized_return - 0.5 * benchmark_volatility**2) * dt + benchmark_volatility * np.sqrt(dt) * Z)
                prices.append(new_price)
            benchmark_simulations[:, i] = prices[1:steps+1]
        benchmark_median_path = np.median(benchmark_simulations, axis=1)
        benchmark_pct = (benchmark_median_path[-1] - benchmark_median_path[0]) / benchmark_median_path[0] * 100
        print(f"\nStockMedRet: {stock_pct:.2f}%")
        print(f"BenchMedRet: {benchmark_pct:.2f}%")
        print("Stock > Benchmark" if stock_pct > benchmark_pct else "Benchmark > Stock")
        plt.title(f"MC Sim {ticker}")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

entrada = input("Stocks: ").upper().split()
print(",".join(entrada))
tickers = [e.strip() for e in entrada if e.strip()]

if not tickers:
        print("Ticker symbol cannot be empty.")
        sys.exit()

t = float(input("Enter the time in years for simulation: "))
n = 1000
steps = 252
dt = t / steps

benchmark = "SPY"  # S&P 500 ETF
benchmark_data = fetch_twelve_data(benchmark)
if benchmark_data is None or benchmark_data.empty:
        print(f"No valid data for benchmark {benchmark}.")
        sys.exit()
benchmark_returns = benchmark_data["close"].pct_change().dropna()
benchmark_volatility = float(benchmark_returns.std() * np.sqrt(252))
benchmark_annualized_return = float(benchmark_returns.mean() * 252)

resultados = []
def new_func(steps, simulations, i, prices):
    simulations[:, i] = prices[1:steps+1]

for ticker in tickers:
        print(f"\n{'='*20}\nSim: {ticker}")
        stock_data = fetch_twelve_data(ticker)
        if stock_data is None or stock_data.empty:
            print(f"No valid data for ticker {ticker}.")
            continue
        returns = stock_data["close"].pct_change().dropna()
        volatility = float(returns.std() * np.sqrt(252))
        annualized_return = float(returns.mean() * 252)
        current_price = float(stock_data["close"].iloc[-1])
        risk_free_rate = 0.03
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility != 0 else float('nan')
        print(f"Tkr: {ticker}")
        print(f"AnnRet: {annualized_return:.2%}")
        print(f"AnnVol: {volatility:.2%}")
        print(f"Sharpe: {sharpe_ratio:.2f}")
        print(f"CurPx: ${current_price:.2f}")
        simulations = np.zeros((steps, n))
        for i in range(n):
            prices = [current_price]
            for _ in range(steps):
                Z = np.random.normal()
                new_price = prices[-1] * np.exp((annualized_return - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * Z)
                prices.append(new_price)
            new_func(steps, simulations, i, prices)
        final_prices = simulations[-1]
        p5, p50, p95 = np.percentile(final_prices, [5, 50, 95])
        print(f"\n[Final Pct]")
        print(f"P5: ${p5:.2f}")
        print(f"P50: ${p50:.2f}")
        print(f"P95: ${p95:.2f}")
        prob_profit = np.mean(final_prices > current_price)
        print(f"\nProbProfit {t}y: {prob_profit:.2%}")
        resultados.append({
            'Ticker': ticker,
            'Retorno anualizado (%)': annualized_return * 100,
            'Volatilidade anualizada (%)': volatility * 100,
            'Sharpe Ratio': sharpe_ratio,
            'Preço atual': current_price,
            'Percentil 5%': p5,
            'Mediana (50%)': p50,
            'Percentil 95%': p95,
            'Probabilidade de lucro (%)': prob_profit * 100
        })
        median_path = np.median(simulations, axis=1)
        plot_and_compare(simulations, steps, n, ticker, median_path, benchmark_data, benchmark_annualized_return, benchmark_volatility, dt)

def plot_and_compare(simulations, steps, n, ticker, median_path, benchmark_data, benchmark_annualized_return, benchmark_volatility, dt):


        plt.figure(figsize=(10, 6))

        for i in range(n):
            plt.plot(simulations[:, i], color='blue', alpha=0.01)
        plt.plot(median_path, color='orange', linewidth=2, label='Median Path')
        plt.fill_between(np.arange(steps), median_path, median_path[0], color='orange', alpha=0.2)

        stock_pct = (median_path[-1] - median_path[0]) / median_path[0] * 100
        benchmark_s = np.zeros((steps, n))
        benchmark_price = float(benchmark_data['Close'].iloc[-1])



        for i in range(n):
            prices = [benchmark_price]
            for _ in range(steps):
                Z = np.random.normal()
                new_price = prices[-1] * np.exp((benchmark_annualized_return - 0.5 * benchmark_volatility**2) * dt + benchmark_volatility * np.sqrt(dt) * Z)
                prices.append(new_price)
            benchmark_s[:, i] = prices[1:steps+1]


        benchmark_median_path = np.median(benchmark_s, axis=1)
        benchmark_pct = (benchmark_median_path[-1] - benchmark_median_path[0]) / benchmark_median_path[0] * 100


        print(f"\nStockMedRet: {stock_pct:.2f}%")
        print(f"BenchMedRet: {benchmark_pct:.2f}%")
        print("Stock > Benchmark" if stock_pct > benchmark_pct else "Benchmark > Stock")

        plt.title(f"{ticker} Simulated")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
