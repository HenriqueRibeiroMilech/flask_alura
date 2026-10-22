from utils import format_currency

def test_format_currency_with_decimal():
    input_value = 59.9
    result = format_currency(input_value)
    assert result == "59,90"