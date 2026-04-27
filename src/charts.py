import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_market_chart(df, symbol, interval_label):
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.035,
        row_heights=[0.60, 0.20, 0.20],
        subplot_titles=(
            f"{symbol} — Candles + MA",
            "RSI 14",
            "MACD"
        )
    )

    fig.add_trace(
        go.Candlestick(
            x=df["time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing_line_color="#00f2ff",
            decreasing_line_color="#ff0055",
            increasing_fillcolor="rgba(0, 242, 255, 0.45)",
            decreasing_fillcolor="rgba(255, 0, 85, 0.45)",
            name="Candles",
        ),
        row=1,
        col=1
    )

    if "SMA20" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["SMA20"],
                mode="lines",
                line=dict(color="#ffaa00", width=1.6),
                name="SMA20",
            ),
            row=1,
            col=1
        )

    if "SMA50" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["SMA50"],
                mode="lines",
                line=dict(color="#a855f7", width=1.6),
                name="SMA50",
            ),
            row=1,
            col=1
        )

    if "EMA21" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["EMA21"],
                mode="lines",
                line=dict(color="#00ff88", width=1.4),
                name="EMA21",
            ),
            row=1,
            col=1
        )

    if "RSI14" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["RSI14"],
                mode="lines",
                line=dict(color="#00f2ff", width=1.8),
                name="RSI14",
            ),
            row=2,
            col=1
        )

        fig.add_hline(y=70, line_dash="dash", line_color="#ff0055", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00ff88", row=2, col=1)

    if "MACD" in df.columns and "MACD_SIGNAL" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["MACD"],
                mode="lines",
                line=dict(color="#00f2ff", width=1.6),
                name="MACD",
            ),
            row=3,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["MACD_SIGNAL"],
                mode="lines",
                line=dict(color="#ffaa00", width=1.4),
                name="MACD Signal",
            ),
            row=3,
            col=1
        )

        fig.add_trace(
            go.Bar(
                x=df["time"],
                y=df["MACD_HIST"],
                marker_color="#666666",
                name="MACD Hist",
            ),
            row=3,
            col=1
        )

    fig.update_layout(
        template="plotly_dark",
        height=760,
        xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=60, b=10),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title=f"{symbol} / {interval_label}",
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")

    return fig
