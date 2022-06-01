# Client.py
import Pyro4

uri1 = input("What is the Pyro uri of the Add & Mult object? ").strip()
uri2 = input("What is the Pyro uri of the Avg & Max object? ").strip()
x = float(input("x? -> "))
y = float(input("y? -> "))
z = float(input("z? -> "))

Math1 = Pyro4.Proxy(uri1)      # get a Pyro proxy to the Hello object
Math2 = Pyro4.Proxy(uri2)

print("Add: ", Math1.Add(x,y,z))   # call remote method
print("Mul: ", Math1.Mul(x,y,z))   # call remote method
print("Avg: ", Math2.Avg(x,y,z))   # call remote method
print("Max: ", Math2.Max(x,y,z))   # call remote method
input()
