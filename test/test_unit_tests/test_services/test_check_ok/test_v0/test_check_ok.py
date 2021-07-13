from models.check_ok.v0.model import CheckOk
from services.check_ok.v0.check_ok import check_ok_response


def test_check_ok_response_works():
    response: CheckOk = check_ok_response()
    assert response.version == 0
    assert response.status == 200
