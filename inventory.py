# import tabulate to allow data to be viewed in table form in console.
from tabulate import tabulate


#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost
        '''
        Add the code to return the cost of the shoe in this method.
        '''

    def get_quantity(self):
        return self.quantity
        '''
        Add the code to return the quantity of the shoes.
        '''

    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"
        '''
        Add a code to returns a string representation of a class.
        '''



#==========Functions outside the class==============
'''
function below created to convert from object from shoe_list to string for manipulation in other functions.
'''
def shoe_obj_to_string():
    all_shoe_data = []
    # for each item in shoe_list __str__() is used to convert object to string, then split by "," into a list
    for sku in shoe_list:
        shoe_as_list = sku.__str__().split(",")
        # new empty list to store lines after stripping white space
        stripped_shoe_list = []
        for component in shoe_as_list:
            stripped_shoe_list.append(component.strip(" "))

        # each list for each object is added to all_shoe_data list.
        all_shoe_data.append(stripped_shoe_list)
    # return final list created above.
    return all_shoe_data

'''
function below created to update inventory.txt file.
'''
def update_inventory_file(all_current_shoe_data):
    # convert to string and write to file.
    all_shoe_string = []
    for item in all_current_shoe_data:
        line_str = f"\n{item[0]},{item[1]},{item[2]},{item[3]},{item[4]}"
        all_shoe_string.append(line_str)

    f_inventory = None
    try:
        # try to open inventory.txt for writing - will replace all data with new.
        f_inventory = open("inventory.txt", "w")

        # for loop to process each line and add to shoe_list
        f_inventory.write("Country,Code,Product,Cost,Quantity")
        for line in all_shoe_string:
            f_inventory.write(line)

    # if file not found, except results in error on screen to advise user.
    except FileNotFoundError:
        print("The inventory file cannot be found.")

    # finally used when inventory is no longer "None" to allow file to be closed after above extraction.
    finally:
        if f_inventory is not None:
            f_inventory.close()

'''
Function below defined to open inventory file - if file not found, results in error with use of Try/Except.
'''
def read_shoes_data():
    shoe_list_obj = []
    # new variable declated as value None (will be changed on successful opening of file.)
    f_inventory = None
    try:
        # try to open inventory.txt
        f_inventory = open("inventory.txt", "r")

        # for loop to process each line and add to shoe_list
        for line in f_inventory:
            # removal of "\n" at end of each line.
            replace_line = line.replace("\n", "")
            # lines then split by comma.
            split_line = replace_line.split(",")
            # if statement to skip first line - "country" is not a valid country and so should mean first line is always skipped
            if split_line[0] != "Country" and len(split_line) == 5: # also include len(split_line) == 5 to ensure lines with missing info ignored
                inventory_shoe = Shoe(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4])
                shoe_list_obj.append(inventory_shoe)

    # if file not found, except results in error on screen to advise user.
    except FileNotFoundError:
        print("The inventory file cannot be found.")

    # finally used when inventory is no longer "None" to allow file to be closed after above extraction.
    finally:
        if f_inventory is not None:
            f_inventory.close()
    return shoe_list_obj

'''
Function defined to allow new shoe details to be entered by the user and added to shoe_list as a Shoe object.
'''
def capture_shoes():
    # console header statement
    print("\n====================== Capture New Shoe Details ============================\n")
    # user asked to enter details of new shoe
    new_shoe_name = input("Please enter the name of the new shoe:\n")
    user_sku = input("Please enter the new SKU code:\nSKU ")
    new_sku = f"SKU{user_sku}"
    new_country = input("Please enter a country for the new shoe:\n")
    # while loop to ensure user enters integer for cost of shoe (assuming that cost will always be a whole number)
    while True:
        try:
            new_cost = int(input("Please enter the cost of the new shoe (local currency):\n"))
            break
        except ValueError:
            print("\nThat input is not a valid quantity. Please try again.\n")
    # while loop to ensure customer enters integer for quantity.
    while True:
        try:
            new_qty = int(input("Please enter the quantity for the new shoe:\n"))
            break
        except ValueError:
            print("\nThat input is not a valid quantity. Please try again.\n")

    # new Shoe object created and added to shoe_list
    new_shoe = Shoe(new_country, new_sku, new_shoe_name, new_cost, new_qty)
    shoe_list.append(new_shoe)
    
    # update of data using obj_to_string function which then allows inventory.txt to be updated as well with the new entry.
    update_shoe_data = shoe_obj_to_string()
    update_inventory_file(update_shoe_data)

    print("\n====================== New Shoe Added ============================\n")

