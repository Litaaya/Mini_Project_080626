import pandas as pd
import pytest
# Giả sử file code của em tên là jobtitle_normalize.py
from src.transform.job_title_normalize import (
    clean_job_title,
    classify_job_title,
    job_title_normalize,
    remove_accents,
)


class TestTextPreprocessing:

    def test_remove_accents(self):
        assert remove_accents("Phân tích dữ liệu") == "Phan tich du lieu"
        assert remove_accents("Đà Nẵng & Đống Đa") == "Da Nang & Dong Da"
        assert remove_accents("Kỹ sư phần mềm") == "Ky su phan mem"

    @pytest.mark.parametrize(
        "raw_title, expected",
        [
            (None, ""),
            ("", ""),
            ("   ", ""),
            ("Senior Data Engineer", "data engineer"),
            (
                "[URGENT] Junior Full-stack Developer (Up to 20M)",
                "full stack developer",
            ),
            (
                "Chuyên viên QA/QC Tester (Kinh nghiệm 2 năm)",
                "qa/qc tester",
            ),
            ("Lập trình viên C# / .NET", "lap trinh vien c# / .net"),
            ("C++ Software Engineer", "c++ software engineer"),
        ],
    )
    def test_clean_job_title_cases(self, raw_title, expected):
        assert clean_job_title(raw_title) == expected


class TestJobClassification:

    @pytest.mark.parametrize(
        "raw_title, expected_category",
        [
            (None, "Unknown"),
            ("", "Unknown"),
            ("Senior Business Analyst (IT BA)", "Business Analyst"),
            ("ETL Developer / Data Pipeline", "Data Engineer"),
            ("BI Analyst / Phân tích dữ liệu", "Data Analyst"),
            ("AI Engineer (Machine Learning)", "Data Scientist / AI"),
            ("DevOps / Cloud Architect", "DevOps / Cloud / SRE"),
            ("Lập trình viên ReactJS / Frontend", "Frontend Developer"),
            ("Java / Python Backend Engineer", "Backend Developer"),
            ("Automation Tester (QC Engineer)", "QA / Tester"),
            ("Mobile Developer (Flutter / iOS)", "Mobile Developer"),
            ("Business Development Executive", "Other"),
            ("Kế toán trưởng / Chief Accountant", "Other"),
        ],
    )
    def test_classify_job_title_cases(self, raw_title, expected_category):
        assert classify_job_title(raw_title) == expected_category


class TestJobTitleNormalizeDataFrame:

    def test_missing_column_raises_key_error(self):
        df_invalid = pd.DataFrame({"company": ["Company A"]})
        with pytest.raises(KeyError, match="Missing required column"):
            job_title_normalize(df_invalid)

    def test_no_input_mutation(self):
        df_raw = pd.DataFrame({"job_title": ["Senior Data Engineer"]})
        df_backup = df_raw.copy()

        df_result = job_title_normalize(df_raw)

        pd.testing.assert_frame_equal(df_raw, df_backup)
        assert "clean_job_title" not in df_raw.columns
        assert "normalized_job_title" not in df_raw.columns

        assert "clean_job_title" in df_result.columns
        assert "normalized_job_title" in df_result.columns

    def test_dataframe_integration(self):
        df_raw = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "job_title": [
                    "Senior Data Engineer (Up to 2000 USD)",
                    "Lập trình viên ReactJS",
                    "Business Development Specialist",
                    None,
                ],
            }
        )

        df_result = job_title_normalize(df_raw)

        assert df_result["clean_job_title"].tolist() == [
            "data engineer",
            "lap trinh vien reactjs",
            "business development specialist",
            "",
        ]

        assert df_result["normalized_job_title"].tolist() == [
            "Data Engineer",
            "Frontend Developer",
            "Other",
            "Unknown",
        ]