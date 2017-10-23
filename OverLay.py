import datetime
import ast
import time
import matplotlib.pyplot as plt
import numpy as np

plt.rcdefaults()

# This version of Accel_graph.py is working off of IB's feed back

class hq:
    def __init__(self):
        d = datetime.datetime.now()
        self.path = "C:\\auto_ana\\file_2017_10_20_roi.txt"
        self.date_ran = None
        self.entries = {}
        self.scanned_pre_market = 0
        self.scanned_after_open = 0
        self.scanned_after_midday = 0
        self.overall_roi = 0.0
        self.total_money_entry = 0.0
        self.total_money_exit = 0.0
        self.starting_ammount = 10000
        # self.entries = {'AXTA; {'ROI': -0.036, 'Entry Price': 28.09, 'Region': 1, 'Scan_Time': 1018.0520000000033,
        # 'Entry Time': 1718.0520000000033, 'Exit Price': 28.08,}
        # 'ATHM' {'ROI': 1.51, 'Entry Price': 55.45, 'Region': 7, 'Scan_Time': 219.862000000001,
        # 'Entry Time': 14414.262999999999, 'Exit Price': 56.3}}
        self.positives = 0
        self.negatives = 0
        self.total = 0
        start = 2340
        self.regions = [[0, start, 1], [start, start * 2, 2], [start * 2, start * 3, 3], [start * 3, start * 4, 4],
                        [start * 4, start * 5, 5], [start * 5, start * 6, 6], [start * 6, start * 7, 7],
                        [start * 7, start * 8, 8], [start * 8, start * 9, 9], [start * 9, start * 10, 10]]
        self.region_totals = {'Region1': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region2': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region3': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region4': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region5': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region6': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region7': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region8': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region9': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0},
                              'Region10': {'Entry': 0, 'Exit': 0, 'ROI': 0, 'N_Trades': 0}}

        self.r1_pos = 0
        self.r1_neg = 0

        self.r2_pos = 0
        self.r2_neg = 0

        self.r3_pos = 0
        self.r3_neg = 0

        self.r4_pos = 0
        self.r4_neg = 0

        self.r5_pos = 0
        self.r5_neg = 0

        self.r6_pos = 0
        self.r6_neg = 0

        self.r7_pos = 0
        self.r7_neg = 0

        self.r8_pos = 0
        self.r8_neg = 0

        self.r9_pos = 0
        self.r9_neg = 0

        self.r10_pos = 0
        self.r10_neg = 0

        date_ran = None
        self.dates_1 = ""
        self.dates_2 = ""
        self.dates_3 = ""
        self.dates_4 = ""
        self.dates_5 = ""

        self.trades_in_bracket = {'Bracket_1': {'Trades': 0},
                                  'Bracket_2': {'Trades': 0},
                                  'Bracket_3': {'Trades': 0},
                                  'Bracket_4': {'Trades': 0},
                                  'Bracket_5': {'Trades': 0},
                                  'Bracket_6': {'Trades': 0},
                                  'Bracket_7': {'Trades': 0}}

        self.listOdDups = []

        # For IB Data Set
        self.ib_entries = {}
        self.starting_dollar_amount = None
        self.ib_total_money_entry = 0.0
        self.ib_total_money_exit = 0.0
        self.ib_overall_roi = 0.0

        self.scan_times = {}
        self.starting_ammount = 60000
        self.list_ofrunning_secs = []
        self.list_of_running_rois = []
        self.list_of_secs_amount_left_in_account = [0]
        self.list_of_prices_amount_left_in_account = [self.starting_ammount]

    def time_to_secs(self, msg):

        msg_ = msg.split(':')
        hours = int(msg_[0])
        mins = int(msg_[1])
        secs = int(msg_[2])
        return (hours * 3600) + (mins * 60) + secs - 34200

    def IB_entry(self, msg):
        msg_split = msg.split(",")
        symbol = msg_split[1]
        seconds_from_open = int(msg_split[2]) + 34200
        price = float(msg_split[3])
        shares_bought = int(msg_split[4])
        total_money_spent = float(msg_split[5])
        account_balance = float(msg_split[6])
        human_entry_time = str(datetime.timedelta(seconds=seconds_from_open))
        seconds_at_buy = self.time_to_secs(human_entry_time)
        if self.list_of_secs_amount_left_in_account[-1] < seconds_at_buy:
            self.list_of_secs_amount_left_in_account.append(seconds_at_buy)
            self.list_of_prices_amount_left_in_account.append(account_balance)

        if symbol in self.ib_entries:
            # ToDO: Handel Multiple Entries
            print "DEBUG: Multiple Symbols Found: ", symbol
            time.sleep(5)
        else:
            self.ib_entries[symbol] = {}
            self.ib_entries[symbol].update({'Entry Time': seconds_at_buy,
                                         "Entry Price": price,
                                         "Shares Purchased": shares_bought,
                                         "Total Spent": total_money_spent,
                                         "Account Balance": account_balance,
                                         "Human Time": human_entry_time})

    def IB_exit(self, msg):
        msg_split = msg.split(",")
        symbol = msg_split[1]
        seconds_from_open = int(msg_split[2]) + 34200
        price = float(msg_split[3])
        shares_sold = int(msg_split[4])
        total_money_spent = float(msg_split[5])
        account_balance = float(msg_split[6])
        human_exit_time = str(datetime.timedelta(seconds=seconds_from_open))
        seconds_at_sell = self.time_to_secs(human_exit_time)
        if self.list_of_secs_amount_left_in_account[-1] < seconds_at_sell:
            self.list_of_secs_amount_left_in_account.append(seconds_at_sell)
            self.list_of_prices_amount_left_in_account.append(account_balance)


        if symbol in self.ib_entries:
            difference = total_money_spent - self.ib_entries[symbol]["Total Spent"]
            roi = ((total_money_spent - self.ib_entries[symbol]["Total Spent"]) /
                   self.ib_entries[symbol]["Total Spent"]) * 100
            self.ib_entries[symbol].update({'Exit Time': seconds_at_sell,
                                         "Exit Price": price,
                                         "Shares Sold": shares_sold,
                                         "Total Spent at Exit": total_money_spent,
                                         "Price Diff": difference,
                                         "ROI": round(roi, 2),
                                         "Account Balance at Exit": account_balance,
                                         "Human Time": human_exit_time})
        else:
            print "DEBUG: No matching symbol in IB_Entries: ", symbol
            time.sleep(5)

    def process_msg_date(self, msg):
        if "MARKET TIME" in msg:
            msg_split = msg.split(",")
            index = len(msg_split) - 1

            dia = (msg_split[index])[11:22]
            self.date_ran = dia

    def get_scan_time_exit(self, msg):
        msg_split = msg.split(",")
        for obj in msg_split:
            if "symbol" in obj:
                symbol =  obj[8:]
                self.scan_times[symbol] = symbol
        for obj in msg_split:
            if "scan_info" in obj:
                this_much = 34 + len(symbol)
                and_this = this_much + 8
                self.scan_times[symbol] = obj[this_much:and_this]

    def RunningROI_(self, msg):

        msg = msg.split(",")
        Running_roi = msg[0][12:]
        print Running_roi
        Secs = msg[1]

        self.list_ofrunning_secs.append(Secs)
        self.list_of_running_rois.append(Running_roi)

    def dispatcher(self, msg):
        if "|EnterPositionIB|" in msg:
            self.IB_entry(msg)
        elif "|ExitPositionIB|" in msg:
            self.IB_exit(msg)
        elif "MARKET TIME" in msg and self.date_ran is None:
            self.process_msg_date(msg)
        elif "EventSignalExitPosition" in msg:
            self.get_scan_time_exit(msg)
        elif "EventSignalEndOfDayCloseAll" in msg:
            self.get_scan_time_exit(msg)
        elif "RunningROI" in msg:
            self.RunningROI_(msg)




    def get_all(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line != "\n" and line != "\r":
                    self.dispatcher(line)

    def assign_region_to_stock(self):
        # Determine what region they belong to
        for symbol, values in self.ib_entries.items():
            for [low, high, region] in self.regions:
                if values["Entry Time"] > low and values["Entry Time"] <= high:
                    self.ib_entries[symbol]["Region"] = region
                    break

    def break_down_region(self):
        # Disperse the total money amongst regions
        for key, values in self.ib_entries.items():
            if values["Region"] == 1:
                self.region_totals['Region1']['Entry'] += values['Entry Price']
                self.region_totals['Region1']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r1_pos += 1
                else:
                    self.r1_neg += 1

            elif values["Region"] == 2:
                self.region_totals['Region2']['Entry'] += values['Entry Price']
                self.region_totals['Region2']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r2_pos += 1
                else:
                    self.r2_neg += 1
            elif values["Region"] == 3:
                self.region_totals['Region3']['Entry'] += values['Entry Price']
                self.region_totals['Region3']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r3_pos += 1
                else:
                    self.r3_neg += 1
            elif values["Region"] == 4:
                self.region_totals['Region4']['Entry'] += values['Entry Price']
                self.region_totals['Region4']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r4_pos += 1
                else:
                    self.r4_neg += 1
            elif values["Region"] == 5:
                self.region_totals['Region5']['Entry'] += values['Entry Price']
                self.region_totals['Region5']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r5_pos += 1
                else:
                    self.r5_neg += 1
            elif values["Region"] == 6:
                self.region_totals['Region6']['Entry'] += values['Entry Price']
                self.region_totals['Region6']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r6_pos += 1
                else:
                    self.r6_neg += 1
            elif values["Region"] == 7:
                self.region_totals['Region7']['Entry'] += values['Entry Price']
                self.region_totals['Region7']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r7_pos += 1
                else:
                    self.r7_neg += 1
            elif values["Region"] == 8:
                self.region_totals['Region8']['Entry'] += values['Entry Price']
                self.region_totals['Region8']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r8_pos += 1
                else:
                    self.r8_neg += 1
            elif values["Region"] == 9:
                self.region_totals['Region9']['Entry'] += values['Entry Price']
                self.region_totals['Region9']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r9_pos += 1
                else:
                    self.r9_neg += 1
            elif values["Region"] == 10:
                self.region_totals['Region10']['Entry'] += values['Entry Price']
                self.region_totals['Region10']['Exit'] += values['Exit Price']
                if values["ROI"] > 0.0:
                    self.r10_pos += 1
                else:
                    self.r10_neg += 1

    def get_roi_for_each_region(self):
        # Calculate ROI for each region
        for key, values in self.region_totals.items():
            if values['Entry'] != 0:
                roi = round((((values['Exit'] - values['Entry']) / values['Entry']) * 100), 2)
                self.region_totals[key]['ROI'] = roi

    def count_trades(self):
        self.positives = self.r1_pos + self.r2_pos + self.r3_pos + self.r4_pos + self.r5_pos + self.r6_pos + self.r7_pos + self.r8_pos + self.r9_pos + self.r10_pos
        self.negatives = self.r1_neg + self.r2_neg + self.r3_neg + self.r4_neg + self.r5_neg + self.r6_neg + self.r7_neg + self.r8_neg + self.r9_neg + self.r10_neg
        self.region_totals['Region1']['N_Trades'] = self.r1_pos + self.r1_neg
        self.region_totals['Region2']['N_Trades'] = self.r2_pos + self.r2_neg
        self.region_totals['Region3']['N_Trades'] = self.r3_pos + self.r3_neg
        self.region_totals['Region4']['N_Trades'] = self.r4_pos + self.r4_neg
        self.region_totals['Region5']['N_Trades'] = self.r5_pos + self.r5_neg
        self.region_totals['Region6']['N_Trades'] = self.r6_pos + self.r6_neg
        self.region_totals['Region7']['N_Trades'] = self.r7_pos + self.r7_neg
        self.region_totals['Region8']['N_Trades'] = self.r8_pos + self.r8_neg
        self.region_totals['Region9']['N_Trades'] = self.r9_pos + self.r9_neg
        self.region_totals['Region10']['N_Trades'] = self.r10_pos + self.r10_neg
        self.total = len(self.entries)

    def total_roi(self):
        for values in self.ib_entries.values():
            self.total_money_entry += values['Entry Price']
            self.total_money_exit += values['Exit Price']
            self.overall_roi = round(
                (((self.total_money_exit - self.total_money_entry) / self.total_money_entry) * 100), 2)

            #self.overall_roi = 0.74
    def assign_bracket_to_stock(self):
        price_bracket = [[0.1, 1, 1], [1, 3, 2], [3, 5, 3], [5, 10, 4], [10, 25, 5], [25, 50, 6], [50, 100, 7]]
        for sym, values in self.ib_entries.items():
            for low, high, bra in price_bracket:
                # TODO: Make it assign what bracket it belongs to based on price at scan/open
                if values['Entry Price'] > low and values['Entry Price'] <= high:
                    self.ib_entries[sym]["Price Bracket"] = bra

    def get_roi_for_each_bracket(self):
        self.bracket_roi = {'Bracket_1': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_2': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_3': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_4': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_5': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_6': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0},
                            'Bracket_7': {'Entry Price': 0.0, 'Exit Price': 0.0, 'ROI': 0.0}}
        for key, values in self.ib_entries.items():
            if values['Price Bracket'] == 1:
                self.bracket_roi['Bracket_1']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_1']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_1']['Exit Price'] - self.bracket_roi['Bracket_1']['Entry Price']) /
                       self.bracket_roi['Bracket_1']['Entry Price']) * 100
                self.bracket_roi['Bracket_1']['ROI'] = roi
            elif values['Price Bracket'] == 2:
                self.bracket_roi['Bracket_2']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_2']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_2']['Exit Price'] - self.bracket_roi['Bracket_2']['Entry Price']) /
                       self.bracket_roi['Bracket_2']['Entry Price']) * 100
                self.bracket_roi['Bracket_2']['ROI'] = roi
            elif values['Price Bracket'] == 3:
                self.bracket_roi['Bracket_3']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_3']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_3']['Exit Price'] - self.bracket_roi['Bracket_3']['Entry Price']) /
                       self.bracket_roi['Bracket_3']['Entry Price']) * 100
                self.bracket_roi['Bracket_3']['ROI'] = roi
            elif values['Price Bracket'] == 4:
                self.bracket_roi['Bracket_4']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_4']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_4']['Exit Price'] - self.bracket_roi['Bracket_4']['Entry Price']) /
                       self.bracket_roi['Bracket_4']['Entry Price']) * 100
                self.bracket_roi['Bracket_4']['ROI'] = roi
            elif values['Price Bracket'] == 5:
                self.bracket_roi['Bracket_5']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_5']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_5']['Exit Price'] - self.bracket_roi['Bracket_5']['Entry Price']) /
                       self.bracket_roi['Bracket_5']['Entry Price']) * 100
                self.bracket_roi['Bracket_5']['ROI'] = roi
            elif values['Price Bracket'] == 6:
                self.bracket_roi['Bracket_6']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_6']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_6']['Exit Price'] - self.bracket_roi['Bracket_6']['Entry Price']) /
                       self.bracket_roi['Bracket_6']['Entry Price']) * 100
                self.bracket_roi['Bracket_6']['ROI'] = roi
            elif values['Price Bracket'] == 7:
                self.bracket_roi['Bracket_7']['Entry Price'] += values['Entry Price']
                self.bracket_roi['Bracket_7']['Exit Price'] += values['Exit Price']
                roi = ((self.bracket_roi['Bracket_7']['Exit Price'] - self.bracket_roi['Bracket_7']['Entry Price']) /
                       self.bracket_roi['Bracket_7']['Entry Price']) * 100
                self.bracket_roi['Bracket_7']['ROI'] = roi

    def count_trades_in_bracket(self):
        pass
        for values in self.ib_entries.values():
            if values['Price Bracket'] == 1:
                self.trades_in_bracket['Bracket_1']['Trades'] +=1
            elif values['Price Bracket'] == 2:
                self.trades_in_bracket['Bracket_2']['Trades'] +=1
            elif values['Price Bracket'] == 3:
                self.trades_in_bracket['Bracket_3']['Trades'] +=1
            elif values['Price Bracket'] == 4:
                self.trades_in_bracket['Bracket_4']['Trades'] +=1
            elif values['Price Bracket'] == 5:
                self.trades_in_bracket['Bracket_5']['Trades'] +=1
            elif values['Price Bracket'] == 6:
                self.trades_in_bracket['Bracket_6']['Trades'] +=1
            elif values['Price Bracket'] == 7:
                self.trades_in_bracket['Bracket_7']['Trades'] +=1

    def count_trades_in_bracket_perday(self):
        pass
        for values in self.entries.values():
            self.dates_1 = values['Date Ran']

    def add_scan_time_to_entries(self):
        for symbol, values in self.scan_times.items():
            try:
                secs = self.time_to_secs(values)
                self.ib_entries[symbol]["Scan Seconds"] = secs
            except:
                pass

    def run_program(self):
        self.get_all()
        self.assign_region_to_stock()
        self.assign_bracket_to_stock()
        self.break_down_region()
        self.get_roi_for_each_region()
        self.get_roi_for_each_bracket()
        self.count_trades()
        self.total_roi()
        self.count_trades_in_bracket()
        self.add_scan_time_to_entries()
        #self.count_trades_in_bracket_perday()

        self._plot()

    def _plot(self):

        # Overall Roi Graph

        fig = plt.figure(figsize=(12, 6))
        ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)


        plt.title("OverLay | Paper Trade \n" + str(self.date_ran))
        ax1.text(23480, 30, "End end Day ROI\n" + str(self.list_of_running_rois[-1]), size='medium')
        ax1.plot(self.list_ofrunning_secs, self.list_of_running_rois, 'b', linewidth=1)
        ax1.set_xlabel('Seconds from Open')

        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('ROI', color='b')
        ax1.tick_params('y', colors='b')
        ax1.axhline(0, color='k', linewidth=1)
        start = 2340
        ax1.set_xticks([0, 2340, start * 2, start * 3, start * 4, start * 5, start * 6, start * 7, start * 8, start * 9,
                        start * 10])

        ax2 = ax1.twinx()

        plt.plot(self.list_of_secs_amount_left_in_account, self.list_of_prices_amount_left_in_account, 'r', linewidth=1)
        ax2.set_ylabel('Account\nBalance', color='r')
        ax2.tick_params('y', colors='r')

        ax2.set_xticks([0, 2340, start * 2, start * 3, start * 4, start * 5, start * 6, start * 7, start * 8, start * 9,
                        start * 10])
        plt.xlim([0, 23400])
        fig.tight_layout()
        #plt.subplots_adjust(left=0.09, bottom=0.05, right=0.93, top=0.95, wspace=0.2, hspace=0)
        #fig = ax1.figure(figsize=(12, 12))
        plt.show()

        #plt.plot(self.list_ofrunning_secs, self.list_of_running_rois, label="G1", linewidth=1)
        #plt.plot(self.list_of_secs_amount_left_in_account, self.list_of_prices_amount_left_in_account, label="G1", linewidth=1)

x = hq()
x.run_program()