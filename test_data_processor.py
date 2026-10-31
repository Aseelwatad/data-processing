import pandas as pd
import pytest
from data_processor import check_columns_exist, rename_columns


# Fixture: لتجهيز داتا وهمية سريعة بالذاكرة بدون فتح ملفات خارجية
@pytest.fixture
def sample_df():
    data = {
        "Employee_ID": [1001, 1002],
        "Full_Name": ["Ahmad Khalil", "Lina Haddad"],
        "Department": ["Engineering", "Data"],
    }
    return pd.DataFrame(data)


# Test 1 (Positive): التأكد من نجاح إعادة تسمية الأعمدة بالحالة الطبيعية
def test_rename_columns_positive(sample_df):
    mapping = {"Full_Name": "Employee_Name"}
    updated_df = rename_columns(sample_df, mapping)

    assert "Employee_Name" in updated_df.columns
    assert "Full_Name" not in updated_df.columns


# Test 2 (Negative): التأكد من رمي KeyError إذا كان العمود المراد تعديله غير موجود
def test_rename_columns_missing_column(sample_df):
    invalid_mapping = {"Non_Existing_Column": "New_Name"}

    with pytest.raises(KeyError):
        rename_columns(sample_df, invalid_mapping)


# Test 3 (Edge Case / Validation): فحص دالة التحقق من الأعمدة بوجود عمود صح وعمود مفقود
def test_check_columns_exist_edge_case(sample_df):
    columns_to_check = ["Employee_ID", "Ghost_Column"]
    all_exist, missing_cols, results = check_columns_exist(
        sample_df, columns_to_check
    )

    assert all_exist is False
    assert "Ghost_Column" in missing_cols
    assert "Employee_ID" not in missing_cols
    assert results["Ghost_Column"] is False
    assert results["Employee_ID"] is True
    