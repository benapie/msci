import os

import Pyro4


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


front_end = Pyro4.Proxy(input('Front end URI\n> '))
restaurant_list = front_end.get_restaurant_list()
order_list = []

clear_terminal()
print('"""\n"""  What is your name?\n"""')
name = input('> ')

while True:
    clear_terminal()
    print('"""\n"""  Pick an action\n"""')
    print('1 : Make an order')
    print('2 : Look at orders')
    print('3 : Delete an order')
    action_choice = input('> ')

    clear_terminal()
    print('"""\n"""  Pick a restaurant\n"""')
    for restaurant_id in restaurant_list:
        print('{}: {}'.format(restaurant_id.ljust(2), restaurant_list[restaurant_id]['NAME']))

    restaurant_choice = input('> ')
    if restaurant_choice == 'q':
        continue

    clear_terminal()
    if action_choice == '1':
        print('"""\n"""  Choose your order\n"""')
        # finding the max length of food name for formatting
        max_length = len(restaurant_list[restaurant_choice]['MENU']['1']['NAME'])
        for food_id in restaurant_list[restaurant_choice]['MENU']:
            if len(restaurant_list[restaurant_choice]['MENU'][food_id]['NAME']) > max_length:
                max_length = len(restaurant_list[restaurant_choice]['MENU'][food_id]['NAME'])
        for food_id in restaurant_list[restaurant_choice]['MENU']:
            print('{}: {} ({})'.format(food_id.ljust(2),
                                       restaurant_list[restaurant_choice]['MENU'][food_id]['NAME'].ljust(max_length),
                                       restaurant_list[restaurant_choice]['MENU'][food_id]['PRICE']))
        food_choice = input('> ')
        order_list = []
        while food_choice != '':
            order_list.append(food_choice)
            food_choice = input('> ')

        clear_terminal()
        print('"""\n"""  Enter your postcode\n"""')
        postcode = input('> ')

        res = front_end.post_order(name, postcode, restaurant_choice, order_list)
        clear_terminal()
        if res['STATUS'] == '200':
            clear_terminal()
            print('"""\n"""  Confirmation\n"""')
            total = 0
            for food_id in order_list:
                total += restaurant_list[restaurant_choice]['MENU'][food_id]['PRICE']
            print('Order total: {}\n'.format(total))
        else:
            print('"""\n"""  Error\n"""')
            print(res['MESSAGE'])
        input('Press enter to continue')
    elif action_choice == '2':
        order_list = front_end.get_restaurant_order_list(restaurant_choice)
        clear_terminal()
        print('"""\n"""  Orders for {}\n"""'.format(restaurant_list[restaurant_choice]['NAME']))
        if len(order_list) == 0:
            print("No orders to show\n")
        else:
            for order in order_list:
                print('ID {}'.format(order['ID']))
                print('       Name: {}'.format(order['NAME']))
                print('  Longitude: {}'.format(order['LONGITUDE']))
                print('   Latitute: {}'.format(order['LATITUDE']))
                print('      Order: {}\n'.format(order['ORDER']))
        print('Press enter to continue')
        input()
    elif action_choice == '3':
        order_list = front_end.get_restaurant_order_list(restaurant_choice)
        clear_terminal()
        print('"""\n"""  Choose the order to delete from {}\n"""'.format(restaurant_list[restaurant_choice]['NAME']))
        if len(order_list) == 0:
            print("No orders to show\n")
        else:
            for order in order_list:
                print('ID {}'.format(order['ID']))
                print('       Name: {}'.format(order['NAME']))
                print('  Longitude: {}'.format(order['LONGITUDE']))
                print('   Latitute: {}'.format(order['LATITUDE']))
                print('      Order: {}\n'.format(order['ORDER']))
        order_choice = input('> ')
        res = front_end.delete_order(order_choice)
        if res['STATUS'] != '200':
            pass
        else:
            clear_terminal()
            print('"""\n"""  Confirmation\n"""')
            print('Order {} deleted\n'.format(order_choice))
            input('Press enter to continue')
