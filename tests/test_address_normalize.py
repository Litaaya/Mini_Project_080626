import pandas as pd
import pytest
from src.transform.address_normalize import address_normalize, format_address

class TestFormatAddress:

    def test_empty_and_null_values(self):
        assert format_address(None) == ""
        assert format_address("") == ""
        assert format_address("   ") == ""
        assert format_address(pd.NA) == ""

    def test_standard_city_district_pairs(self):
        raw_1 = "Hà Nội: Đống Đa"
        assert format_address(raw_1) == "Hà Nội - Đống Đa"

        raw_2 = "Hồ Chí Minh: Tân Bình: Hà Nội: Ba Đình"
        assert format_address(raw_2) == "Hồ Chí Minh - Tân Bình; Hà Nội - Ba Đình"

    def test_multiple_cities_without_districts(self):
        raw = "Hà Nội: Hồ Chí Minh: Đà Nẵng"
        assert format_address(raw) == "Hà Nội; Hồ Chí Minh; Đà Nẵng"

    def test_single_city_only(self):
        assert format_address("Bình Dương") == "Bình Dương"
        assert format_address("Thành phố Hà Nội") == "Thành phố Hà Nội"

    def test_city_with_multiple_districts(self):
        raw = "Hà Nội: Cầu Giấy, Nam Từ Liêm"
        assert format_address(raw) == "Hà Nội - Cầu Giấy, Nam Từ Liêm"

    def test_dirty_spaces_and_extra_colons(self):
        raw = "  Hồ Chí Minh :  Tân Bình  : : Hà Nội : Ba Đình  "
        assert format_address(raw) == "Hồ Chí Minh - Tân Bình; Hà Nội - Ba Đình"


class TestAddressNormalizeDataFrame:

    def test_no_input_mutation(self):
        df_raw = pd.DataFrame({"address": ["Hà Nội: Đống Đa"]})
        df_raw_backup = df_raw.copy()
        df_result = address_normalize(df_raw)
        pd.testing.assert_frame_equal(df_raw, df_raw_backup)
        assert "clean_address" not in df_raw.columns
        assert "clean_address" in df_result.columns

    def test_dataframe_integration(self):
        df_raw = pd.DataFrame(
            {
                "id": [1, 2, 3, 4],
                "address": [
                    "Hồ Chí Minh: Tân Bình: Hà Nội: Ba Đình",
                    "Hà Nội: Hồ Chí Minh: Đà Nẵng",
                    "Đà Nẵng",
                    None,
                ],
            }
        )

        df_result = address_normalize(df_raw)

        expected_clean_addresses = [
            "Hồ Chí Minh - Tân Bình; Hà Nội - Ba Đình",
            "Hà Nội; Hồ Chí Minh; Đà Nẵng",
            "Đà Nẵng",
            "",
        ]

        assert df_result["clean_address"].tolist() == expected_clean_addresses