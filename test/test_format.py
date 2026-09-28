from pathlib import Path
import pytest
from src.format import return_path,process_all_lines,format_all,save_formatted_text

def test_return_path(tmp_path):
    test_path = tmp_path / "example_01.md"
    # assert return_path(test_path).exists() == True# 中身作ってないので除外（必ず検証エラーになる
    assert return_path(test_path) == Path(test_path)

# @pytest.mark.parametrize(
#         "input,expected",[
#             pytest.param("sample_03.md","expected_03.md",id = "sample_03")
#         ]
# )
# def test_process_all_lines(input,expected):
#     input_path = return_path("test/samples/sample_03.md")
#     expected_path = return_path("test/samples/expected_03.md")
    
#     expected_output = []

#     with open(expected_path,mode="r",encoding="utf-8") as content:
#         for line in content:
#             expected_output.append(line.removesuffix("\n"))

#     assert process_all_lines(input_path) == expected_output
            





@pytest.mark.parametrize(
        "input,expected",
        [
            pytest.param("## title","""
<br>
<br>
## title
<br>
<br>
""",id = "h2_half_blank"),

            pytest.param("##　title","""
<br>
<br>
## title
<br>
<br>
""",id= "h2_full_blank"),

            pytest.param("title","""title""",id="no_h2"),

            pytest.param("title ## ","""title ## """,id="h2_inside"),

            pytest.param("### title","""### title""",id = "h3")
        ]
)
def test_format_all(input,expected):
    assert format_all(input) == expected

@pytest.fixture
def prepare_formatted_text()->list[str]:
     return ["foo","bar","hoge"]


def test_save_formatted_text(tmp_path,prepare_formatted_text):
    target_path = tmp_path / "sample.01.md"
    save_formatted_text(target_path,prepare_formatted_text)


def test_save_formatted_text_no_fixture(tmp_path):
    target_path = tmp_path / "sample.01.md"
    formatted_text = ["foo","bar","hoge"]
    save_formatted_text(target_path,formatted_text)
    assert target_path.exists() == True
    assert target_path.read_text(encoding="utf-8") == "\n".join(formatted_text)

def test_save_formatted_text_no_fixture_ci_check_fail(tmp_path):
    target_path = tmp_path / "sample.01.md"
    formatted_text = ["foo","bar","hoge"]
    save_formatted_text(target_path,formatted_text)
    assert target_path.exists() == True
    assert target_path.read_text(encoding="utf-8") == formatted_text

# @pytest.mark.parametrize(
#         "input,expected",[
#             pytest.param("test/samples/sample_03.md","expected_03.md",id = "sample_03")
#         ]
# )
def test_all_pipeline(tmp_path):
    input_path = return_path("test/samples/sample_01.md")
    output_path = tmp_path / "sample_01.md"
    expected_output_path = return_path("test/samples/expected_01.md")
    formatted_text = process_all_lines(input_path)
    save_formatted_text(output_path,formatted_text)
    assert output_path.read_text(encoding="utf-8",newline = "") == expected_output_path.read_text(encoding="utf=8",newline ="")
