from django.shortcuts import render

def trading_view(request):
    trading_pairs = {
        'EURUSD': 'EUR/USD',
        'XAUUSD': 'GOLD',
        'GBPUSD': 'GBP/USD',
        'USDJPY': 'USD/JPY',
        'BTCUSD': 'BTC/USD',
        'ETHUSD': 'ETH/USD'
    }
    
    context = {
        'trading_pairs': trading_pairs,
        'default_pair': 'EURUSD'
    }
    return render(request, 'trading/trading.html', context)
