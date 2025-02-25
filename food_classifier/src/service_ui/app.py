import gradio as gr
from interfaces.customer_page import create_customer_page
from interfaces.nutrition_page import create_nutrition_page
from utils.customer_session import CustomerSession

def create_demo():
    """Create Gradio demo with session management"""
    with gr.Blocks() as demo:
        # Initialize session state
        session_state = gr.State(CustomerSession())
        
        # Create tab buttons
        with gr.Tabs() as tabs:
            with gr.Tab("고객 정보"):
                customer_page = create_customer_page(session_state)
            with gr.Tab("영양 정보"):
                nutrition_page = create_nutrition_page(session_state)
    
    return demo

# Run server
if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )
