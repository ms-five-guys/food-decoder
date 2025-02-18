import gradio as gr
import cv2
import numpy as np

def process_image(image):
    """
    Process the captured image
    """
    if image is None:
        return "No image captured"
    
    # Add image processing logic here
    return image

# Create Gradio interface
demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(
        sources=["webcam"],
        type="numpy",
        label="Camera"
    ),
    outputs=gr.Image(type="numpy", label="Captured Image"),
    title="📱 Mobile Camera Capture",
    description="Take a photo using your smartphone camera",
    theme="default",
    css="""
        #component-0 { max-width: 500px; margin: 0 auto; }
        .gradio-container { max-width: 550px; margin: 0 auto; }
    """
)

# Run server
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,       # Specify port
        share=True              # Generate public URL
    )
