import pytest
import pandas as pd
from src.transform.validator import validate_records


class TestValidateRecords:
    @pytest.fixture
    def sample_dataframe(self):
        data = {
            "created_date": ["8/1/2023", "invalid_date", "8/2/2023", "cái gì đó ở đây"],
            "company": ["Công ty A", "", "Công ty C", "Không phải công TY b   "],
            "salary": ["10 - 20 triệu", "10 triệu", "20 - 10 triệu", "Hai mươi tám Euro"],
            "address": ["Hà Nội", "Đà Nẵng", "", ""],
            "time": ["Còn 9 ngày", "Còn 5 ngày", "Hết hạn", ""],
            "job_url": [
                "https://www.topcv.vn/job/1",
                "http://invalid-url.com",
                "https://www.topcv.vn/job/3",
                "https://www.topcv.vn/job/4"
            ],
        }

        return pd.DataFrame(data)

    def test_validate_records_split_correctly(self, sample_dataframe):
        valid_df, dlq_df = validate_records(sample_dataframe)

        assert len(valid_df) == 1
        assert valid_df.iloc[0]["company"] == "Công ty A"

        assert len(dlq_df) == 3

        assert len(valid_df) + len(dlq_df) == len(sample_dataframe)