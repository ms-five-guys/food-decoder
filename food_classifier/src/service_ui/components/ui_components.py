import gradio as gr
import re
from components.data_processing import get_customer_info, get_nutritional_info

def extract_number(value):
    """
    문자열에서 숫자만 추출하여 float로 변환
    예: '180kcal' -> 180.0
    """
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r'(\d+\.?\d*)', str(value))
    return float(match.group(1)) if match else 0.0

def create_table_row(food_info, confidence):
    """
    Create an HTML table row for the food information
    """
    return f"""
    <tr>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['food_name']}</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{confidence:.1f}%</td>
        <td style="padding: 16px; text-align: left; border-bottom: 1px solid #e5e5e5;">{food_info['serving_size']}</td>
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

def process_and_append(image, history):
    """
    Process new image and append result to history
    """
    new_result = get_nutritional_info(image)
    
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
        
        # Create initial tables
        tables_html = f"""
        <div style="margin-bottom: 30px;">
        <table style="width:100%; border-collapse: collapse; margin-top: 10px; font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
            <tr>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">음식</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">확률</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">1회 제공량</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">에너지(kcal)</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">수분(g)</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">단백질(g)</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">지방(g)</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">탄수화물(g)</th>
                <th style="padding: 16px; text-align: left; border-bottom: 2px solid #e5e5e5; font-weight: 600;">당류(g)</th>
            </tr>
            {create_table_row(new_result['food_info'], new_result['confidence'])}
        </table>
        </div>

        <div style="margin-top: 30px;">
        <h3 style="margin-bottom: 15px;">영양성분 총계</h3>
        <table style="width:100%; border-collapse: collapse; font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
            <tr>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">에너지<br>(kcal)</th>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">수분<br>(g)</th>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">단백질<br>(g)</th>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">지방<br>(g)</th>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">탄수화물<br>(g)</th>
                <th style="padding: 16px; text-align: right; border-bottom: 2px solid #e5e5e5; font-weight: 600;">당류<br>(g)</th>
            </tr>
            {create_summary_row(totals)}
        </table>
        </div>
        """
    else:
        # Parse previous totals from history
        prev_totals = extract_totals_from_html(history)
        
        # Update totals
        totals = {
            'calories': prev_totals['calories'] + extract_number(new_result['food_info']['calories']),
            'water': prev_totals['water'] + extract_number(new_result['food_info']['water']),
            'protein': prev_totals['protein'] + extract_number(new_result['food_info']['protein']),
            'fat': prev_totals['fat'] + extract_number(new_result['food_info']['fat']),
            'carbohydrates': prev_totals['carbohydrates'] + extract_number(new_result['food_info']['carbohydrates']),
            'sugar': prev_totals['sugar'] + extract_number(new_result['food_info']['sugar'])
        }
        
        # Add new row to existing table and update summary
        tables_html = history.replace("</table>", 
                                    create_table_row(new_result['food_info'], new_result['confidence']) + 
                                    "</table>")
        tables_html = update_summary_table(tables_html, totals)

    return tables_html, tables_html

def extract_totals_from_html(html):
    """
    Extract the current totals from the summary table in the HTML
    """
    # Default values in case we can't extract from HTML
    default_totals = {
        'calories': 0,
        'water': 0,
        'protein': 0,
        'fat': 0,
        'carbohydrates': 0,
        'sugar': 0
    }
    
    if not html:
        return default_totals
    
    # Simple parsing - in production, you might want to use a proper HTML parser
    pattern = r'영양성분 총계.*?<tr>\s*<td[^>]*>(\d+\.?\d*)</td>\s*<td[^>]*>(\d+\.?\d*)</td>\s*<td[^>]*>(\d+\.?\d*)</td>\s*<td[^>]*>(\d+\.?\d*)</td>\s*<td[^>]*>(\d+\.?\d*)</td>\s*<td[^>]*>(\d+\.?\d*)</td>\s*</tr>'
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        return {
            'calories': float(match.group(1)),
            'water': float(match.group(2)),
            'protein': float(match.group(3)),
            'fat': float(match.group(4)),
            'carbohydrates': float(match.group(5)),
            'sugar': float(match.group(6))
        }
    return default_totals

def update_summary_table(html, totals):
    """
    Update the summary table in the HTML with new totals
    """
    # Replace only the summary row, preserving the headers
    pattern = r'(<div style="margin-top: 30px;">.*?<tr>.*?</tr>)\s*<tr>.*?</tr>\s*</table>'
    replacement = f'\\1\n{create_summary_row(totals)}</table>'
    return re.sub(pattern, replacement, html, flags=re.DOTALL)

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
        gr.Markdown("## 📱 Nutritional Information")
        gr.Markdown("Upload or take photos of food to get nutritional information")
        
        with gr.Row():
            image_input = gr.Image(
                sources=["webcam", "upload"],
                type="numpy",
                label="Camera"
            )

        # Submit button in its own row
        submit_btn = gr.Button("Submit", variant="primary")

        with gr.Row():
            result_output = gr.HTML(label="Nutritional Information")

        # State to store the history
        result_state = gr.State("")
        
        submit_btn.click(
            fn=process_and_append,
            inputs=[image_input, result_state],
            outputs=[result_output, result_state]
        )

    return customer_info_interface, nutritional_info_interface