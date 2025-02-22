import os
import sys
import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(parent_dir)

from clients.db_client import DatabaseClient
plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

class CustomerProcessor:
    def __init__(self, db_client=None):
        self.db_client = db_client or DatabaseClient(
            host='azure-mysql-host',
            user='username',
            password='password',
            database='database-name'
        )
    
    def get_customer_info(self, customer_code):
        """Get customer information and visualize nutrition history"""
        if not customer_code:
            return None, "Please enter a customer code.", None, None
        
        try:
            self.db_client.connect()
            customer_info = self.db_client.get_customer_info(customer_code)
            self.db_client.close()
            
            if not customer_info:
                return None, "No customer information found.", None, None
            
            # Process customer photo
            photo = self._process_customer_photo(customer_info['basic_info']['photo_url'])
            
            # Create visualizations
            nutrition_text, nutrition_summary = self._create_nutrition_text(customer_info)
            nutrition_plot = self._create_nutrition_plot(customer_info)
            
            return photo, nutrition_text, nutrition_summary, nutrition_plot
            
        except Exception as e:
            return None, f"Error: {str(e)}", None, None
    
    def _process_customer_photo(self, photo_url):
        """Process and resize customer photo"""
        response = requests.get(photo_url)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return cv2.resize(image, (300, 300))
    
    def _create_nutrition_text(self, customer_info):
        """Create formatted nutrition text"""
        # Format the customer info with HTML and CSS
        customer_info_text = "<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
        customer_info_text += "<strong>고객 상세 정보</strong><br><br>"
        customer_info_text += "<table style='width:100%;'>"
        customer_info_text += f"<tr><td><strong>성함</strong></td><td>{customer_info['basic_info']['name']}</td></tr>"
        customer_info_text += f"<tr><td><strong>생년월일</strong></td><td>{customer_info['basic_info'].get('id_number', 'N/A')}</td></tr>"
        customer_info_text += f"<tr><td><strong>성별</strong></td><td>{customer_info['basic_info'].get('gender', 'N/A')}</td></tr>"
        customer_info_text += f"<tr><td><strong>키</strong></td><td>{customer_info['basic_info'].get('height', 'N/A')} cm</td></tr>"
        customer_info_text += f"<tr><td><strong>몸무게</strong></td><td>{customer_info['basic_info'].get('weight', 'N/A')} kg</td></tr>"
        customer_info_text += f"<tr><td><strong>특이사항</strong></td><td>{customer_info['basic_info'].get('special_conditions', 'N/A')}</td></tr>"
        customer_info_text += "</table>"
        customer_info_text += "</div>"
        
        # Create a text summary of recent nutrition with colored text
        nutrition_summary = "<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
        nutrition_summary += "<strong>최근 영양 섭취 정보</strong><br><br>"
        nutrition_summary += "<br>".join(
            f"날짜: <span style='color:blue;'>{nutrition['date']}</span><br>"
            f"  - 칼로리: <span style='color:red;'>{nutrition['total_calories']} kcal</span><br>"
            f"  - 수분: <span style='color:green;'>{nutrition['total_water']}g</span><br>"
            f"  - 단백질: <span style='color:orange;'>{nutrition['total_protein']}g</span><br>"
            f"  - 지방: <span style='color:purple;'>{nutrition['total_fat']}g</span><br>"
            f"  - 탄수화물: <span style='color:brown;'>{nutrition['total_carbohydrates']}g</span><br>"
            f"  - 당류: <span style='color:pink;'>{nutrition['total_sugar']}g</span><br>"
            for nutrition in customer_info['recent_nutrition']
        )
        nutrition_summary += "</div>"
        
        return customer_info_text, nutrition_summary
    
    def _create_nutrition_plot(self, customer_info):
        """Create nutrition history plot"""
        # Extract data for plotting
        dates = [nutrition['date'] for nutrition in customer_info['recent_nutrition']]
        calories = [nutrition['total_calories'] for nutrition in customer_info['recent_nutrition']]
        water = [nutrition['total_water'] for nutrition in customer_info['recent_nutrition']]
        protein = [nutrition['total_protein'] for nutrition in customer_info['recent_nutrition']]
        fat = [nutrition['total_fat'] for nutrition in customer_info['recent_nutrition']]
        carbohydrates = [nutrition['total_carbohydrates'] for nutrition in customer_info['recent_nutrition']]
        sugar = [nutrition['total_sugar'] for nutrition in customer_info['recent_nutrition']]
        
        # Create separate plots for each nutritional component
        fig, axs = plt.subplots(3, 2, figsize=(12, 10))  # 3 rows, 2 columns

        # Plot Calories
        axs[0, 0].plot(dates, calories, marker='o', label='Calories (kcal)', color='r')
        axs[0, 0].set_title('Calories')
        axs[0, 0].set_xlabel('Date')
        axs[0, 0].set_ylabel('kcal')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Plot Water
        axs[0, 1].plot(dates, water, marker='o', label='Water (g)', color='b')
        axs[0, 1].set_title('Water')
        axs[0, 1].set_xlabel('Date')
        axs[0, 1].set_ylabel('g')
        axs[0, 1].tick_params(axis='x', rotation=45)

        # Plot Protein
        axs[1, 0].plot(dates, protein, marker='o', label='Protein (g)', color='g')
        axs[1, 0].set_title('Protein')
        axs[1, 0].set_xlabel('Date')
        axs[1, 0].set_ylabel('g')
        axs[1, 0].tick_params(axis='x', rotation=45)

        # Plot Fat
        axs[1, 1].plot(dates, fat, marker='o', label='Fat (g)', color='m')
        axs[1, 1].set_title('Fat')
        axs[1, 1].set_xlabel('Date')
        axs[1, 1].set_ylabel('g')
        axs[1, 1].tick_params(axis='x', rotation=45)

        # Plot Carbohydrates
        axs[2, 0].plot(dates, carbohydrates, marker='o', label='Carbohydrates (g)', color='c')
        axs[2, 0].set_title('Carbohydrates')
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('g')
        axs[2, 0].tick_params(axis='x', rotation=45)

        # Plot Sugar
        axs[2, 1].plot(dates, sugar, marker='o', label='Sugar (g)', color='y')
        axs[2, 1].set_title('Sugar')
        axs[2, 1].set_xlabel('Date')
        axs[2, 1].set_ylabel('g')
        axs[2, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig 