import gradio as gr
from components.interfaces.customer_interface import create_customer_interface
from components.interfaces.nutrition_interface import create_nutrition_interface
from components.utils.customer_session import CustomerSession

def create_demo():
    """Create Gradio demo with session management"""
    with gr.Blocks() as demo:
        # Initialize session state
        session_state = gr.State(CustomerSession())
        
        # Create tab buttons
        with gr.Tabs() as tabs:
            with gr.Tab("고객 정보"):
                customer_interface = create_customer_interface(session_state)
            with gr.Tab("영양 정보"):
                nutrition_interface = create_nutrition_interface(session_state)
    
    return demo

# Run server
if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )
