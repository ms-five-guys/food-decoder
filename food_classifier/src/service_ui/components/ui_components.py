import gradio as gr
import re
from components.data_processing import get_customer_info, get_nutritional_info

def extract_number(value):
    """
    extract numbers from string and convert to float
    example: '180kcal' -> 180.0
    """
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r'(\d+\.?\d*)', str(value))
    return float(match.group(1)) if match else 0.0

def create_table_row(food_info, confidence):
    """
    create an HTML table row for the food information
    """
    return f"""
    <tr>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['food_name']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{confidence:.1f}%</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['calories']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['water']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['protein']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['fat']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['carbohydrates']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['sugar']}</td>
    </tr>
    """

def create_summary_row(totals):
    """
    Create an HTML table row for the total nutritional information
    """
    return f"""
    <tr>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['calories']):.1f}</td>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['water']):.1f}</td>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['protein']):.1f}</td>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['fat']):.1f}</td>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['carbohydrates']):.1f}</td>
        <td style="padding: 16px; text-align: right; border-bottom: 1px solid #e5e5e5;">{float(totals['sugar']):.1f}</td>
    </tr>
    """

def create_food_card(food_info, confidence):
    """
    Create a card for food information
    """
    return f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin-bottom: 15px; align-items: center; overflow-x: auto;">
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">음식명</div>
            <div style="font-size: 0.9em; margin-top: 2px; overflow: hidden; text-overflow: ellipsis;">{food_info['food_name']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">확률</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{confidence:.1f}%</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">에너지</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['calories']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">수분</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['water']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">단백질</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['protein']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">지방</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['fat']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">탄수화물</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['carbohydrates']}</div>
        </div>
        <div>
            <div style="font-size: 0.75em; color: #666; white-space: nowrap;">당류</div>
            <div style="font-size: 0.9em; margin-top: 2px;">{food_info['sugar']}</div>
        </div>
    </div>
    <hr style="margin: 15px 0; border: none; border-top: 1px solid #e0e0e0;">
    """

def create_warning_section(totals):
    """
    create warning section for nutritional components intake
    """
    recommended = get_recommended_daily_values()
    warnings = []
    
    # calculate intake percentage for each nutritional component and check if it exceeds 100%
    percentages = {
        '에너지': (totals['calories'] / recommended['calories']) * 100,
        '수분': (totals['water'] / recommended['water']) * 100,
        '단백질': (totals['protein'] / recommended['protein']) * 100,
        '지방': (totals['fat'] / recommended['fat']) * 100,
        '탄수화물': (totals['carbohydrates'] / recommended['carbohydrates']) * 100,
        '당류': (totals['sugar'] / recommended['sugar']) * 100
    }
    
    # collect over items 100%
    over_items = [f"{name}({int(pct)}%)" for name, pct in percentages.items() if pct > 100]
    
    if not over_items:
        return ""  # if no over items, return empty string
    
    warning_text = ", ".join(over_items) + " 항목에서 권장섭취량을 초과했습니다."
    
    return f"""
    <div style="padding: 15px; border-radius: 15px; border: 1px solid #FFB74D; margin-bottom: 20px; 
         background-color: #FFF3E0; overflow: hidden;">
        <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #F57C00;">⚠️ 섭취량 경고</h3>
        <div style="font-size: 0.9em; color: #E65100;">
            {warning_text}
        </div>
    </div>
    """

def process_and_append(image, history):
    """
    Process new image and append result to history
    """
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
    new_result = get_nutritional_info(image)
    
    # get_nutritional_info 결과 검증
    if not new_result or 'food_info' not in new_result:
        error_html = f"""
        <div style="padding: 15px; border-radius: 15px; border: 1px solid #FF5252; margin-bottom: 20px; 
             background-color: #FFEBEE; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #D32F2F;">❌ 오류</h3>
            <div style="font-size: 0.9em; color: #C62828;">
                음식을 인식할 수 없습니다. 다시 시도해주세요.
            </div>
        </div>
        """
        return history + error_html if history else error_html, history if history else ""

    if not history:
        # Initialize totals
        totals = {
            'calories': extract_number(new_result['food_info']['calories']),
            'water': extract_number(new_result['food_info']['water']),
            'protein': extract_number(new_result['food_info']['protein']),
            'fat': extract_number(new_result['food_info']['fat']),
            'carbohydrates': extract_number(new_result['food_info']['carbohydrates']),
            'sugar': extract_number(new_result['food_info']['sugar'])
        }
        
        # Create initial HTML with all sections
        tables_html = f"""
        <div id="today-nutrition" style="padding: 15px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; overflow: hidden;">
            <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">🍽️ 오늘의 식단</h3>
            <div class="food-cards" style="overflow-x: auto;">
                {create_food_card(new_result['food_info'], new_result['confidence'])}
            </div>
        </div>
        <div id="nutrition-summary">
            {create_summary_section(totals)}
        </div>
        <div id="nutrition-warning">
            {create_warning_section(totals)}
        </div>
        """
    else:
        # Parse previous totals and update
        prev_totals = extract_totals_from_html(history)
        totals = {
            'calories': prev_totals['calories'] + extract_number(new_result['food_info']['calories']),
            'water': prev_totals['water'] + extract_number(new_result['food_info']['water']),
            'protein': prev_totals['protein'] + extract_number(new_result['food_info']['protein']),
            'fat': prev_totals['fat'] + extract_number(new_result['food_info']['fat']),
            'carbohydrates': prev_totals['carbohydrates'] + extract_number(new_result['food_info']['carbohydrates']),
            'sugar': prev_totals['sugar'] + extract_number(new_result['food_info']['sugar'])
        }
        
        # Split HTML into sections using unique IDs
        sections = history.split('<div id="nutrition-summary">')
        if len(sections) != 2:
            return history, history  # Return unchanged if structure is invalid
            
        today_nutrition = sections[0]
        
        # Add new card to Today Nutrition section
        card_insert_point = today_nutrition.rfind('</div>')
        if card_insert_point != -1:
            # Insert new card before the last </div> of food-cards
            today_nutrition = (
                today_nutrition[:card_insert_point] +
                create_food_card(new_result['food_info'], new_result['confidence']) +
                today_nutrition[card_insert_point:]
            )
        
        # Create new HTML with updated sections
        tables_html = (
            today_nutrition +
            '<div id="nutrition-summary">' +
            create_summary_section(totals) +
            create_warning_section(totals)
        )

    return tables_html, tables_html

def extract_totals_from_html(html):
    """
    Extract the current totals from the summary section in the HTML
    """
    recommended = get_recommended_daily_values()
    
    # Find percentage values in the summary section
    pattern = r'<div style="font-size: 0.9em; text-align: right;">(\d+)%</div>'
    matches = re.findall(pattern, html)
    
    if len(matches) == 6:  # All six nutritional values found
        return {
            'calories': (float(matches[0]) / 100) * recommended['calories'],
            'water': (float(matches[1]) / 100) * recommended['water'],
            'protein': (float(matches[2]) / 100) * recommended['protein'],
            'fat': (float(matches[3]) / 100) * recommended['fat'],
            'carbohydrates': (float(matches[4]) / 100) * recommended['carbohydrates'],
            'sugar': (float(matches[5]) / 100) * recommended['sugar']
        }
    
    # Return default values if pattern not found
    return {
        'calories': 0,
        'water': 0,
        'protein': 0,
        'fat': 0,
        'carbohydrates': 0,
        'sugar': 0
    }

def update_summary_table(html, totals):
    """
    Update the summary table in the HTML with new totals
    """
    # Replace only the summary row, preserving the headers
    pattern = r'(<div style="margin-top: 20px;">.*?<tr>.*?</tr>)\s*<tr>.*?</tr>\s*</table>'
    replacement = f'\\1\n{create_summary_row(totals)}</table>'
    return re.sub(pattern, replacement, html, flags=re.DOTALL)

def create_summary_section(totals):
    """
    create summary section for nutritional components
    """
    recommended = get_recommended_daily_values()
    
    return f"""
    <div style="padding: 15px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; overflow: hidden;">
        <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">📊 하루 권장 영양성분 총계</h3>
        <div style="display: grid; grid-template-columns: 1fr 3fr 1fr; gap: 10px; align-items: center;">
            <div style="font-size: 0.9em; color: #666;">에너지</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['calories'] / recommended['calories']) * 100}%; height: 100%; 
                     background-color: #4CAF50; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['calories'] / recommended['calories']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">수분</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['water'] / recommended['water']) * 100}%; height: 100%; 
                     background-color: #2196F3; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['water'] / recommended['water']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">단백질</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['protein'] / recommended['protein']) * 100}%; height: 100%; 
                     background-color: #FF9800; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['protein'] / recommended['protein']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">지방</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['fat'] / recommended['fat']) * 100}%; height: 100%; 
                     background-color: #E91E63; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['fat'] / recommended['fat']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">탄수화물</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['carbohydrates'] / recommended['carbohydrates']) * 100}%; height: 100%; 
                     background-color: #9C27B0; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['carbohydrates'] / recommended['carbohydrates']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">당류</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['sugar'] / recommended['sugar']) * 100}%; height: 100%; 
                     background-color: #FF5722; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['sugar'] / recommended['sugar']) * 100)}%</div>
        </div>
    </div>
    """

def get_recommended_daily_values():
    """
    return daily recommended intake
    based on 2020 Korean Dietary Reference Intakes for Koreans
    adult male standard (19-29 years old)
    """
    return {
        'calories': 2600,     # kcal
        'water': 2500,        # ml
        'protein': 65,        # g
        'fat': 65,           # g (총 에너지의 약 20-25%)
        'carbohydrates': 360, # g (총 에너지의 약 55-65%)
        'sugar': 50          # g (총 에너지의 10% 이내)
    }

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
            """
            image processing and error handling
            """
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

    return customer_info_interface, nutritional_info_interface