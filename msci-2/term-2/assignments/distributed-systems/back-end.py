import random
import uuid

import Pyro4

ns = Pyro4.locateNS()


@Pyro4.expose
class BackEnd(object):
    def __init__(self):
        self.replica_id = uuid.uuid4()
        self.order_list = []
        self.is_backup = True
        self.restaurant_data = {
            '1': {
                'NAME': 'Fifty Six',
                'MENU': {
                    '1': {
                        'NAME': 'Pork Vermicelli',
                        'PRICE': 10.00
                    },
                    '2': {
                        'NAME': 'Not Hotpot',
                        'PRICE': 7.00
                    },
                    '3': {
                        'NAME': 'Pig Intestine Soup',
                        'PRICE': 8.00
                    },
                    '4': {
                        'NAME': 'Just a Pork Bone',
                        'PRICE': 15.00
                    }
                },
                'ORDERS': []
            },
            '2': {
                'NAME': 'Ben and Elliott\'s',
                'MENU': {
                    '1': {
                        'NAME': 'Milky Egg',
                        'PRICE': 0.01
                    },
                    '2': {
                        'NAME': 'Coffee',
                        'PRICE': 10000
                    },
                    '3': {
                        'NAME': 'Chilli with Baked Beans',
                        'PRICE': 5.00
                    }
                },
                'ORDERS': []
            },
            '3': {
                'NAME': 'Callum\'s Seductive Date Night Location',
                'MENU': {
                    '1': {
                        'NAME': 'Sunbites',
                        'PRICE': 27.00
                    }
                },
                'ORDERS': []
            }
        }

    def get_restaurant_list(self):
        """
        Returns a list of the restaurants, _without_ orders.
        """
        restaurant_list = {}
        for restaurant_id in self.restaurant_data:
            restaurant_list[restaurant_id] = {}
            restaurant_list[restaurant_id]['NAME'] = self.restaurant_data[restaurant_id]['NAME']
            restaurant_list[restaurant_id]['MENU'] = self.restaurant_data[restaurant_id]['MENU']
        return restaurant_list

    def get_restaurant_order_list(self, restaurant_id):
        """
        Returns a list of the orders for a restaurant.
        """
        return self.restaurant_data[restaurant_id]['ORDERS']

    @staticmethod
    def has_failed():
        return random.random() < 0.1

    def delete_order(self, order_id):
        for restaurant_id in self.restaurant_data:
            for i in range(0, len(self.restaurant_data[restaurant_id]['ORDERS'])):
                if self.restaurant_data[restaurant_id]['ORDERS'][i]['ID'] == order_id:
                    self.restaurant_data[restaurant_id]['ORDERS'].pop(i)
                    return {'STATUS': '200'}
        return {'STATUS': '404', 'MESSAGE': 'Could not find order to delete.'}

    def verify_food_order(self, restaurant_id, food_order):
        """
        Verifies whether all the ids of a food order exists for a restaurant.
        """
        if restaurant_id not in self.restaurant_data:
            return {'STATUS': '404', 'MESSAGE': 'Restaurant ID not found.'}
        for food in food_order:
            if food not in self.restaurant_data[restaurant_id]['MENU']:
                return {'STATUS': '404', 'MESSAGE': 'Food ID not found.'}
        return {'STATUS': '200'}

    def is_order_done(self, order_id):
        """
        Will check whether an order has already been completed.
        """
        for restaurant_id in self.restaurant_data:
            if order_id in self.restaurant_data[restaurant_id]['ORDERS']:
                return True
        return False

    def process_order(self, order):
        """
        Add an order to the order list, then updates all replicas with the new state.
        """
        if self.is_order_done(order['ID']):
            return {'STATUS': '400', 'MESSAGE': 'Request has already been done.'}

        self.restaurant_data[order['RESTAURANT_ID']]['ORDERS'].append(order)

        self.update_replicas()

        return {'STATUS': '200', 'MESSAGE': 'Order posted successfully.'}

    def update_replicas(self):
        """
        Update the other replicas in the nameserver with state (restaurant_data).
        #todo also updates itself..
        """
        for replica_uri in ns.list():
            if replica_uri != 'Pyro.NameServer':
                proxy = Pyro4.Proxy(ns.list()[replica_uri])
                proxy.update_state(self.restaurant_data)

    def update_state(self, new_restaurant_data):
        """
        Function called by primary replica to update the state (restaurant_data).
        """
        self.restaurant_data = new_restaurant_data


daemon = Pyro4.Daemon()
O = BackEnd()
uri = daemon.register(O)
ns.register('replica.{}'.format(O.replica_id), uri)
print('Server Ready: Object uri =', uri)
daemon.requestLoop()
daemon.close()