'''
Function defined to get all shoe data stored as objects and print to console
'''
def view_all():
    # header text
    print("\n====================== View All Data ============================\n")
    # creation of empty list to be used to produce table.
    all_shoe_data = []
    # for each item in shoe_list __str__() is used to convert object to string, then split by "," into a list
    for sku in shoe_list:
        shoe_as_list = sku.__str__().split(",")
        # each list for each object is added to all_shoe_data list.
        all_shoe_data.append(shoe_as_list)

    print("Stock quanitity below includes stock on order.")
    # print all_shoe_data list as table using tabulate() and indicated header.
    print(tabulate(all_shoe_data, headers = ["Country", "Code", "Shoe", "Cost", "Quantity"]))

    # footer text.
    print("\n====================== View All data END ============================\n")

def check_max_min(max_or_min):
    # creation of empty list to be used to produce table.
    all_shoe_data = shoe_obj_to_string()
    
    # calculate len(all_shoe_data) for total product lines
    total_items = len(all_shoe_data)

    # print current stock before showing lines to reorder.
    print("\nCurrent Stock:\n")
    print(tabulate(all_shoe_data, headers = ["Country", "Code", "Shoe", "Cost", "Quantity"]))
    print("")

    # new variable with value of quantity for first product in inventory (converted to int for comparison)
    low_high_stock_check = int(all_shoe_data[0][4])
    # new list to add indexes of products if multiple lines need to be reordered/put on sale - starts with index zero included.
    low_high_stock_list = [0]
    # for range 0 - total items qty is extracted and converted to int for comparison against existing lowest quatity
    for i in range(0, (total_items)):
        if max_or_min == "low":
            # if lower then existing stock_check then values in stock_check replaced
            if int(all_shoe_data[i][4]) < low_high_stock_check:
                low_high_stock_check = int(all_shoe_data[i][4])
                # existing indexs in list replaced with new lowest qty index.
                low_high_stock_list = [i]
            # if values are equal = values are appended to list
            elif int(all_shoe_data[i][4]) == low_high_stock_check:
                low_high_stock_list.append(i)
        elif max_or_min == "high":
            # if higher then existing stock_check then values in stock_check replaced
            if int(all_shoe_data[i][4]) > low_high_stock_check:
                low_high_stock_check = int(all_shoe_data[i][4])
                # existing indexs in list replaced with new lowest qty index.
                low_high_stock_list = [i]
            # if values are equal = values are appended to list
            elif int(all_shoe_data[i][4]) == low_high_stock_check:
                low_high_stock_list.append(i)
    
    return_data = [all_shoe_data, low_high_stock_check, low_high_stock_list]
    return return_data

def re_stock():
    # restock header
    print("\n====================== Restock Shoe ============================\n")

    # call check_max_min() with input "low" to call data on lowest stock lines
    low_stock_data = check_max_min("low")
    # separate data into required lists
    all_shoe_data = low_stock_data[0]
    lowest_stock_check = low_stock_data[1]
    lowest_stock_list = low_stock_data[2]
    # reorder quantity arbitrarily set to 10 - can change here if needed.
    reorder_qty = 10

    # empty list to obtain data for items to be reordered and forloop of lowest_stock_list
    reorder_list = []
    for index in lowest_stock_list:
        # data appended to reorder_list
        reorder_list.append(all_shoe_data[index])
    if len(lowest_stock_list) > 1:
        print("\nLow Stock multiple lines:\n")
    else:
        print("\nLow stock item:\n")
    print(tabulate(reorder_list, headers = ["Country", "Code", "Shoe", "Cost", "Quantity"]))

    # while loop to ask user if they would like to reorder. loop to ensure only valid entry can be input by user.
    while True:
        # user input converted to lowercase.
        reorder_now = input(f"\nRestock Quanity: {reorder_qty} EA\nWould you like to restock the above product? Type \'Y\' or \'N\':\n").lower()
        if reorder_now == "y":
            for item in lowest_stock_list:
                # lowest quantity of item amended to increase by reorder quantity then break.
                all_shoe_data[item][4] = str(lowest_stock_check + reorder_qty)
            # call update_inventory_file() to update inventory.txt
            update_inventory_file(all_shoe_data)
            print("\nItem restock requested.\n")
            break
        # if no selected, break and message to advise not reordered to exit function
        elif reorder_now == "n":
            print("\nItem has not been re-ordered\n")
            break
        # else statent to catch invalid entry.
        else:
            print("\ninput not valid. Please try again.\n")
    print("\n====================== Restock Shoe END ============================\n")

