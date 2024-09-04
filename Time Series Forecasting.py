import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')

# Get today's date and calculate the start date (one year ago)
today = date.today()
end_date = today.strftime("%Y-%m-%d")
start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")

# Download GOOG stock data
data = yf.download('GOOG', start=start_date, end=end_date, progress=False)

# Create a new 'Date' column and rearrange the columns
data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)

# Display the last 5 rows of the data
print(data.tail())

# Extract the 'Date' and 'Close' columns for time series analysis
data = data[["Date", "Close"]]
print(data.head())

# Plot the decomposed components of the time series (Trend, Seasonality, Residuals)
result = seasonal_decompose(data["Close"], model='multiplicative', period=30)
result.plot()
plt.gcf().set_size_inches(15, 10)
plt.show()

# Plot autocorrelation for the 'Close' prices
pd.plotting.autocorrelation_plot(data["Close"])
plt.show()

# Plot partial autocorrelation
plot_pacf(data["Close"], lags=30)  # Reduced lags to 30 for clarity
plt.show()

# Set parameters for ARIMA model
p, d, q = 5, 1, 2

# Fit ARIMA model (Note: 'ARIMA' is now from 'statsmodels.tsa.arima.model')
model = ARIMA(data["Close"], order=(p, d, q))
fitted = model.fit()
print(fitted.summary())

# Forecast using the ARIMA model
predictions_arima = fitted.predict(start=len(data), end=len(data)+10, typ='levels')
print(predictions_arima)

# Fit SARIMA model
sarima_model = sm.tsa.statespace.SARIMAX(data['Close'], 
                                         order=(p, d, q), 
                                         seasonal_order=(p, d, q, 12))
sarima_fitted = sarima_model.fit()
print(sarima_fitted.summary())

# Forecast using the SARIMA model
predictions_sarima = sarima_fitted.predict(start=len(data), end=len(data)+10)
print(predictions_sarima)

# Plot the training data and predictions
plt.figure(figsize=(15, 10))
plt.plot(data["Close"], label="Training Data")
plt.plot(range(len(data), len(data) + 11), predictions_arima, label="ARIMA Predictions", color="red")
plt.plot(range(len(data), len(data) + 11), predictions_sarima, label="SARIMA Predictions", color="green")
plt.legend()
plt.show()
