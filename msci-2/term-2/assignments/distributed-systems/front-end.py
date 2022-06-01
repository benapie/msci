import json

import Pyro4
import requests


def post_code_lookup(postcode):
    """
    Uses postcode.io web services to validate a postcode.
    :param postcode: a postcode, given as a string.
    :return: a dump of address info or an error (if there is an error).
    """
    r = requests.get('https://api.postcodes.io/postcodes/{}'.format(postcode))
    response = json.loads(r.text)
    if response['status'] == 200:
        return {'STATUS': '200', 'DATA': response['result']}
    elif response['status'] == 404:
        return {'STATUS': 404, 'MESSAGE': 'Invalid postcode.'}
    else:
        return {'STATUS': 400, 'MESSAGE': 'Error in checking postcode.'}


# The first URI is always the primary, the other two are backups.
# back_end_proxy_list = [input('backup uri 1 -> '), input('backup url 2 -> ')]
# front_end_proxy = Pyro4.Proxy(input('primary uri -> '))


@Pyro4.expose
class FrontEnd(object):
    def __init__(self):
        self.uri_list = [input('Replica 1 URI\n> '), input('Replica 2 URI\n> '), input('Replica 3 URI\n> ')]
        self.proxy_priority = [0, 1, 2]  # first entry of this list is the primary.
        self.process_id_counter = 0
        self.proxy_list = [Pyro4.Proxy(self.uri_list[0]), Pyro4.Proxy(self.uri_list[1]), Pyro4.Proxy(self.uri_list[2])]

    def elect_new_primary(self):
        self.proxy_list[self.proxy_priority[0]].make_backup()
        self.proxy_list[self.proxy_priority[-1]].make_primary()
        self.proxy_priority = [self.proxy_priority[-1]] + self.proxy_priority[0:-1]

    def get_order(self, order_id):
        response = self.proxy_list[self.proxy_priority[0]].get_order(order_id)
        return response

    def get_restaurant_order_list(self, restaurant_id):
        """
        Returns a list of the orders for a restaurant.
        """
        return self.proxy_list[self.proxy_priority[0]].get_restaurant_order_list(restaurant_id)

    def delete_order(self, order_id):
        """
        Given the ID of the request to post the order, will delete that order.
        """
        return self.proxy_list[self.proxy_priority[0]].delete_order(order_id)

    def ensure_primary(self):
        """
        Ensures that the primary server has not crashed.
        """
        while self.proxy_list[self.proxy_priority[0]].has_failed():
            self.elect_new_primary()
            print('Replica {} has crashed, replica {} now elected as primary.'.format(self.proxy_priority[1],
                                                                                      self.proxy_priority[0]))

    def get_restaurant_list(self):
        """
        Returns a list of the restaurant with menus.
        :return:
        """
        self.ensure_primary()
        return self.proxy_list[self.proxy_priority[0]].get_restaurant_list()

    def post_order(self, name, postcode, restaurant_id, food_order):
        """
        This function
          (i) checks the postcode via the web service postcodes.io;
         (ii) gets the longitude and latitude;
        (iii) if the primary replica crashes, will elect a new primary;
         (iv) verifies order data with the primary replica;
          (v) constructs and sends the request to the primary replica; then
         (vi) returns the response from the primary replica.
        """
        # (i), (ii)
        address = post_code_lookup(postcode)
        if address['STATUS'] != '200':
            return address
        address = address['DATA']

        # (iii)
        self.ensure_primary()

        # (iv)
        res = self.proxy_list[self.proxy_priority[0]].verify_food_order(restaurant_id, food_order)
        if res['STATUS'] != '200':
            return res

        # (v)
        order = {
            'ID': str(self.process_id_counter),
            'NAME': name,
            'LONGITUDE': address['longitude'],
            'LATITUDE': address['latitude'],
            'RESTAURANT_ID': restaurant_id,
            'ORDER': food_order
        }
        self.process_id_counter += 1

        # (vi)
        return self.proxy_list[self.proxy_priority[0]].process_order(order)


daemon = Pyro4.Daemon()
front_end = FrontEnd()
uri = daemon.register(front_end)

print("Server Ready: Object uri =", uri)
daemon.requestLoop()
