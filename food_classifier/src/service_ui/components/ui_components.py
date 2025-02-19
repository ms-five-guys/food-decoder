import gradio as gr
from components.data_processing import get_customer_info, get_nutritional_info

def create_interfaces():
    customer_info_interface = gr.Interface(
        fn=get_customer_info,
        inputs=gr.Textbox(label="Customer Code"),
        outputs=[
            gr.Image(label="Customer Photo", width=300, height=300),  # Display customer photo
            gr.HTML(label="Customer Information"),  # Display customer information
            gr.HTML(label="Recent Nutrition Summary"),  # Display recent nutrition summary
            gr.Plot(label=" ")  # Display recent nutrition graph
        ],
        title="📱 Customer Information",
        description="Enter customer code to get customer information",
        theme="default"
    )

    nutritional_info_interface = gr.Interface(
        fn=get_nutritional_info,
        inputs=gr.Image(
            sources=["webcam"],
            type="numpy",
            label="Camera"
        ),
        outputs=gr.Textbox(label="Nutritional Information"),
        title="📱 Nutritional Information",
        description="Take a photo of food to get nutritional information",
        theme="default"
    )

    return customer_info_interface, nutritional_info_interface
