import pandas as pd

def extract_table_from_number_row(file_path, output_path, empty_cell_threshold=0.2, text_ratio_threshold=0.5):
    df = pd.read_excel(file_path, sheet_name=0, header=None)

    # 숫자로 시작하는 첫 데이터 행 찾기
    def starts_with_number(val):
        if pd.isnull(val):
            return False
        if isinstance(val, (int, float)):
            return True
        if isinstance(val, str) and val.strip() and val.strip()[0].isdigit():
            return True
        return False

    row_start_idx = None
    for idx, val in enumerate(df.iloc[:,0]):
        if starts_with_number(val):
            row_start_idx = idx
            break

    if row_start_idx is None:
        print("숫자로 시작하는 행이 없습니다.")
        return None

    df = df.iloc[row_start_idx:, :].reset_index(drop=True)

    def is_not_empty(cell):
        if pd.isnull(cell):
            return False
        if isinstance(cell, str):
            return cell.strip() != ''
        return True

    value_mask = df.applymap(is_not_empty)

    row_empty_ratio = 1 - value_mask.mean(axis=1)
    valid_rows = row_empty_ratio <= empty_cell_threshold

    valid_row_indices = df.index[valid_rows]
    if len(valid_row_indices) == 0:
        print("적합한 행이 없습니다.")
        return None

    col_mask_in_rows = value_mask.loc[valid_row_indices, :]
    valid_cols = col_mask_in_rows.any(axis=0)

    def text_ratio(series):
        non_empty = series.dropna().map(lambda x: isinstance(x, str) and x.strip() != '')
        if len(non_empty) == 0:
            return 0
        return non_empty.sum() / len(non_empty)

    valid_cols = [col for col in df.columns[valid_cols] if text_ratio(df.loc[valid_rows, col]) <= text_ratio_threshold]

    extracted_block = df.loc[valid_rows, valid_cols]
    extracted_block.to_excel(output_path, index=False, header=False)
    return output_path

# 실행 예
extract_table_from_number_row('table_block_filtered.xlsx', 'table_block_number_start.xlsx')