'''
function to allow search of product by SKU code
'''
def search_shoe():
    print("\n====================== Search Shoe ============================\n")
    # obtain all shoe data using created function.
    all_shoe_data = shoe_obj_to_string()
    # create empty dictionary
    shoe_dictionary = {}
    # for each list in all_shoe_data use code data as key and assign whole list as value
    for item in all_shoe_data:
        shoe_dictionary[item[1]] = item
    # while loop for user search input.
    while True:
        # user requested to enter Code or "-1" to exit
        user_search = input("\nPlease enter the full SKU code to search or \'-1\' to exit:\n")
        # if exit break out of loop
        if user_search == "-1":
            break
        # else try/except statements
        else:
            try:
                # removal of whitespace in user input
                search_replace = user_search.replace(" ", "")
                # creation of empty list for tabulate
                search_list = []
                # search replace used as key to call dictionary value. which then appended to search_list for display.
                search_list.append(shoe_dictionary[search_replace])
                # spacer
                print("")
                # print table of search list - always only one line. then break.
                print(tabulate(search_list, headers = ["Country", "Code", "Shoe", "Cost", "Quantity"]))
                print("")
                break
            # except in case of keyerror, loop around for user entry again
            except KeyError:
                print("\nThat product code is not valid. Please try again.\n")
    
    print("\n====================== Search Shoe END ============================\n")

'''
This function will calculate the total value of each inventory item, and display as table
'''
def value_per_item():
    print("\n====================== Inventory Value ============================\n")

    # obtain all shoe data using created function.
    all_shoe_data = shoe_obj_to_string()
    # create empty variable to track total value of all stock.
    total_stock_value = 0
    # for loop through all_shoe_data to obtain cost and quantity (convert to float and integer)
    for item in all_shoe_data:
        cost = float(item[3])
        qty = int(item[4])
        # calculate value of each line
        value = cost * qty
        # value added to the total_stock_value variable
        total_stock_value += value
        # value formatted for readability and appended to each list for individual loop.
        item.append(f"{value:,.2f}")
    # all data included value printed to table
    print(tabulate(all_shoe_data, headers = ["Country", "Code", "Shoe", "Cost", "Quantity", "Inventory Value"]))
    # total inventory value printed.
    print(f"\nTotal Inventory Value across all lines (local currency):\n{total_stock_value:,.2f}\n")

    print("\n====================== Inventory Value END ============================\n")

def highest_qty():
    print("\n====================== Highest Stock ============================\n")

    # call check_max_min() with input "low" to call data on lowest stock lines
    high_stock_data = check_max_min("high")
    # separate data into required lists
    all_shoe_data = high_stock_data[0]
    highest_stock_check = high_stock_data[1]
    highest_stock_list = high_stock_data[2]

    # empty list to obtain data for items to be discounted and forloop of highest_stock_list
    discount_list = []
    for index in highest_stock_list:
        # data appended to discount list
        discount_list.append(all_shoe_data[index])
    
    # conditional statements to print statment to put shoe on sale - for single or multiple lines.
    if len(highest_stock_list) > 1:
        print("\nMultiple lines of highest stock to be put on sale:\n")
    else:
        print("\nHighest stock item to be put on sale:\n")
    print(tabulate(discount_list, headers = ["Country", "Code", "Shoe", "Cost", "Quantity"]))

    print("\n====================== Highest Stock END ============================\n")



#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
print("\n================= Welcome to Shoe Stock Inventory Manager =================\n")
# while loop to run until user selects exist, and in case of invalid entry.
while True:
    #=============Shoe list=========== Runs each loop to update with any changes to inventory.txt during use.
    '''
    The list will be used to store a list of objects of shoes.
    '''
    # call read_shoes_data to update object list each loop
    shoe_list = read_shoes_data()
    
    print("\n====================== Main Menu ======================\n")
    menu = input('''Select one of the following Options below:
n - Create New Inventory entry
is - View all inventory stock
s - Search inventory by SKU
rs - Restock lowest stock lines
h - View highest stock lines
iv - View inventory value
e - Exit
: ''').lower()

    # blank inputs within each statement to allow user entry before proceeding to main menu after action.
    if menu == 'n':
        capture_shoes()
        input("Press enter to proceed.")
    
    elif menu == "is":
        view_all()
        input("Press enter to proceed.")
    
    elif menu == "s":
        search_shoe()
        input("Press enter to proceed.")
    
    elif menu == "rs":
        re_stock()
        input("Press enter to proceed.")
    
    elif menu == "h":
        highest_qty()
        input("Press enter to proceed.")
    
    elif menu == "iv":
        value_per_item()
        input("Press enter to proceed.")
    
    elif menu == "e":
        print("\nThank you for using the inventory manager")
        print("\n====================== END ============================\n")
        break

    else:
        print("\nEntry not valid. Please try again.")
