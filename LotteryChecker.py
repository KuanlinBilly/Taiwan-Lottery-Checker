import requests
import pandas as pd

class LotteryChecker:
    def __init__(self, url):
        self.url = url
        self.table = pd.read_html(url)
        self.period_table = self.table[1]

    def get_name_list(self):
        name_list = []
        for i in range(10):
            a = self.period_table.iloc[i, :]
            period = str(a).split(' ')[11]
            name_list.append(str(period))
        return name_list

    def find_row(self, dataframe, value):
        result = dataframe[dataframe[0] == value]
        if not result.empty:
            return result.index[0]
        else:
            return None

    def get_winning_numbers(self, row):
        target = self.table[row + 2]
        winning_numbers = pd.DataFrame(target.iloc[3, 2:8])
        winning_numbers = winning_numbers.astype(int).iloc[:, 0]

        special_number = target.iloc[3, 8]
        special_number = int(special_number)

        return winning_numbers, special_number


class PrizeChecker:
    def __init__(self, user_input, winning_numbers, special_number):
        self.user_input = user_input
        self.winning_numbers = winning_numbers
        self.special_number = special_number

    def check_prize(self):
        user_input_set = set(self.user_input)
        winning_numbers_set = set(self.winning_numbers)
        common_numbers = user_input_set.intersection(winning_numbers_set)

        if len(common_numbers) == 6:
            return "頭獎"
        elif len(common_numbers) == 5 and self.special_number in user_input_set:
            return "貳獎"
        elif len(common_numbers) == 5:
            return "參獎"
        elif len(common_numbers) == 4 and self.special_number in user_input_set:
            return "肆獎"
        elif len(common_numbers) == 4:
            return "伍獎"
        elif len(common_numbers) == 3 and self.special_number in user_input_set:
            return "陸獎"
        elif len(common_numbers) == 2 and self.special_number in user_input_set:
            return "柒獎"
        elif len(common_numbers) == 3:
            return "普獎"
        else:
            return "NO"


class LotteryApp:
    def __init__(self, url):
        self.lottery_checker = LotteryChecker(url)

    def main(self):
        print('這是一個樂透對獎器！')
        period = eval(input("請輸入期別號: "))
        num = input("請輸入投注號碼的六個數字，以逗號分隔: ")

        period = str(period)
        num = num.split(',')

        name_list = self.lottery_checker.get_name_list()
        name_list = pd.DataFrame(name_list)

        row = self.lottery_checker.find_row(name_list, str(period))
        winning_numbers, special_number = self.lottery_checker.get_winning_numbers(row)

        user_input = pd.DataFrame(num)
        user_input = user_input.astype(int).iloc[:, 0]

        prize_checker = PrizeChecker(user_input, winning_numbers, special_number)
        prize = prize_checker.check_prize()
        print(f'查詢結果：{prize}')

if __name__ == "__main__":
    url = 'https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx'
    lottery_app = LotteryApp(url)
    lottery_app.main()
