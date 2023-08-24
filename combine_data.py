#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import argparse

def combine(folder_path):
    tsv_files = [file for file in os.listdir(folder_path) if file.endswith('.tsv')]
    combined_data = pd.concat([pd.read_csv(os.path.join(folder_path, file), sep='\t') for file in tsv_files], ignore_index=True)
    combined_data.to_csv(folder_path+'.tsv', sep='\t', index=False)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="데이터가 들어있는 파일들을 하나로 병합합니다")
    parser.add_argument("input_folder", help="병합할 파일들이 있는 폴더명을 입력하세요.")
    
    args = parser.parse_args()
    
    folder_name = args.input_folder
    combine(folder_name)

