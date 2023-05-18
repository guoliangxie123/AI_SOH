import pandas as pd
import os
from tqdm import tqdm


def con_file(path):
    all_file = os.listdir(path)
    for i in tqdm(all_file):
        new_path = path+'/'+i
        file_name = i[:-5]
        # 读取Excel文件中的所有sheet
        excel_file = pd.ExcelFile(new_path)
        sheets = excel_file.sheet_names

        # 创建一个空的DataFrame来存储合并后的数据
        merged_data = pd.DataFrame(columns=['数据时间'])

        # 遍历每个sheet，将数据按列"数据时间"进行合并
        for sheet in sheets:
            if sheet == '车辆运行数据':
                merged_data = pd.read_excel(excel_file,sheet_name=sheet)
            else:
                df = pd.read_excel(excel_file,sheet_name=sheet)
                merged_data = pd.merge(merged_data, df, on='数据时间', how='left')

        merged_data.to_excel(f'../data/train/{file_name}.xlsx',index=False)

if __name__ == '__main__':
    con_file(path="../15台车运行数据")





