# import os
# import json
# import csv
# import random

# def extract_data_from_json(json_file):
#     with open(json_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     # 필요한 데이터 추출
#     tourist_attraction_kr = data['annotations'][1]['k_context']
#     tourist_attraction_en = data['annotations'][1]['t_context']
    
#     return tourist_attraction_kr, tourist_attraction_en

# def process_folder(folder_path, sample_size):
#     all_data = []
    
#     # 폴더 내 모든 JSON 파일 처리
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             json_file_path = os.path.join(folder_path, filename)
#             tourist_attraction_kr, tourist_attraction_en = extract_data_from_json(json_file_path)
#             all_data.append((tourist_attraction_kr, tourist_attraction_en))
    
#     # 샘플 수 조정
#     if sample_size > len(all_data):
#         sample_size = len(all_data)
    
#     # 무작위 샘플링
#     sampled_data = random.sample(all_data, sample_size)
    
#     # CSV 파일로 저장
#     csv_file_path = os.path.join(folder_path, 'tourist_attractions.csv')
#     with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         # CSV 헤더 작성
#         csv_writer.writerow(['관광지명', 'Tourist Attraction'])
        
#         # CSV에 샘플 데이터 작성
#         for tourist_attraction in sampled_data:
#             csv_writer.writerow(tourist_attraction)
    
#     print(f"CSV 파일이 '{csv_file_path}'로 저장되었습니다.")

# # 사용자로부터 폴더 경로와 샘플 수 입력 받기
# folder_path = input("폴더 경로를 입력하세요: ")
# sample_size = int(input("추출할 샘플 수를 입력하세요: "))

# process_folder(folder_path, sample_size)

import os
import json
import csv

def extract_data_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 필요한 데이터 추출
    tourist_attraction_kr = data['annotations'][1]['k_context']
    tourist_attraction_en = data['annotations'][1]['t_context']
    
    return tourist_attraction_kr, tourist_attraction_en

def process_folder(folder_path):
    csv_file_path = os.path.join(folder_path, '숙박_일본어_24336.csv')
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # CSV 헤더 작성
        csv_writer.writerow(['관광지명', 'Tourist Attraction'])
        
        # 폴더 내 모든 JSON 파일 처리
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                json_file_path = os.path.join(folder_path, filename)
                tourist_attraction_kr, tourist_attraction_en = extract_data_from_json(json_file_path)
                # CSV에 데이터 작성
                csv_writer.writerow([tourist_attraction_kr, tourist_attraction_en])
    
    print(f"CSV 파일이 '{csv_file_path}'로 저장되었습니다.")

# 사용자로부터 폴더 경로 입력 받기
folder_path = input("폴더 경로를 입력하세요: ")
process_folder(folder_path)