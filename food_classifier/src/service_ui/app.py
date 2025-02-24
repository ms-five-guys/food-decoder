import gradio as gr
from components.create_interfaces import create_interfaces
from components.utils.customer_session import CustomerSession

# Create Gradio interfaces with session management
def create_demo():
    # Initialize session state
    session_state = gr.State(CustomerSession())
    
    # Create interfaces with session state
    customer_info_interface, nutritional_info_interface = create_interfaces(session_state)
    
    # Combine interfaces
    demo = gr.TabbedInterface(
        [customer_info_interface, nutritional_info_interface],
        ["고객 정보", "영양 정보"]
    )
    return demo

# Run server
if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )
