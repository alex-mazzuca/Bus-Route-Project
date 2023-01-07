#-----------------------
# Name: Alex Mazzuca
# Program: projectAM.py
#-----------------------

from graphics import *
import pickle
import sys
from math import radians, sin, cos, sqrt, asin

# Purpose: The purpose of the main() function is to initiate the program by 
#          calling upon the appropriate functions desired by the user through
#          a command prompt. In terms of commands the program will allow the user
#          to load three ETS files(only trips.txt, shapes.txt and stops.txt) into a python
#          data structure(dictionary). The user can then access these data structures.
#          The user will also be able to pickle the three data strutcures(dictionaries)
#          and load them later in order to use the data for the graphics window.
#          A graphics window can be loaded in order to plot the bus routes and stops.
# Parameters: None
# Return: Returns nothing as a way of exiting the program.
def main():
    command_input = load_info()
    shape_IDs_dict = {}
    shapes_dict = {}
    stops_dict = {}
    dict_tuple = ()
    while command_input != "0":
        if command_input == "1":
            shape_IDs_dict = load_shape_IDs(shape_IDs_dict)
        elif command_input == "2":
            shapes_dict = load_shapes(shapes_dict)
            dict_tuple = (shape_IDs_dict, shapes_dict)
        elif command_input == "3":
            stops_dict = load_stops(stops_dict)
        elif command_input == "4" and shape_IDs_dict != {}:
            print_shape_IDs(shape_IDs_dict)
        elif command_input == "5" and shapes_dict != {}:
            print_points(shapes_dict)
        elif command_input == "6" and stops_dict != {}:
            print_stops(stops_dict)
        elif command_input == "7":
            save_pickle(shape_IDs_dict, shapes_dict, stops_dict)
        elif command_input == "8":
            dict_tuple = load_pickle()
            if dict_tuple != ():
                shape_IDs_dict, shapes_dict, stops_dict = dict_tuple
        elif command_input == "9" and dict_tuple != ():
            load_graph_window(dict_tuple)
        command_input = load_info()
    return

# Purpose: Will display an info box to inform the user the types of commands
#          that can be inputed into the command prompt.
# Parameters: None
# Return: command_input - A string character the user inputs as a desired command.
def load_info():
    print()
    print("Edmonton Transit System".center(32, " "))
    print("""---------------------------------
(1) Load shape IDs form GTFS file
(2) Load shapes from GTFS file
(3) Load stops from GTFS file
        
(4) Print shape IDs for a route
(5) Print point for a shape ID
(6) Print stops for a location

(7) Save shapes, shape IDs, and stops in a pickle
(8) Load shapes, shape IDs, and stops from a pickle

(9) Display interactive map
        
(0) Quit""")
    command_input = input("\nEnter command: ")
    while command_input not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        command_input = input("\nEnter command: ")
    return command_input

# Purpose: This function will ask the user for the name of a file to be opened
#          that conatins bus route numbers with their shapeIDs. The function will
#          then sort the bus route numbers and shapeIDs into a dictionary.
# Parameters: shape_IDs_dict - an empty dictionary
# Return: shape_IDs_dict - Returns a dictionary that contains the bus route
#         numbers as keys with their corresponding list of shapeIDs as values.
#         Will return nothing if no file is found or an incorrect file is chosen.
def load_shape_IDs(shape_IDs_dict):
    shape_IDs_dict = {}
    filename = input("\nEnter a file name [data/trips.txt]: ")
    if filename == "":
        filename = "data/trips.txt"
    try:
        file = open(filename, "r")
    except:
        print("\n\t** File Not Found **")
        return
    trips_list = file.readlines()
    file.close()
    for string in trips_list[1:]:
        string = string.split(",")
        if len(string) != 7:
            print("\n\t** Incorrect File! **")
            return
        if string[0] not in shape_IDs_dict:
            shape_IDs_dict[string[0]] = []
        shape_IDs_dict[string[0]].append(string[6].strip("\n"))
    for bus_number in shape_IDs_dict:
        shape_IDs_dict[bus_number] = set(shape_IDs_dict[bus_number])            
    return shape_IDs_dict

