# dictionary_symbols.py - Python program to manage CSV file which holds positions and whether orders were placed
# 4/4/2022
# Meshal Albaiz

import csv # CSV functions
from symbols import symbol_list # import ticker list


field_names = ['symbol', 'held'] # field names of CSV file

def reset_positions(): # function to reset all positions if profile is wiped
    positions = [] # create empty list of dictionaries
    for symb in symbol_list:
        dict = {'symbol': symb, 'held': "False"} # create dictionary for each ticker
        positions.append(dict) # append it to list

    with open('positions.csv', 'w') as csvfile: # save list of dictionaries to CSV file
        writer = csv.DictWriter(csvfile, fieldnames = field_names, lineterminator='\n')
        writer.writeheader()
        writer.writerows(positions)

def update_position(symbol, held): # function to update position in CSV file
    positions = get_all_positions() # get all positions from CSV file

    for stock in positions: # for each stock in positions
        if stock['symbol'] == symbol: # if stock is found then update position
            stock['held'] = held


    with open('positions.csv', 'w') as csvfile: # save updated list to CSV file
        writer = csv.DictWriter(csvfile, fieldnames = field_names, lineterminator='\n')
        writer.writeheader()
        writer.writerows(positions)

def get_position_csv(symbol): # get specific position from CSV
    firstline = True # boolean to skip first line in CSV file = header
    loaded_positions = [] # create empty list to load positions onto
    the_stock = {} # create empty position to load stock position onto
    with open('positions.csv', mode='r') as infile: # load positions
        reader = csv.reader(infile)
        for line in reader:
            if firstline:
                firstline = False
                continue
            dict = {'symbol': line[0], 'held': line[1]}
            loaded_positions.append(dict)
    for stock in loaded_positions: # find specific stock
        if stock['symbol'] == symbol:
            the_stock = stock # get stock information
    return the_stock # return stock information

def get_all_positions(): # get all positions from CSV file
    firstline = True # boolean to skip first line in CSV file = header
    loaded_positions = [] # create empty list to load positions onto
    with open('positions.csv', mode='r') as infile: # load positions
        reader = csv.reader(infile)
        for line in reader:
            if firstline:
                firstline = False
                continue
            dict = {'symbol': line[0], 'held': line[1]}
            loaded_positions.append(dict)
    return loaded_positions # return list of positions
