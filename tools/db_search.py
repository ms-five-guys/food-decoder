import pandas as pd
import os
 
# 현재 스크립트의 절대 경로를 기준으로 파일 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "food_db.csv")
search_file_path = os.path.join(script_dir, "search_words.txt")

# CP949로 파일 읽기
df = pd.read_csv(db_path, encoding='cp949')
# 상위 3개 행 출력
print(df.head(3))

# 빈 DataFrame 생성 (최종 결과 저장용)
final_result = pd.DataFrame(columns=df.columns)
 
# "식품명" 컬럼 확인
if "식품명" in df.columns:
    # 검색어 파일 읽기
    try:
        with open(search_file_path, 'r', encoding='utf-8') as f:
            search_words = [line.strip() for line in f if line.strip()]
        
        print(f"📝 검색어 파일에서 {len(search_words)}개의 검색어를 읽어왔습니다.")
        
        # 각 검색어에 대해 검색 수행
        for search_word in search_words:
            # 검색 결과 필터링 (대소문자 구분 없이 포함된 값 찾기)
            result = df[df["식품명"].str.contains(search_word, case=False, na=False)]
            
            if not result.empty:
                print(f"\n검색어 '{search_word}'에 대한 결과:")
                print(result[["식품명"]])
                
                # 검색 결과를 최종 DataFrame에 추가
                final_result = pd.concat([final_result, result], ignore_index=True)
                print(f"✅ '{search_word}' 관련 데이터를 임시 DB에 저장했습니다.")
            else:
                print(f"❌ '{search_word}'을(를) 포함하는 식품이 없습니다.")
                
    except FileNotFoundError:
        print(f"❌ 검색어 파일({search_file_path})을 찾을 수 없습니다.")
        print("파일을 생성하고 검색어를 한 줄에 하나씩 입력해주세요.")
        exit()

    # 최종 데이터 저장
    if not final_result.empty:
        final_filename = "final_searched_foods.csv"
        final_result.to_csv(final_filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ 모든 검색 데이터를 '{final_filename}' 파일로 저장했습니다.")
        print(f"📥 다운로드를 원하면 해당 파일을 확인하세요.")
    else:
        print("\n❌ 저장된 검색 결과가 없습니다. 파일이 생성되지 않았습니다.")
 
else:
    print("❌ '식품명' 컬럼이 존재하지 않습니다. 컬럼 이름을 확인하세요.")