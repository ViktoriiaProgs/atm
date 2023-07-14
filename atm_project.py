'''ATM'''

from random import *
import requests
from bs4 import BeautifulSoup as Bs
from datetime import datetime


def print_menu():
    main_atm = {
        1: 'Withdraw money',
        2: 'Deposit money',
        3: 'Exchange rate',
        4: 'Change money',
        0: 'Exit'}
    print('\nMenu:')
    for key in main_atm.keys():
        print(key, '--', main_atm[key])
    option = int(input('\nSelect transaction: '))
    return option


# ---------------------------------------------------
class Files():
    def __init__(self):
        self.file_user = 'file_for_balance_user.txt'
        self.file_atm = 'file_for_balance_atm.txt'
        self.file_operation = 'file_for_all_operation.txt'
        self.file_currency = 'file_for_currency_user'

    def user_balance(self, arg):
        text = open(self.file_user, 'w')
        text.write(str(arg))
        text.close()

    def atm_balance(self, arg):
        text = open(self.file_atm, 'w')
        text.write(str(arg))
        text.close()

    def currency_balance(self, arg):
        text = open(self.file_currency, 'w')
        text.write(str(arg))
        text.close()

    def all_operations(self, operation):
        text = open(self.file_operation, 'a', encoding='utf-8')
        line_operation = {str(datetime.now()): operation}
        text.write(str(line_operation))
        text.write('\n')
        text.close()


# ---------------------------------------------

class ATM(Files):
    def __init__(self, balance_user, pin, *args):
        super().__init__()
        self.balance_user = balance_user
        self.system_balance = randint(2000, 10000)
        self.__pin = pin
        self.currency = args

    @property
    def method(self):
        return self.__pin

    def __call__(self, *args, **kwargs):
        pin_get = self.__pin
        kilk = 1
        while kilk < 4:
            pin_try = input(f'Please enter your PIN:\n'
                            f' (automatically generated {pin_get})\n')
            if int(pin_try) == pin_get:
                print('Welcome! PIN was entered correctly')
                return True
            else:
                if kilk < 3:
                    print(f'Attention! PIN code entered incorrectly!\n'
                          f'Please try again\n'
                          f'You have attempts left - {3 - kilk}\n')
                kilk += 1
        else:
            print('Attention! PIN code is blocked. Please contact the bank for assistance. ')
            return False

    # 3 attempts

    def withdraw(self):
        print(f'\n(*automatically generated balance*)\n'
              f' - ATM balance - {self.system_balance}uah\n'
              f' - Customer balance - {self.balance_user}uah\n')

        withdrawal_sum = int(float(input(f'  CASH WITHDRAWAL \nPlease enter the amount:\n')))

        if withdrawal_sum > self.balance_user:
            print(f'Insufficient funds.\nCurrent balance {self.balance_user}uah')
        elif withdrawal_sum > self.system_balance:
            print(f'Insufficient funds in the ATM.\n You can withdraw {self.system_balance}uah')
        else:
            print(f'CASH WITHDRAWAL ↓↓↓\n'
                  f'$$$$$$$$ {withdrawal_sum}uah $$$$$$$$$$')
            self.balance_user = self.balance_user - withdrawal_sum
            self.system_balance = self.system_balance - withdrawal_sum
            print(f'\nPlease take the cash\nAccount balance - {self.balance_user}uah')
            super().user_balance(self.balance_user)
            super().atm_balance(self.system_balance)
        # transaction record
        type_operation = 'Cash withdrawal'
        super().all_operations(type_operation)

    def deposit(self):
        print(f'(*automatically generated balance sheet*)\n'
              f' - ATM balance - {self.system_balance}\n'
              f' - Customer balance - {self.balance_user}\n')

        deposit_sum = int(input(f'  DEPOSIT MONEY \nPlease enter the amount:'))
        self.balance_user = self.balance_user + deposit_sum
        self.system_balance = self.system_balance + deposit_sum
        print(f'BALANCE IS REPLENISHED\nAvailable balance - {self.balance_user}uah')
        super().user_balance(self.balance_user)
        super().atm_balance(self.system_balance)
        # transaction record
        type_operation = 'Deposit of cash'
        super().all_operations(type_operation)

    @staticmethod
    def currency_rate():
        url = 'https://tables.finance.ua/ua/currency/official/-/1'
        response = requests.get(url)
        html = Bs(response.content, 'html.parser')
        value_currency = ['USD', 'EUR']
        dct_currency = {}
        for i in html.select('.curtable'):
            for el in [0, 1]:
                if i.select('.index')[el].text in value_currency:
                    dct_currency[i.select('.index')[el].text] = float(i.select('.value')[el].text)
        return dct_currency

    def output_currency_rate(self):  # p 3
        dct_currency = ATM.currency_rate()
        print('\nNBU exchange rate:')

        for key in dct_currency.keys():
            print(f'{key} : {dct_currency[key]}')
        # transaction record
        type_operation = 'Currency exchange rate information'
        super().all_operations(type_operation)

    def currency_convert(self):  # p 4
        dct_currency = ATM.currency_rate()
        dlr = round(self.balance_user / dct_currency['USD'], 2)
        eur = round(self.balance_user / dct_currency['EUR'], 2)
        dict_currency = {1: 'USD',
                         2: 'EUR'}
        print(f'The amount is available for conversion to foreign currency:\n'
              f'{self.balance_user}uah   =  {dlr}usd або {eur}eur\n')
        k = 0
        print('Currency exchange rate:')
        for key in dct_currency.keys():
            k += 1
            print(f'{k} - {key} : {dct_currency[key]}')
        currency_choice = int(input(f'Select a currency:\n'))

        convert_sum = float(input(f'Enter the AMOUNT in UAH that you want to exchange for {dict_currency[currency_choice]}:\n'))

        if convert_sum > self.balance_user:
            print(f'Insufficient funds in the account.\nCurrent balance  {self.balance_user}uah')

        else:
            if currency_choice == 1:
                self.currency = round(convert_sum / dct_currency[dict_currency[currency_choice]], 2)
                self.balance_user = round(
                    self.balance_user - self.currency * dct_currency[dict_currency[currency_choice]],
                    2)
            elif currency_choice == 2:
                self.currency = round(convert_sum / dct_currency[dict_currency[currency_choice]], 2)
                self.balance_user = round(
                    self.balance_user - self.currency * dct_currency[dict_currency[currency_choice]], 2)

            print(f'The operation is successfully completed.\n'
                  f'Available balance in UAH - {self.balance_user}uah\n'
                  f'Available balance in {dict_currency[currency_choice]} - {self.currency}{dict_currency[currency_choice]}')

        super().user_balance(self.balance_user)  # record UAH balance
        super().currency_balance(self.currency)  # recording the balance sheet currency
        # transaction record
        type_operation = 'Currency exchange'
        super().all_operations(type_operation)


