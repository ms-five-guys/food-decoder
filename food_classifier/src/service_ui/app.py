import gradio as gr
from components.create_interfaces import create_interfaces

# Create Gradio interfaces
customer_info_interface, nutritional_info_interface = create_interfaces()

# Combine interfaces
demo = gr.TabbedInterface(
    [customer_info_interface, nutritional_info_interface],
    ["Customer Info", "Nutritional Info"]
)

# Run server
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )
