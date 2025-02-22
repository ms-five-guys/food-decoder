import os
import sys
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from utils.customer_processing import CustomerProcessor

# Initialize processor
customer_processor = CustomerProcessor()

def get_customer_details(customer_code, guardian_code):
    """Get customer details and create visualization"""
    # 입력값 검증
    if not customer_code or not guardian_code:
        gr.Warning("고객 코드 또는 보호자 코드를 확인해주세요.")
        return None, "", None, None
    
    photo, info_text, nutrition_summary, plot = customer_processor.get_customer_info(customer_code, guardian_code)
    
    if photo is None:  # 에러가 발생한 경우
        gr.Error(info_text)  # 에러 메시지를 팝업으로 표시
        return None, "", None, None
    
    return photo, info_text, nutrition_summary, plot

def create_customer_interface():
    """Create customer information interface"""
    customer_info_interface = gr.Interface(
        fn=get_customer_details,
        inputs=[
            gr.Textbox(label="고객 코드"),
            gr.Textbox(label="보호자 코드", type="password")
        ],
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