# OhlcvAnalyser

## What OhlcvAnalyser Do?
OhlcvAnalyser helps analyse OHLCV(Open, High, Low, Close, Volume) data.

## How to use OhlcvAnalyser

```
pip install OhlcvAnalyser
```

```python
from OhlcvAnalyser import MultiOhlcvAnalyser, SingleOhlcvAnaylser

from OhlcvAnalyser.analyser import (
    PriceAnalyser,
    ProfitAnalyser,
    VarianceAnalyser,
    CoefficientAnalyser,
)

from OhlcvAnalyser.plotter import Plotter
```

## Examples

### Info
![image](./README_ASSETS/00_multi_info.png)

### Price analysis
![image](./README_ASSETS/01_price_analyser.png)

### Coefficient analysis
![image](./README_ASSETS/02_coefficient_analyser.png)

### RegressionPlot
![image](./README_ASSETS/03_regression_plotter.png)

### OhlcvPlot
![image](./README_ASSETS/04_ohlcv_plotter.png)