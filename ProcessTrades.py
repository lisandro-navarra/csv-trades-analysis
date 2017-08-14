import os
import csv
import sys
from operator import itemgetter
from itertools import groupby


class ProcessTrades():
    def __init__(self, ifilename, ofilename, columns):
        assert(os.path.isfile(ifilename))
        assert(isinstance(columns, list))
        self.ifilename = ifilename
        self.ofilename = ofilename
        self.columns = columns

    def group_trade_data(self):
        with open(self.ifilename, mode='r', buffering=1) as tradesFile:
            trades = []
            reader = csv.reader(tradesFile)
            for row in reader:
                trades.append(dict(zip(self.columns, row)))
        trades.sort(key=itemgetter('symbol'))
        return groupby(trades, key=itemgetter('symbol'))

    def process_file(self):
        trade_data = self.group_trade_data()

        with open(self.ofilename, 'wb') as output:
            csvwriter = csv.writer(output)
            for symbol, data in trade_data:
                items = [x for x in data]
                max_price = max([int(x['price']) for x in items])
                max_time_gap = max([int(x['timestamp']) for x in items]) - min([int(x['timestamp']) for x in items])
                volume = sum([int(x['quantity']) for x in items])
                weighted_avg_price = sum([int(x['quantity']) * int(x['price']) for x in items]) / volume
                csvwriter.writerow([symbol, max_time_gap, volume, weighted_avg_price, max_price])



if __name__=="__main__":
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    process_trades = ProcessTrades(input_filename,
                                   output_filename,
                                   columns = ['timestamp',
                                              'symbol',
                                              'quantity',
                                              'price'])
    process_trades.process_file()