# Purpose: This function will ask the user for the name of a file that contains
#          the shapeIDs with their coordinates. The function will then sort the 
#          shapeIDs and their coordinates into a dictionary.
# Parameters: shapes_dict - an empty dictionary
# Return: shapes_dict - A dictionary of shapeIDs as keys with their
#         corresponding list of tupled coordinates as values.
#         Will return nothing if no file is found or an incorrect file is chosen.
def load_shapes(shapes_dict):
    shapes_dict = {}
    filename = input("\nEnter a file name [data/shapes.txt]: ")
    if filename == "":
            filename = "data/shapes.txt"
    try:
        file = open(filename, "r")
    except:
        print("\n\t** File Not Found **")
        return
    shapes_list = file.readlines()
    file.close()
    for string in shapes_list[1:]:
        string = string.split(",")
        if len(string) != 4:
            print("\n\t** Incorrect File! **")
            return
        if string[0] not in shapes_dict:
            shapes_dict[string[0]] = []
        temp_tuple =  float(string[1]), float(string[2])
        shapes_dict[string[0]].append(temp_tuple) 
    return shapes_dict

# Purpose: This function will ask the user for a desired route. Based on that 
#          route the function will print its corresponding shapeIDs. 
# Parameters: shape_IDs_dict - dictionary of bus route numbers with their coorisponding shape_IDs 
# Return: Will return nothing if a route is not found.
def print_shape_IDs(shape_IDs_dict):
    route_number = input("\nRoute? ")
    print("\nShape IDs for ", route_number, ":", sep = "")
    if route_number not in shape_IDs_dict:
        print("\t** NOT FOUND **")
        return
    for ids in shape_IDs_dict[route_number]:
        print("\t", ids)
           
# Purpose: This fuction will ask the user for a desired Shape ID. The function
#          will then print the coorisponding tupled coordinates.
# Parameters: shapes_dict - dictionary that contains shapeIDs with its corrisponding
#             list of tupled coordinates.
# Return: Will return nothing if shape is is not found.
def print_points(shapes_dict):
    shape_ID = input("\nShape ID? ")
    print("\nShape for ", shape_ID, ":", sep = "")
    if shape_ID not in shapes_dict:
        print("\t** NOT FOUND **")
        return
    for coordinates in shapes_dict[shape_ID]:
        print("\t", coordinates)

# Purpose: This function will save shape_IDs_dict, shapes_dict and stops_dict as a tuple
#          into a pickled file.
# Parameters: shape_IDs_dict - dictionary of bus route numbers with their corresponding list of shape_IDs
#             shapes_dict - A dictionary of shapeIDs as keys with their corresponding 
#             list of tupled coordinates as values.
#             stops_dict - a dictionary with tupled coordinates as the keys and a list
#             of lists that contain the stops info and the stop number as values
# Return: None
def save_pickle(shape_IDs_dict, shapes_dict, stops_dict):
    dict_tuple = shape_IDs_dict, shapes_dict, stops_dict
    filename = input("\nEnter a file name [etsdata.p]: ")
    if filename == "":
        filename = "etsdata.p"
    file = open(filename, "wb")
    pickle.dump(dict_tuple, file)
    file.close()

# Purpose: This function will load a selected pickled file. The pickled file
#          should load the tupled dictionaries (shape_IDs_dict, shapes_dict and stops_dict).
# Parameters: None
# Return: dict_tuple - tupled dictionaries (shape_IDs_dict, shapes_dict and stops_dict)
#         Will return empty tuple if file is not found.
def load_pickle():
    filename = input("\nEnter a file name [etsdata.p]: ")
    if filename == "":
        filename = "etsdata.p"
    try:
        file = open(filename, "rb")
        dict_tuple = pickle.load(file)
    except:
        print("\t** NOT FOUND **")
        return ()
    file.close()
    return dict_tuple

