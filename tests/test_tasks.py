from green_lane.rules.tasks import detect_task


def test_detect_table_lookup():
    assert detect_task("show me the table") == "table_lookup"


def test_detect_math_units():
    assert detect_task("calculate unit ratio") == "math_units"


def test_detect_extractive():
    assert detect_task("what is sterile changeover?") == "extractive"


