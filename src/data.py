import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=30, show_spinner=False)
def get_ticker(symbol, base_url):
    try:
        url = f"{base_url}/api/v3/ticker/24hr"
        response = requests.get(
            url,
            params={"symbol": symbol},
            timeout=8
        )

        try:
            data = response.json()
        except Exception:
            return None, "استجابة غير صالحة من السيرفر."

        if response.status_code != 200:
            if isinstance(data, dict):
                return None, data.get("msg", f"HTTP Error {response.status_code}")
            return None, f"HTTP Error {response.status_code}"

        return {
            "symbol": symbol,
            "price": float(data["lastPrice"]),
            "change": float(data["priceChangePercent"]),
            "high": float(data["highPrice"]),
            "low": float(data["lowPrice"]),
            "volume": float(data["volume"]),
        }, None

    except requests.exceptions.RequestException as e:
        return None, f"خطأ اتصال: {e}"

    except Exception as e:
        return None, f"خطأ معالجة البيانات: {e}"


@st.cache_data(ttl=60, show_spinner=False)
def get_klines(symbol, interval, limit, base_url):
    try:
        url = f"{base_url}/api/v3/klines"
        response = requests.get(
            url,
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit,
            },
            timeout=8
        )

        try:
            data = response.json()
        except Exception:
            return None, "استجابة غير صالحة من السيرفر."

        if response.status_code != 200:
            if isinstance(data, dict):
                return None, data.get("msg", f"HTTP Error {response.status_code}")
            return None, f"HTTP Error {response.status_code}"

        if not isinstance(data, list):
            return None, "صيغة بيانات الشموع غير صحيحة."

        columns = [
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ]

        df = pd.DataFrame(data, columns=columns)

        df["time"] = pd.to_datetime(df["time"], unit="ms")

        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["open", "high", "low", "close"])

        return df, None

    except requests.exceptions.RequestException as e:
        return None, f"خطأ اتصال: {e}"

    except Exception as e:
        return None, f"خطأ معالجة الشموع: {e}"
