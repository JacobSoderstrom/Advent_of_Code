a_lst = []          # Start with empty list
while True:
    a_str = input('Enter item (empty str to exit): ')
    if not a_str:   # Exit on empty string.
        break
    a_lst.append(a_str)
