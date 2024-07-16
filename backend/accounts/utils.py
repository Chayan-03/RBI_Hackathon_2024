# accounts/utils.py

import random
import string

def generate_random_card_number(length=16):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_account_number(length=12):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_ifsc_code(length=11):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_bank_name():
    return random.choice(['Bank of America', 'Chase Bank', 'Wells Fargo', 'Citi Bank', 'HSBC'])

def generate_random_pin(length=4):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_cvv():
    return random.randint(100, 999) 