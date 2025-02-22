import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from interfaces.customer_interface import create_customer_interface
from interfaces.nutrition_interface import create_nutrition_interface

def create_interfaces():
    """Create all interfaces"""
    customer_info_interface = create_customer_interface()
    nutritional_info_interface = create_nutrition_interface()
    return customer_info_interface, nutritional_info_interface 