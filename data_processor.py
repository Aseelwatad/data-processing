import csv
import logging
import time
from typing import Any, Dict, List, Tuple, Union
import openpyxl
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_path = r"C:\Users\hp1\Documents\estarta\trainee_excel_csv_exercise.xlsx"
csv_file_path = r"C:\Users\hp1\Documents\estarta\csv_data.csv"
csv_builtin_path = r"C:\Users\hp1\Documents\estarta\csv_data_builtin.csv"


def data_reader(
    file_path: str = file_path, retries: int = 3, delay: int = 2
) -> pd.DataFrame:
    """Reads an Excel file using pandas with a retry mechanism."""
    logging.info(f"Attempting to read Excel via pandas: {file_path}")
    for attempt in range(1, retries + 1):
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            logging.info("Data read successfully from Excel file using pandas.")
            return df
        except FileNotFoundError:
            logging.error(f"Excel file not found at path: {file_path}")
            raise
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                logging.error(
                    f"Failed to read Excel after {retries} attempts."
                )
                raise RuntimeError(
                    f"Failed to read {file_path} after {retries} retries."
                ) from e


def data_reader_openpyxl(file_path: str = file_path) -> List[List[Any]]:
    """Reads an Excel file using openpyxl and returns its content as a list of lists."""
    logging.info(f"Attempting to read Excel via openpyxl: {file_path}")
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb.active
        data = [list(row) for row in ws.iter_rows(values_only=True)]
        logging.info(
            f"Data read successfully from Excel file using openpyxl (Sheet: {ws.title})."
        )
        return data
    except Exception as e:
        logging.error(f"Error reading file with openpyxl: {e}")
        raise


def data_writer(
    df: pd.DataFrame, csv_file_path: str = csv_file_path
) -> None:
    """Writes the DataFrame to a CSV file using pandas."""
    try:
        df.to_csv(csv_file_path, index=False, encoding="utf-8")
        logging.info(
            f"Data written successfully to CSV file via pandas: {csv_file_path}"
        )
    except Exception as e:
        logging.error(f"Failed to write CSV via pandas: {e}")
        raise


def data_writer_csv_module(
    df: pd.DataFrame, csv_file_path: str = csv_builtin_path
) -> None:
    """Writes the DataFrame to a CSV file using Python's built-in csv module."""
    try:
        with open(
            csv_file_path, mode="w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(df.columns.tolist())
            writer.writerows(df.values.tolist())
        logging.info(
            f"Data written successfully to CSV file via csv module: {csv_file_path}"
        )
    except Exception as e:
        logging.error(f"Failed to write CSV via built-in module: {e}")
        raise


def rename_columns(
    df: pd.DataFrame, rename_dict: Dict[str, str]
) -> pd.DataFrame:
    """Rename the columns of the DataFrame to match the desired format."""
    if not isinstance(df, pd.DataFrame):
        logging.error("Input 'df' must be a pandas DataFrame.")
        raise TypeError("df must be a pandas DataFrame.")

    if not isinstance(rename_dict, dict):
        logging.error("Input 'rename_dict' must be a dictionary.")
        raise TypeError("rename_dict must be a dictionary.")

    df_columns = df.columns.tolist()
    missing_cols = [old for old in rename_dict.keys() if old not in df_columns]

    if missing_cols:
        error_msg = f"The following columns do not exist in DataFrame: {missing_cols}"
        logging.error(error_msg)
        raise KeyError(error_msg)

    new_df = df.rename(columns=rename_dict)
    logging.info(f"Columns successfully renamed: {rename_dict}")
    return new_df


def check_columns_exist(
    df: pd.DataFrame, columns: Union[str, List[str]]
) -> Tuple[bool, List[str], Dict[str, bool]]:
    """Checks if specified columns exist, returning status, missing list, and mapping."""
    if not isinstance(df, pd.DataFrame):
        logging.error("Input 'df' must be a pandas DataFrame.")
        raise TypeError("df must be a pandas DataFrame.")

    if isinstance(columns, str):
        columns = [columns]

    existing_set = set(df.columns)
    results = {col: (col in existing_set) for col in columns}
    missing_columns = [col for col in columns if not results[col]]
    all_exist = len(missing_columns) == 0

    if all_exist:
        logging.info("All specified columns exist in the DataFrame.")
    else:
        logging.warning(
            f"Missing columns detected: {missing_columns}"
        )

    return all_exist, missing_columns, results


if __name__ == "__main__":
    df = data_reader()
    print("\nData Reader (Pandas):")
    print(df.head())

    print("\nData Reader 1 (OpenPyXL Preview):")
    openpyxl_data = data_reader_openpyxl()
    print(openpyxl_data[:2])

    print("\nValidate Columns Check:")
    test_cols = ["Employee_ID", "Full_Name", "Not_Existing_Column"]
    all_exist, missing_cols, check_dict = check_columns_exist(
        df, test_cols
    )
    print(
        f"All exist: {all_exist} | Missing: {missing_cols} | Details: {check_dict}"
    )

    mapping = {
        "Employee_ID": "Employee ID",
        "Full_Name": "Full Name",
        "Department": "Department",
        "Job_Title": "Job Title",
        "City": "City",
        "Email": "Email",
        "Phone_Number": "Phone Number",
        "Joining_Date": "Joining Date",
        "Employment_Status": "Employment Status",
        "Notes": "Notes",
    }

    renamed_df = rename_columns(df, mapping)
    print("\nRenamed Columns:")
    print(renamed_df.head())

    data_writer(renamed_df, csv_file_path)
    data_writer_csv_module(renamed_df, csv_builtin_path)