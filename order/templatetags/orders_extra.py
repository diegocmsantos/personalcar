from django import template

register = template.Library()

def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, '')
    
def multiply(price, quant):
    "Multiply price and quant"
    print "price: " + str(price)
    print "quant: " + str(quant)
    return price * quant

register.filter('multiply', multiply)