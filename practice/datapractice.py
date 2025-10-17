import pandas as pd

def extract_table_block(file_path, output_path, empty_cell_threshold=0.2):
    df = pd.read_excel(file_path, sheet_name=0, header=None)

    def is_not_empty(cell):
        if pd.isnull(cell):
            return False
        if isinstance(cell, str):
            return cell.strip() != ''
        return True

    value_mask = df.applymap(is_not_empty)

    row_empty_ratio = 1 - value_mask.mean(axis=1)
    valid_rows = row_empty_ratio <= empty_cell_threshold

    # valid_rows에 한해서의 완성된 열 범위 구하기
    valid_row_indices = df.index[valid_rows]
    if len(valid_row_indices) == 0:
        print("적합한 행이 없습니다.")
        return None

    # valid_rows내에서 최소, 최대 열 인덱스 구하기
    col_mask_in_rows = value_mask.loc[valid_row_indices, :]
    # 열 중 하나라도 True인 열은 포함
    valid_cols = col_mask_in_rows.any(axis=0)

    # 행과 해당 열만 포함해서 결과 추출
    extracted_block = df.loc[valid_rows, valid_cols]

    extracted_block.to_excel(output_path, index=False, header=False)
    return output_path

# 실행 예
extract_table_block('practice.xlsx', 'table_block_all_cols.xlsx')
