import os
import sys
import re
import gradio as gr

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from processors.food_processing import FoodProcessor
from processors.nutrition_utils import (
    create_food_card,
    create_summary_section,
    create_warning_section,
    extract_number
)

# Initialize processor
food_processor = FoodProcessor()

def process_and_append(image, history, session_state):
    """
    Process new image and append result to history
    """
    # Get recommended values first
    recommended_values = food_processor.get_recommended_values(session_state)
    if not recommended_values:
        error_html = """
        <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; margin-bottom: 20px; 
             background-color: #FFEBEE; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #1976D2;">ℹ️ 안내</h3>
            <div style="font-size: 0.9em; color: #0D47A1;">
                고객 정보가 필요합니다. 고객 코드와 보호자 코드를 입력해 주세요.
            </div>
        </div>
        """
        return error_html, ""

    # Get today's consumption history if no history exists
    if not history:
        food_processor.db_communicator.connect()
        consumption_records = food_processor.db_communicator.get_today_consumption_by_patient(session_state.customer_id)
        
        if consumption_records:
            # Initialize totals
            totals = {
                'calories': 0,
                'carbohydrates': 0,
                'protein': 0,
                'fat': 0,
                'fiber': 0,
                'sodium': 0
            }
            
            # Create food cards for each record
            food_cards = []
            for record in consumption_records:
                food_info = food_processor.db_communicator.get_food_info_by_id(record['food_id'])
                if food_info:
                    totals['calories'] += extract_number(food_info.get('Energy', '0'))
                    totals['carbohydrates'] += extract_number(food_info.get('Carbohydrates', '0'))
                    totals['protein'] += extract_number(food_info.get('Protein', '0'))
                    totals['fat'] += extract_number(food_info.get('Fat', '0'))
                    totals['fiber'] += extract_number(food_info.get('Dietary_Fiber', '0'))
                    totals['sodium'] += extract_number(food_info.get('Sodium', '0'))
                    
                    # Create food card with time information
                    food_cards.append(create_food_card(food_info, 1.0, record['time']))  # Added time parameter
            
            food_processor.db_communicator.close()
            
            if food_cards:
                # Create warning and summary sections
                warning_section = create_warning_section(totals, recommended_values)
                summary_section = create_summary_section(totals, recommended_values)
                
                # Combine all food cards
                food_records = "\n".join(food_cards)
                
                # Create full history HTML
                history = f"""
                {warning_section}
                {summary_section}
                <div style="margin-top: 20px;">
                    <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 오늘 식사 기록</h3>
                    {food_records}
                </div>
                """
        else:
            food_processor.db_communicator.close()
            print("No previous records found")
            history = ""

    # if image is not present, return current history
    if image is None:
        error_html = f"""
        <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; margin-bottom: 20px; 
             background-color: #FFEBEE; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #1976D2;">ℹ️ 안내</h3>
            <div style="font-size: 0.9em; color: #0D47A1;">
                이미지를 먼저 촬영해주세요.
            </div>
        </div>
        """
        return history + error_html if history else error_html, history if history else ""
    
    result = food_processor.get_nutritional_info(image, session_state)
    
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
        warning_section = create_warning_section(totals, recommended_values)
        
        # 요약 섹션 생성
        summary_section = create_summary_section(totals, recommended_values)
        
        # 전체 HTML 생성
        full_html = f"""
        {warning_section}
        {summary_section}
        <div style="margin-top: 20px;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 오늘 식사 기록</h3>
            {new_food_card}
        </div>
        """
        
        return full_html, full_html
    
    # 기존 기록이 있는 경우
    else:
        # 현재 총계 추출
        current_totals = extract_totals_from_html(history, recommended_values)
        
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
        warning_section = create_warning_section(new_totals, recommended_values)
        
        # 요약 섹션 업데이트
        summary_section = create_summary_section(new_totals, recommended_values)
        
        start_idx = history.find('🍽️ 오늘 식사 기록</h3>')
        if start_idx != -1:
            start_idx = history.find('</h3>', start_idx) + 5  # </h3> 다음부터
            food_records = history[start_idx:].strip()
        else:
            food_records = ""
            
        # 디버그 로그 추가
        print("\n=== Food Records Debug Log ===")
        print(f"Start Index: {start_idx}")
        print(f"History Length: {len(history)}")
        print(f"Found Records: {bool(food_records)}")
        print(f"Food Records: {food_records[:100]}...")  # 처음 100자만 출력
        
        # 음식 기록에 새로운 카드 추가
        updated_food_records = f"""
        <div style="margin-top: 20px;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 오늘 식사 기록</h3>
            {new_food_card}
            {food_records}
        </div>
        """
        print(f"Updated Records Length: {len(updated_food_records)}")
        print("=== Debug Log End ===\n")
        
        # 전체 HTML 업데이트
        full_html = f"""
        {warning_section}
        {summary_section}
        {updated_food_records}
        """
        
        return full_html, full_html

def extract_totals_from_html(html, recommended):
    """Extract the current totals from the summary section in the HTML"""

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

def create_nutrition_page(session_state):
    """
    Create nutritional information page
    """
    with gr.Blocks() as nutrition_page:
        gr.Markdown("## 🥗 오늘의 식단 정보")

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

        def process_with_error_handling(image, history, session_state):
            """
            Image processing and error handling
            """
            if image is None:
                error_html = f"""
                <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; 
                     background-color: #FFEBEE; overflow: hidden;">
                    <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #1976D2;">ℹ️ 안내</h3>
                    <div style="font-size: 0.9em; color: #0D47A1;">
                        이미지를 먼저 촬영해주세요.
                    </div>
                </div>
                """
                return error_html, "", history  # error message, empty result, keep previous history

            # if image is present, process
            try:
                result = process_and_append(image, history, session_state)
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
            inputs=[image_input, result_state, session_state],
            outputs=[error_output, result_output, result_state]
        )

    return nutrition_page 