# ================================

print('Welcome!')
balance_user_random = randint(1000, 2500)
pin_random = randint(1000, 9999)
user = ATM(balance_user_random, pin_random)

if user():
    user.user_balance(balance_user_random)
    while True:
        menu_item = print_menu()
        if menu_item == 1:
            user.withdraw()
        elif menu_item == 2:
            user.deposit()
        elif menu_item == 3:
            user.output_currency_rate()
        elif menu_item == 4:
            user.currency_convert()
        elif menu_item == 0:
            print('Goodbye!')
            exit()
        else:
            print('Option entered incorrectly. '
                  'Try again.')


# Create a program,
# that will simulate the operation of the ATM/terminal system.
# When creating an object, the amount of the user's balance and the access pin are passed as attributes.
#
# The pin code verification is called automatically when the object is created and takes three attempts.
# If the login is successful, the balance is automatically written to a separate text file +
# the balance of the system itself is stored in another file.
#
# The following actions are available to the user:
#
# 1. Withdraw funds.
#   In this case, the amount cannot exceed the available balance of the user and the system itself.
#   When withdrawing, the amount is automatically deducted from the user's and the system's balance.
#
# 2. Deposit funds.
#    In this case, the user's and the system's balance will be replenished by the corresponding amount.
#
# 3) Find out the current exchange rate.
#       Here, we use a request, and the rate itself is obtained from an arbitrary website.
#
# 4) Transfer a certain amount to an arbitrary currency.
#   Here, we also use a request for the current exchange rate.
#   After the operation, another attribute will be created for the user
#   (amount of funds in the specified currency),
#   the value of which will be stored in a new text file.
#
# 5.Each operation is recorded in a separate file in the form of a dictionary,
# where the key is time + date (datetime.now()),
# the value is the type of operation performed.

