# Convert BRL to BTC (Market)

A simple Python tool to convert Brazilian Real (BRL) to Bitcoin (BTC) using real-time market data. This project fetches the latest BTC/BRL exchange rate from the **CoinGecko API** and calculates the equivalent amount of BTC for a given BRL value.

---

## Features

- **Real-time Conversion**: Fetches the latest BTC/BRL exchange rate from the CoinGecko API.
- **Easy-to-Use**: Simple interface using Streamlit to view the convert values and create a QRCode using your public wallet key.
- **Lightweight**: Minimal dependencies and fast execution.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)

Install the required library using pip:

```bash
pip install requests streamlit qrcode

streamlit run main.py
```

## View Example

In this site in the Streamlit Deploy you can see the project running: [Convert BRL to BTC](https://convert-brl-btc-market.streamlit.app/)