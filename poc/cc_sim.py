"""
Cookie Clicker Simulator
You should first implement the ClickerState class. This class will keep track of the state 
of the game during a simulation. This various fields in this class should roughly
 correspond to the local variables used in implementing the function greedy_boss
  in the Practice Activity. (Cookies correspond to money and upgrades to CPS correspond
   to bribes.) By encapsulating the game state in this class, the logic for running 
a simulation of the game will be greatly simplified. The ClickerState class must keep 
track of four things:

The total number of cookies produced throughout the entire game 
(this should be initialized to 0.0).
The current number of cookies you have (this should be initialized to 0.0).
The current time (in seconds) of the game (this should be initialized to 0.0).
The current CPS (this should be initialized to 1.0).
Note that you should use floats to keep track of all state properties. 
You will have fractional values for cookies and CPS throughout.

During a simulation, upgrades are only allowed at an integral number of seconds 
as required in Cookie Clicker. However, the CPS value is a floating point number. 
In addition to this information, your ClickerState class must also keep track of 
the history of the game. We will track the history as a list of tuples. Each tuple
in the list will contain 4 values: a time, an item that was bought at that time 
(or None), the cost of the item, and the total number of cookies produced by that 
time. This history list should therefore be initialized as [(0.0, None, 0.0, 0.0)]. 

BuildInfo class contains the following functions:

build_items: get a list of buildable items sorted by name
get_cost(item): get the current cost of an item
get_cps(item): get the current CPS of an item
update_item(item): update the cost of an item by the growth factor
clone: return clone of buildinfo
"""

#import matplotlib.pyplot as plt
import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cur_cookies = 0.0
        self._cur_time = 0.0
        self._cur_cps = 1.0
        self._item_name = None
        self._item_cost = 0.0
        self._history_list = [(self._cur_time, self._item_name, self._item_cost, self._total_cookies)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "total cookies: " + str(self._total_cookies) + "\n"\
        + "current cookies: " + str(self._cur_cookies) + "\n"\
        + "current time: " + str(self._cur_time) + "\n"\
        + "current cps:" + str(self._cur_cps) + "\n"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cur_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cur_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._cur_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies >= self._cur_cookies:
            return math.ceil((cookies-self._cur_cookies)/self._cur_cps)
        return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0:
          pass
        else:
          self._cur_cookies += (self._cur_cps * time)
          self._total_cookies += (self._cur_cps*time)
          self._cur_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._cur_cookies:
          pass
        else:
          self._cur_cps += additional_cps
          self._cur_cookies -= cost
          self._history_list.append((self._cur_time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    BuildInfo class contains the following functions:

    build_items: get a list of buildable items sorted by name
    get_cost(item): get the current cost of an item
    get_cps(item): get the current CPS of an item
    update_item(item): update the cost of an item by the growth factor
    clone: return clone of buildinfo
    """
    copied_build_info = build_info.clone()
    newgame = ClickerState()
    while duration >= 0:
        item = strategy(newgame.get_cookies(), newgame.get_cps(), newgame.get_history(), duration, copied_build_info)
        if item == None:
            break
        item_price = copied_build_info.get_cost(item)
        time_needed = newgame.time_until(item_price)
        if time_needed > duration:
            break
        # wait for time needed
        newgame.wait(time_needed)
        duration -= time_needed
        newgame.buy_item(item, item_price, copied_build_info.get_cps(item))
        copied_build_info.update_item(item) 
        
    newgame.wait(duration)
    #get time needed until purchase
    #break if time needed > duration
    # wait for time needed
    # buy item
    # update build info
    # wait remainder of duration
    return newgame


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    - iterate over item list and get cost of each.
    - select item with lowest cost, return that item
    """
    cheapest_item = None
    min_cost = float("inf")
    itemlist = build_info.build_items()
    for item in itemlist:
        if (build_info.get_cost(item) < min_cost and (cookies + time_left*cps) >= build_info.get_cost(item)):
            min_cost = build_info.get_cost(item)
            cheapest_item = item
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    - iterate over item list and get cost of each.
    - select item with highest cost, return that item
    """
    highest_item = None
    max_cost = float("-inf")
    itemlist = build_info.build_items()
    for item in itemlist:
        if (build_info.get_cost(item) > max_cost and (cookies + time_left*cps) >= build_info.get_cost(item)):
            max_cost = build_info.get_cost(item)
            highest_item = item
    return highest_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    Change cheapest to calculate best cost/cps ratio benefit.
    """
    best_item = None
    most_efficient = float("inf")
    itemlist = build_info.build_items()
    for item in itemlist:
        #generate value
        efficiency = build_info.get_cost(item)/build_info.get_cps(item)
        if (efficiency < most_efficient and (cookies + time_left*cps) > build_info.get_cost(item)):
            most_efficient = efficiency
            best_item = item
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
