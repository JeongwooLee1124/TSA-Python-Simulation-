from unittest import TestCase, main
from ServerEvent import ServerEvent


class TestServerEvent(TestCase):

    def test_ServerEventValues(self):
        self.assertTrue('SERVICE_COMPLETION' in ServerEvent.__members__)
        self.assertTrue('SERVER_DOWN' in ServerEvent.__members__)
        self.assertTrue('SERVER_UP' in ServerEvent.__members__)

        self.assertEqual(3, len(ServerEvent.__members__))


if __name__ == '__main__':
    main(verbosity=2)
