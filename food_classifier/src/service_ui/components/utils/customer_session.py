class CustomerSession:
    """Customer session management class"""
    
    def __init__(self):
        """Initialize customer session"""
        self._customer_id = None
        self._customer_info = None
    
    @property
    def customer_id(self):
        """Get current customer ID"""
        return self._customer_id
    
    @property
    def customer_info(self):
        """Get current customer info"""
        return self._customer_info
    
    def set_customer(self, customer_info):
        """
        Set customer information
        
        Args:
            customer_info (dict): Customer information including customer_id
        """
        if not customer_info or 'customer_id' not in customer_info:
            raise ValueError("Invalid customer information")
            
        self._customer_id = customer_info['customer_id']
        self._customer_info = customer_info
    
    def clear(self):
        """Clear current session"""
        self._customer_id = None
        self._customer_info = None
    
    def is_active(self):
        """Check if there is an active customer session"""
        return self._customer_id is not None 