# Purpose: This function will load a graphics window that displays a map
#          of Edmonton. In the graphics window the user will be able to 
#          type in a bus route number and then click "plot" in order to
#          display the route on the map. Only the shape with the most points
#          will be displayed as a route. The user can also click on the map in order to
#          display the lat/lon coordinates and pixel coordinates.
# Parameters: dict_tuple - tupled dictionaries (shape_IDs_dict and shapes_dict)
# Return: Returns when window is closed or an incorrect pickle was loaded.
def load_graph_window(dict_tuple):
    win = GraphWin("Edmonton Transit System", 630, 768)
    image_obj = Image(Point(win.getWidth() // 2, win.getHeight() // 2), "background.gif")
    image_obj.draw(win)
    entry_obj = draw_entry_box(win)
    draw_plot_box(win)
    win.setCoords(-113.7138, 53.39576, -113.2714,  53.71605)
    try:
        shape_IDs_dict, shapes_dict, stops_dict = dict_tuple
    except:
        print("\tIncorrect pickle loaded")
        win.close()
        return
    interact_map(win, entry_obj, shape_IDs_dict, shapes_dict, stops_dict)
    return

# Purpose: This function will display the entry box on the graphics window in 
#          order to allow the user to type in a bus route number.
# Parameters: win - the graphics window
# Return: entry_obj - the entry object entered by the user (bus route number)    
def draw_entry_box(win):
    entry_obj = Entry(Point(60, 22), 10)
    entry_obj.setSize(15)
    entry_obj.draw(win)
    return entry_obj

# Purpose: This function will display the "plot" box on the graphics window.
# Parameters: win - the graphics window
# Return: None
def draw_plot_box(win):
    rect = Rectangle(Point(120, 10), Point(220, 37))
    rect.setFill("white")
    rect.draw(win)
    text = Text(Point(170, 24), "Plot")
    text.draw(win)

# Purpose: This function allows the user to interact with the graphics window.
#          Clicking on the map of Edmonton will print the coordinates of the click
#          and the five nearest stops around the mouse click. The stops will be
#          represented by black dots. The user may also plot a bus route by entering
#          a bus number into the input box and clicking on the "plot" box.
# Parameters: win - the graphics window
#             entry_obj - the entry object entered by the user (bus route number) 
#             shape_IDs_dict - dictionary of bus route numbers with their corresponding list of shape_IDs
#             shapes_dict - A dictionary of shapeIDs as keys with their corresponding 
#             list of tupled coordinates as values.
#             stops_dict - a dictionary with tupled coordinates as the keys and a list
#         of lists that contain the stops info and the stop number as values
# Return: Will return nothing if window is closed.
def interact_map(win, entry_obj, shape_IDs_dict, shapes_dict, stops_dict):
    while True:
        try:
            mouse = win.getMouse()
        except:
            return
        pixel = win.toScreen(mouse.x, mouse.y)
        if pixel[0] < 120 or pixel[0] > 220 or pixel[1] < 10 or pixel[1] > 37:
            pixel = coordinates_print(win, mouse, pixel)
            display_stops(win, stops_dict, mouse)
        elif pixel[0] >= 120 and pixel[0] <= 220 and pixel[1] >= 10 and pixel[1] <= 37:
            draw_route(win, entry_obj, shapes_dict, shape_IDs_dict)

# Purpose: This function will plot lines on the graphics window to indicate the
#          desired bus route from the user. The function will loop through 
#          shape_IDs_dict in order to find the shapeIDs of the desired bus route 
#          number. The shapeID in shapes_dict with the most coordinates will be 
#          plotted on the graph as a route. 
# Parameters: win - the graphics window
#             entry_obj - the entry object entered by the user (bus route number) 
#             shape_IDs_dict - dictionary of bus route numbers with their corresponding list of shape_IDs
#             shapes_dict - A dictionary of shapeIDs as keys with their corresponding 
#             list of tupled coordinates as values.
# Return: Will return nothing if the user does not click anything on the window
def draw_route(win, entry_obj, shapes_dict, shape_IDs_dict):         
    bus_number = entry_obj.getText()      
    if (bus_number in shape_IDs_dict):
        longest_ID = list(shape_IDs_dict[bus_number])[0]
        for shape_ID in shape_IDs_dict[bus_number]:
            if len(shapes_dict[shape_ID]) > len(shapes_dict[longest_ID]):
                longest_ID = shape_ID
        for i in range(len(shapes_dict[longest_ID]) - 1):
            line = Line(Point(shapes_dict[longest_ID][i][1], shapes_dict[longest_ID][i][0]), 
                        Point(shapes_dict[longest_ID][i + 1][1], shapes_dict[longest_ID][i + 1][0],))
            if win.isOpen():
                line.setFill("gray50")
                line.setWidth(3)
                line.draw(win)

# Purpose: This function wait for a desired click from the user. If the user 
#          clicks on the graphics window (map area) the lat/lon coordinates and 
#          the pixel coordinates will be printed out. Clicking on the "plot" box 
#          will not print coordinates.
# Parameters: win - the graphics window
#             mouse - point object of a users mouse click
#             pixel - win.toScreen coordintes of the mouse click
# Return: None 
def coordinates_print(win, mouse, pixel):
        print("\nGeographic (lat, lon):", (mouse.y, mouse.x), 
              "\nPixel (x, y):", pixel)
        sys.stdout.flush()  

# Purpose: This function will load the bus stops into a dictionary from the
#          "stops.txt" file. The coordinates of the bus stops will serve as
#          keys for the dictionary and will be in a tupled format. The values will
#          contain a list of lists that contain the stops info and the stop number.
# Parameters: stops_dict - an empty dictionary
# Return: stops_dict - a dictionary with tupled coordinates as the keys and a list
#         of lists that contain the stops info and the stop number as values
#         Will return nothing if wrong file was inputted or file was not found.
def load_stops(stops_dict):
    stops_dict = {}
    filename = input("\nEnter a file name [data/stops.txt]: ")
    if filename == "":
        filename = "data/stops.txt"
    try:
        file = open(filename, "r")
    except:
        print("\n\t** File Not Found **")
        return
    stops_list = file.readlines()
    file.close()
    for string in stops_list[1:]:
        string = string.split(",")
        if len(string) != 10:
            print("\n\t** Incorrect File! **")
            return
        temp_coords_tuple = float(string[4][2:]), float(string[5])
        if temp_coords_tuple not in stops_dict:
            stops_dict[temp_coords_tuple] = []
        stops_dict[temp_coords_tuple].append([string[0], string[2]])
    return stops_dict

# Purpose: This function will ask the user for coordinates(lat, lon) to a bus stop
#          and then will print out the bus stop information and bus stop number.         
# Parameters: stops_dict - a dictionary with tupled coordinates as the keys and a list
#         of lists that contain the stops info and the stop number as values
# Return: Will return nothing if coordinates were not found within the dictionary
#         or no coordinates were inputted.
def print_stops(stops_dict):
    coords_string = input("Location as 'lat,lon'? ")
    try:
        coords_tuple = float(coords_string[1:10]), float(coords_string[12:23])
    except:
        print("\t** NOT FOUND **")
        return        
    print("\nStops for ", coords_string, ":", sep = "")
    if coords_tuple not in stops_dict:
        print("\t** NOT FOUND **")
        return
    for stop_info in stops_dict[coords_tuple]:
        for i in range(len(stop_info) - 1):
            print("\t", [stop_info][i][0], "  ", [stop_info][i][1].strip('"'), end = "")
    print("")

# Purpose: This function will display the closest five stops to the user's click
#          on the map. The point will be displayed on the map through five black 
#          dots and the stops coordinates, distance, and info will be printed out.
# Parameters: win - graphics window
#             stops_dict - a dictionary with tupled coordinates as the keys and a list
#             of lists that contain the stops info and the stop number as values
#             mouse - point object of a users mouse click
# Return: None
def display_stops(win, stops_dict, mouse):
    print("\nNearest stops: \n\tDistance    Stop    Description")          
    lowest_dict = determine_5_lowest(mouse, stops_dict)
    for dist_key in lowest_dict:
        plot_stops(win, lowest_dict[dist_key][0])
        print(" " * (6 - len(str(dist_key)) + 9), dist_key, 
              "  ", lowest_dict[dist_key][1],
              " " * (6 - len(lowest_dict[dist_key][1])), 
              lowest_dict[dist_key][2].strip('"'))
    sys.stdout.flush()

# Purpose: This function will determine the five lowest distances between the
#          users mouse click and the stops within stops_dict. This function will
#          call upon the haversine function to determine the disatnces between
#          the points. The five lowest distances will be placed into a dictionary
#          with the stop infomration placed into a tuple as values.
# Parameters: mouse - point object of a users mouse click
#             stops_dict - a dictionary with tupled coordinates as the keys and a list
#             of lists that contain the stops info and the stop number as values
# Return: lowest_dict - a dictionary of the five lowest distances as keys with their
#         corresponding bus stop info placed in a tuple as values
def determine_5_lowest(mouse, stops_dict):
    lowest_dict = {}
    for coords in stops_dict:
        dist = haversine(mouse.y, mouse.x, coords[0], coords[1])
        dist = round((dist) * 1000, 1)
        if len(lowest_dict) < 5:
            lowest_dict[dist] = (coords, stops_dict[coords][0][0], stops_dict[coords][0][1])
        else:
            highest_dist = 0
            for dist_key in lowest_dict:
                if dist_key > highest_dist:
                    highest_dist = dist_key
            if dist < highest_dist:
                del lowest_dict[highest_dist]
                lowest_dict[dist] = (coords, stops_dict[coords][0][0], stops_dict[coords][0][1])
    return lowest_dict

# Purpose: This function will plot the bus stop on the graphics map.
# Parameters: win - the graphics window
#             coords - tuple of the bus stop coordinates
# Return: None         
def plot_stops(win, coords):
    circle = Circle(Point(coords[1], coords[0]), .0001)
    circle.setFill("black")
    circle.draw(win)

# Source for the following function:
# URL: https://rosettacode.org/wiki/Haversine_formula
# Purpose: This function will determine the distance between two points on a map.
# Parameters: lat1 - latitude of first point
#             lon1 - longitude of first point
#             lat2 - latitude of second point
#             lon2 - longitude of second point
# Return: R * c - distance in km
def haversine(lat1, lon1, lat2, lon2):
 
    R = 6372.8 # Earth radius in kilometers
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
 
    return R * c
#------------------------------------------------------------