import os
import sys
import re
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from utils.food_processing import FoodProcessor
from utils.nutrition_utils import (
    create_food_card,
    create_summary_section,
    create_warning_section,
    extract_number,
    get_recommended_daily_values
)

# Initialize processor
food_processor = FoodProcessor()

def process_and_append(image, history):
    """Process new image and append result to history"""
    # if image is not present, process
    if image is None:
        error_html = f"""
        <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; margin-bottom: 20px; 
             background-color: #FFEBEE; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #D32F2F;">❌ 오류</h3>
            <div style="font-size: 0.9em; color: #C62828;">
                이미지를 먼저 촬영해주세요.
            </div>
        </div>
        """
        return history + error_html if history else error_html, history if history else ""
    
    # 이미지가 있는 경우 기존 로직 실행
    result = food_processor.get_nutritional_info(image)
    
    # get_nutritional_info 결과 검증
    if not result or 'food_info' not in result:
        error_html = f"""
        <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; margin-bottom: 20px; 
             background-color: #FFEBEE; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #D32F2F;">❌ 오류</h3>
            <div style="font-size: 0.9em; color: #C62828;">
                머신러닝 서버에서 오류가 발생했습니다. 다시 시도해주세요.
            </div>
        </div>
        """
        return history + error_html if history else error_html, history if history else ""

    # 새로운 음식 카드 생성
    new_food_card = create_food_card(result['food_info'], result['confidence'])
    
    # 첫 번째 음식인 경우 (history가 비어있는 경우)
    if not history:
        totals = {
            'calories': extract_number(result['food_info'].get('Energy', '0')),
            'carbohydrates': extract_number(result['food_info'].get('Carbohydrates', '0')),
            'protein': extract_number(result['food_info'].get('Protein', '0')),
            'fat': extract_number(result['food_info'].get('Fat', '0')),
            'fiber': extract_number(result['food_info'].get('Dietary_Fiber', '0')),
            'sodium': extract_number(result['food_info'].get('Sodium', '0'))
        }
        
        # 경고 섹션 생성
        warning_section = create_warning_section(totals)
        
        # 요약 섹션 생성
        summary_section = create_summary_section(totals)
        
        # 전체 HTML 생성
        full_html = f"""
        {warning_section}
        {summary_section}
        <div style="margin-top: 20px;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 식사 기록</h3>
            {new_food_card}
        </div>
        """
        
        return full_html, full_html
    
    # 기존 기록이 있는 경우
    else:
        # 현재 총계 추출
        current_totals = extract_totals_from_html(history)
        
        # 새로운 음식의 영양성분을 더함
        new_totals = {
            'calories': current_totals['calories'] + extract_number(result['food_info'].get('Energy', '0')),
            'carbohydrates': current_totals['carbohydrates'] + extract_number(result['food_info'].get('Carbohydrates', '0')),
            'protein': current_totals['protein'] + extract_number(result['food_info'].get('Protein', '0')),
            'fat': current_totals['fat'] + extract_number(result['food_info'].get('Fat', '0')),
            'fiber': current_totals['fiber'] + extract_number(result['food_info'].get('Dietary_Fiber', '0')),
            'sodium': current_totals['sodium'] + extract_number(result['food_info'].get('Sodium', '0'))
        }
        
        # 경고 섹션 업데이트
        warning_section = create_warning_section(new_totals)
        
        # 요약 섹션 업데이트
        summary_section = create_summary_section(new_totals)
        
        # 기존 음식 기록 찾기 (🍽️ 식사 기록 제목 이후부터 다음 div 닫기 태그까지)
        start_idx = history.find('🍽️ 식사 기록</h3>')
        if start_idx != -1:
            start_idx = history.find('</h3>', start_idx) + 5  # </h3> 다음부터
            food_records = history[start_idx:].strip()
        else:
            food_records = ""
        
        # 음식 기록에 새로운 카드 추가
        updated_food_records = f"""
        <div style="margin-top: 20px;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 식사 기록</h3>
            {new_food_card}
            {food_records}
        </div>
        """
        
        # 전체 HTML 업데이트
        full_html = f"""
        {warning_section}
        {summary_section}
        {updated_food_records}
        """
        
        return full_html, full_html

def extract_totals_from_html(html):
    """Extract the current totals from the summary section in the HTML"""
    recommended = get_recommended_daily_values()
    
    # Find all percentage values in the summary section
    percentages = re.findall(r'text-align: right;">(\d+)%</div>', html)
    
    if len(percentages) >= 6:  # Make sure we found all 6 nutritional components
        return {
            'calories': (float(percentages[0]) / 100) * recommended['calories'],
            'carbohydrates': (float(percentages[1]) / 100) * recommended['carbohydrates'],
            'protein': (float(percentages[2]) / 100) * recommended['protein'],
            'fat': (float(percentages[3]) / 100) * recommended['fat'],
            'fiber': (float(percentages[4]) / 100) * recommended['fiber'],
            'sodium': (float(percentages[5]) / 100) * recommended['sodium']
        }
    else:
        return {
            'calories': 0,
            'carbohydrates': 0,
            'protein': 0,
            'fat': 0,
            'fiber': 0,
            'sodium': 0
        }

def create_nutrition_interface():
    """Create nutritional information interface"""
    with gr.Blocks() as nutritional_info_interface:
        gr.Markdown("## 🥗 Nutritional Information")

        with gr.Row():
            image_input = gr.Image(
                sources=["upload", "webcam"],
                type="pil",
                label="Camera",
                height=320,
                width=400,
                mirror_webcam=False
            )

        with gr.Row():
            submit_btn = gr.Button("Submit", variant="primary")

        # error message for error handling
        error_output = gr.HTML(label="", elem_classes=["error-message"])

        # result output for result
        result_output = gr.HTML(label="Nutritional Information")

        # State to store the history
        result_state = gr.State("")

        def process_with_error_handling(image, history):
            """Image processing and error handling"""
            if image is None:
                error_html = f"""
                <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; 
                     background-color: #FFEBEE; overflow: hidden;">
                    <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #D32F2F;">❌ 오류</h3>
                    <div style="font-size: 0.9em; color: #C62828;">
                        이미지를 먼저 촬영해주세요.
                    </div>
                </div>
                """
                return error_html, "", history  # error message, empty result, keep previous history

            # if image is present, process
            try:
                result = process_and_append(image, history)
                return "", result[0], result[1]  # empty error message, result, new history
            except Exception as e:
                error_html = f"""
                <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; 
                     background-color: #FFEBEE; overflow: hidden;">
                    <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #D32F2F;">❌ 오류</h3>
                    <div style="font-size: 0.9em; color: #C62828;">
                        음식을 인식할 수 없습니다. 다시 시도해주세요.
                    </div>
                </div>
                """
                return error_html, "", history  # error message, empty result, keep previous history

        submit_btn.click(
            fn=process_with_error_handling,
            inputs=[image_input, result_state],
            outputs=[error_output, result_output, result_state]
        )

    return nutritional_info_interface 