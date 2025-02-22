import os
import sys
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from utils.customer_processing import CustomerProcessor

# Initialize processor
customer_processor = CustomerProcessor()

def get_customer_details(customer_code):
    """Get customer details and create visualization"""
    # customer_processor.get_customer_info는 4개의 값을 반환함:
    # photo, customer_info_text, nutrition_summary, nutrition_plot
    photo, info_text, nutrition_summary, plot = customer_processor.get_customer_info(customer_code)
    
    if photo is None:  # 에러가 발생한 경우
        return None, info_text, None, None  # 에러 메시지는 info_text에 포함됨
    
    return photo, info_text, nutrition_summary, plot

def create_customer_interface():
    """Create customer information interface"""
    customer_info_interface = gr.Interface(
        fn=get_customer_details,
        inputs=gr.Textbox(label="고객 코드"),
        outputs=[
            gr.Image(label="고객 사진", width=300, height=300),
            gr.HTML(label="고객 상세 정보"),
            gr.HTML(label="최근 섭취 정보"),
            gr.Plot(label=" ")
        ],
        title="📱 고객 정보",
        description="고객 코드와 보호자 코드를 입력하여 고객의 상세 정보를 확인하세요.",
        theme="default"
    )
    return customer_info_interface 