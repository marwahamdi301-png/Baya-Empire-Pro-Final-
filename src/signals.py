import pandas as pd


def _is_valid(value):
    return value is not None and not pd.isna(value)


def generate_signal(df):
    clean = df.dropna(subset=["close"]).copy()

    if clean.empty or len(clean) < 50:
        return {
            "signal": "WAIT",
            "label": "انتظار",
            "score": 0,
            "confidence": 0,
            "color": "#aab3c5",
            "reasons": ["لا توجد بيانات كافية لحساب الإشارة."],
            "risk": "غير محدد",
        }

    last = clean.iloc[-1]

    close = last["close"]
    sma20 = last.get("SMA20")
    sma50 = last.get("SMA50")
    ema21 = last.get("EMA21")
    rsi = last.get("RSI14")
    macd = last.get("MACD")
    macd_signal = last.get("MACD_SIGNAL")

    score = 0
    reasons = []

    # Trend by SMA20
    if _is_valid(sma20):
        if close > sma20:
            score += 1
            reasons.append("السعر أعلى من SMA20: زخم قصير إيجابي.")
        else:
            score -= 1
            reasons.append("السعر أسفل SMA20: ضغط قصير سلبي.")

    # Trend by SMA50
    if _is_valid(sma50):
        if close > sma50:
            score += 1
            reasons.append("السعر أعلى من SMA50: الاتجاه العام أفضل.")
        else:
            score -= 1
            reasons.append("السعر أسفل SMA50: الاتجاه العام ضعيف.")

    # MA Cross
    if _is_valid(sma20) and _is_valid(sma50):
        if sma20 > sma50:
            score += 1
            reasons.append("SMA20 أعلى من SMA50: ميل صاعد.")
        else:
            score -= 1
            reasons.append("SMA20 أسفل SMA50: ميل هابط.")

    # EMA21
    if _is_valid(ema21):
        if close > ema21:
            score += 1
            reasons.append("السعر أعلى من EMA21: دعم ديناميكي.")
        else:
            score -= 1
            reasons.append("السعر أسفل EMA21: ضعف زخم.")

    # RSI
    if _is_valid(rsi):
        if rsi < 30:
            score += 2
            reasons.append("RSI أقل من 30: تشبع بيع محتمل.")
        elif rsi > 70:
            score -= 2
            reasons.append("RSI أعلى من 70: تشبع شراء محتمل.")
        elif 45 <= rsi <= 60:
            score += 1
            reasons.append("RSI في منطقة متوازنة تميل للإيجابية.")
        elif 40 <= rsi < 45:
            score -= 1
            reasons.append("RSI أقل من 45: زخم متوسط ضعيف.")

    # MACD
    if _is_valid(macd) and _is_valid(macd_signal):
        if macd > macd_signal:
            score += 1
            reasons.append("MACD أعلى من خط الإشارة: زخم إيجابي.")
        else:
            score -= 1
            reasons.append("MACD أسفل خط الإشارة: زخم سلبي.")

    if score >= 3:
        signal = "BUY"
        label = "شراء تجريبي"
        color = "#00ff88"
    elif score <= -3:
        signal = "SELL"
        label = "بيع / تخفيف تجريبي"
        color = "#ff0055"
    else:
        signal = "HOLD"
        label = "انتظار / مراقبة"
        color = "#ffaa00"

    confidence = min(95, 45 + abs(score) * 8)

    if confidence >= 75:
        risk = "متوسط"
    elif confidence >= 60:
        risk = "مرتفع"
    else:
        risk = "مرتفع جداً"

    return {
        "signal": signal,
        "label": label,
        "score": score,
        "confidence": confidence,
        "color": color,
        "reasons": reasons,
        "risk": risk,
    }
