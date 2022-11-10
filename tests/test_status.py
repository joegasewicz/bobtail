from bobtail.status import Status


class TestStatus:

    def test_get(self):
        s = Status()
        result = s.get(200)
        expected = "200 OK"
        assert result == expected
