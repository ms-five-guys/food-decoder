import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from interfaces.customer_interface import create_customer_interface
from interfaces.nutrition_interface import create_nutrition_interface

def create_interfaces(session_state):
    """
    Create all interfaces with session management
    """
    customer_info_interface = create_customer_interface(session_state)
    nutritional_info_interface = create_nutrition_interface(session_state)
    return customer_info_interface, nutritional_info_interface 