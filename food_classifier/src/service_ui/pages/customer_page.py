import os
import sys
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from processors.customer_processing import CustomerProcessor

# Initialize processor
customer_processor = CustomerProcessor()

def get_customer_details(customer_code, guardian_code, session_state):
    """Get customer details and create visualization"""
    # 입력값 검증
    if not customer_code or not guardian_code:
        gr.Warning("고객 코드 또는 보호자 코드를 확인해주세요.")
        return None, "", None
    
    photo, info_text, plot = customer_processor.get_customer_info(
        customer_code, 
        guardian_code,
        session_state
    )
    
    if photo is None:
        gr.Error(info_text)
        return None, "", None
    
    return photo, info_text, plot

def create_customer_page(session_state):
    """Create customer information page"""
    with gr.Blocks() as customer_page:
        gr.Markdown("## 👨‍⚕️ 고객 정보")
        
        with gr.Row():
            customer_code = gr.Textbox(label="고객 코드")
            guardian_code = gr.Textbox(label="보호자 코드", type="password")
            submit_btn = gr.Button("조회", variant="primary")
            
        with gr.Column():
            customer_photo = gr.Image(label="고객 사진")
            customer_info = gr.HTML()
            nutrition_history = gr.Plot()
            
        def get_customer_details(code, guardian, state):
            """Get customer details and create visualization"""
            # 입력값 검증
            if not code or not guardian:
                gr.Warning("고객 코드 또는 보호자 코드를 확인해주세요.")
                return None, "", None
            
            photo, info_text, plot = customer_processor.get_customer_info(
                code, 
                guardian,
                state
            )
            
            if photo is None:
                gr.Error(info_text)
                return None, "", None
            
            return photo, info_text, plot
            
        # Event handler - 버튼 클릭으로 변경
        submit_btn.click(
            fn=get_customer_details,
            inputs=[
                customer_code,
                guardian_code,
                session_state
            ],
            outputs=[
                customer_photo,
                customer_info,
                nutrition_history
            ]
        )
        
    return customer_page