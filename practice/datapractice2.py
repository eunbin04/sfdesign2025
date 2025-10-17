import pandas as pd

def extract_table_block_no_text_columns(file_path, output_path, empty_cell_threshold=0.2, text_ratio_threshold=0.5):
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

    col_mask_in_rows = value_mask.loc[valid_row_indices, :]
    valid_cols = col_mask_in_rows.any(axis=0)

    # 문자 비율이 높은 열 제외
    def text_ratio(series):
        non_empty = series.dropna().map(lambda x: isinstance(x, str) and x.strip() != '')
        if len(non_empty) == 0:
            return 0
        return non_empty.sum() / len(non_empty)

    valid_cols = [col for col in df.columns[valid_cols] if text_ratio(df.loc[valid_rows, col]) <= text_ratio_threshold]

    extracted_block = df.loc[valid_rows, valid_cols]
    extracted_block.to_excel(output_path, index=False, header=False)
    return output_path

# 사용 예
extract_table_block_no_text_columns('practice.xlsx', 'table_block_filtered.xlsx')
