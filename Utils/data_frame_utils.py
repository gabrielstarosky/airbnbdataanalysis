 
import numpy as np
from scipy import stats as st


def remove_outliers(data_frame, column, method, value_method):

    if(method == 'zscore'):
        zscore_array = st.zscore(data_frame[column])
        abs_zscore_array = np.abs(zscore_array)

        return data_frame[abs_zscore_array <= value_method]
    
    elif(method == 'percentile'):
        minor_percent_value = np.percentile(data_frame[column], value_method[0])
        major_percent_value = np.percentile(data_frame[column], value_method[1])

        data_frame = data_frame[data_frame[column] >= minor_percent_value]
        data_frame = data_frame[data_frame[column] <= major_percent_value]

        return data_frame

    elif(method == 'absolute'):
        minor_value = value_method[0]
        major_value = value_method[1]

        data_frame = data_frame[data_frame[column] >= minor_value]
        data_frame = data_frame[data_frame[column] <= major_value]

        return data_frame
    else:
        raise ValueError("Value '" + method + "' for method arg is not valid.")


def get_corr_diagonal_matrix(data_frame, method='pearson'):

    corr_matrix = data_frame.corr(method=method)

    triang_matrix = np.tril(np.ones(corr_matrix.shape), k=-1)
    triang_matrix[triang_matrix == 0] = np.nan

    corr_matrix = corr_matrix * triang_matrix

    return corr_matrix


def export_list_of_columns(list_of_columns, filename):

    str_list_of_columns = '\n'.join(list_of_columns)

    with open(filename, 'w') as file:
        file.write(str_list_of_columns)


def drop_columns_by_files(data_frame, file_full_list_col, file_list_col_keep):

    def get_list_of_columns(filepath):
        with open(filepath, 'r') as file:
            return [column.strip('\n') for column in file]

    full_list_col = get_list_of_columns(file_full_list_col)
    full_set_col = set(full_list_col)

    list_col_keep = get_list_of_columns(file_list_col_keep)
    set_col_keep = set(list_col_keep)

    set_col_remove = full_set_col - set_col_keep
    list_col_remove = list(set_col_remove)

    return data_frame.drop(columns = list_col_remove)