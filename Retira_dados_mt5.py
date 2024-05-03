import MetaTrader5 as mt5
import pandas as pd

def initialize_mt5():
    """ Inicializa a conexão com o MT5 se ainda não estiver conectado. """
    if not mt5.initialize():
        print("Erro na inicialização do MT5")
        return False
    return True

def shutdown_mt5():
    """ Encerra a conexão com o MT5 se estiver conectado. """
    if mt5.terminal_info() is not None:
        mt5.shutdown()

def get_symbol_info(symbol):
    """ Obtém informações do símbolo no MT5. """
    info_symbol = mt5.symbol_info(symbol)
    if info_symbol is None:
        print(f"O símbolo {symbol} não foi encontrado.")
        return None
    return info_symbol

def fetch_mini_index(symbol, timeframe, count):
    """ Busca os dados históricos do mini índice do MT5. """
    if not initialize_mt5():
        return None

    if not get_symbol_info(symbol):
        shutdown_mt5()
        return None

    prices = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    shutdown_mt5()

    if prices is None or len(prices) == 0:
        print("Não foi possível obter os dados históricos.")
        return None

    df = pd.DataFrame(prices)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Exemplo de uso
symbol = "WIN$"
timeframe = mt5.TIMEFRAME_M1
quantity = 14400
data_frame = fetch_mini_index(symbol, timeframe, quantity)
# Salvar o DataFrame em um arquivo CSV na pasta "Downloads"
data_frame.to_csv('/Users/maibrothao/Downloads/mtwin14400.csv', index=False)


