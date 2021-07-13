from models.check_ok.v0.model import CheckOk

check_ok_with_default_values: CheckOk = CheckOk()


class TestDefaults:
    def test_version_is_correct(self):
        assert check_ok_with_default_values.version == 0

    def test_http_response_is_ok(self):
        assert check_ok_with_default_values.status == 200
