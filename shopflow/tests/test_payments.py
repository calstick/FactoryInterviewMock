from app.services.payments import process_apple_pay


def test_process_apple_pay_approves_valid_mock_token():
    result = process_apple_pay(42.50, "mock_apple_pay_success")

    assert result["approved"] is True
    assert result["authorization_id"] is not None
    assert result["reason"] is None


def test_process_apple_pay_declines_invalid_mock_token():
    result = process_apple_pay(42.50, "not-a-valid-mock-token")

    assert result["approved"] is False
    assert result["authorization_id"] is None
    assert result["reason"] == "invalid_token"


def test_process_apple_pay_declines_empty_mock_token():
    result = process_apple_pay(42.50, "")

    assert result["approved"] is False
    assert result["authorization_id"] is None
    assert result["reason"] == "invalid_token"
