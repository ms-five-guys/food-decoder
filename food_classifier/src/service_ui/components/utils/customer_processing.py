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
    
    def get_customer_info(self, customer_code, guardian_code):
        """Get customer information and visualize nutrition history"""
        if not customer_code or not guardian_code:
            return None, "고객 코드 또는 보호자 코드를 확인해주세요.", None, None
        
        try:
            self.db_client.connect()
            
            # 고객 코드와 보호자 코드를 합쳐서 하나의 코드로 생성
            combined_code = f"{customer_code}-{guardian_code}"
            
            # 고객 기본 정보 조회
            customer_info = self.db_client.get_customer_basic_info(combined_code)
            
            if not customer_info:
                self.db_client.close()
                return None, "고객 정보를 찾을 수 없습니다.", None, None
            
            # 영양 정보 조회
            nutrition_info = self.db_client.get_customer_nutrition_info(customer_info['customer_id'])
            
            self.db_client.close()
            
            # Process customer photo
            photo = self._process_customer_photo(customer_info['photo_url'])
            
            # Create visualizations
            customer_detail_text = self._create_customer_detail_text(customer_info)
            nutrition_plot = self._create_nutrition_plot(nutrition_info)
            
            return photo, customer_detail_text, nutrition_plot
            
        except Exception as e:
            return None, f"오류가 발생했습니다: {str(e)}", None, None
    
    def _process_customer_photo(self, photo_url):
        """Process and resize customer photo"""
        response = requests.get(photo_url)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return cv2.resize(image, (300, 300))
    
    def _create_customer_detail_text(self, customer_info):
        """Create formatted customer detail text"""
        # Format the customer info with HTML and CSS
        customer_info_text = "<div style='border: 1px solid #ccc; padding: 10px; border-radius: 5px;'>"
        customer_info_text += "<strong>고객 상세 정보</strong><br><br>"
        customer_info_text += "<table style='width:100%;'>"
        customer_info_text += f"<tr><td><strong>성함</strong></td><td>{customer_info['name']}</td></tr>"
        customer_info_text += f"<tr><td><strong>성별</strong></td><td>{'남성' if customer_info['gender'] == 'M' else '여성'}</td></tr>"
        customer_info_text += f"<tr><td><strong>나이</strong></td><td>{customer_info['age']}세</td></tr>"
        customer_info_text += f"<tr><td><strong>키</strong></td><td>{customer_info['height']} cm</td></tr>"
        customer_info_text += f"<tr><td><strong>몸무게</strong></td><td>{customer_info['weight']} kg</td></tr>"
        customer_info_text += f"<tr><td><strong>특이사항</strong></td><td>{customer_info['notes']}</td></tr>"
        customer_info_text += "</table>"
        customer_info_text += "</div>"
        
        return customer_info_text
    
    def _create_nutrition_plot(self, customer_info):
        """Create nutrition history plot in a single vertical column"""
        dates = [nutrition['date'] for nutrition in customer_info['recent_nutrition']]
        
        plot_configs = [
            {'data': 'total_calories', 'title': 'Calories', 'color': '#FF6B6B', 'ylabel': 'kcal', 'rec_key': 'calories'},
            {'data': 'total_water', 'title': 'Water', 'color': '#45B7D1', 'ylabel': 'g', 'rec_key': 'water'},
            {'data': 'total_protein', 'title': 'Protein', 'color': '#96E072', 'ylabel': 'g', 'rec_key': 'protein'},
            {'data': 'total_fat', 'title': 'Fat', 'color': '#E8A2FF', 'ylabel': 'g', 'rec_key': 'fat'},
            {'data': 'total_carbohydrates', 'title': 'Carbohydrates', 'color': '#FFD93D', 'ylabel': 'g', 'rec_key': 'carbohydrates'},
            {'data': 'total_sugar', 'title': 'Sugar', 'color': '#FF8B94', 'ylabel': 'g', 'rec_key': 'sugar'}
        ]
        
        fig, axs = plt.subplots(len(plot_configs), 1, figsize=(10, 24))
        plt.rcParams['font.size'] = 14

        for idx, config in enumerate(plot_configs):
            values = [nutrition[config['data']] for nutrition in customer_info['recent_nutrition']]
            rec_range = customer_info['recommended_nutrition'][config['rec_key']]
            min_val, max_val = rec_range['min'], rec_range['max']
            
            line = axs[idx].plot(dates, values, 
                               color=config['color'],
                               linewidth=2,
                               label=f"{config['title']} ({config['ylabel']})")
            
            axs[idx].scatter(dates, values, 
                            color=config['color'],
                            s=64)
            
            for date, value in zip(dates, values):
                if value < min_val:
                    axs[idx].scatter(date, value, 
                                   color='#FF4444',
                                   s=100,
                                   zorder=5)
                    axs[idx].annotate(f'{value}', 
                                    xy=(date, value),
                                    xytext=(5, 5),
                                    textcoords='offset points',
                                    color='#FF4444',
                                    fontweight='bold')
                elif value > max_val:
                    axs[idx].scatter(date, value, 
                                   color='#FFA500',
                                   s=100,
                                   zorder=5)
                    axs[idx].annotate(f'{value}', 
                                    xy=(date, value),
                                    xytext=(5, 5),
                                    textcoords='offset points',
                                    color='#FFA500',
                                    fontweight='bold')

            axs[idx].axhline(y=min_val, color='#666666', linestyle='--', alpha=0.5)
            axs[idx].axhline(y=max_val, color='#666666', linestyle='--', alpha=0.5)
            axs[idx].fill_between(dates, min_val, max_val,
                                color='#FFFFFF', alpha=0.1,
                                label=f'Recommended ({min_val}-{max_val})')
            
            axs[idx].set_title(config['title'], fontsize=16, pad=15)
            axs[idx].set_xlabel('Date', fontsize=14)
            axs[idx].set_ylabel(config['ylabel'], fontsize=14)
            axs[idx].tick_params(axis='both', labelsize=12)
            axs[idx].tick_params(axis='x', rotation=45)
            axs[idx].legend(fontsize=12)

        plt.tight_layout(pad=4.0)
        return fig 