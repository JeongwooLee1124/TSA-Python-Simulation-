from unittest import TestCase, main
from ServerState import ServerState


class TestServerState(TestCase):

    def test_ServerStateValues(self):
        self.assertTrue('AVAILABLE' in ServerState.__members__)
        self.assertTrue('BUSY' in ServerState.__members__)
        self.assertTrue('OOS' in ServerState.__members__)
        self.assertTrue('PENDING_OOS' in ServerState.__members__)
        self.assertTrue('INVALID' in ServerState.__members__)

        self.assertEqual(5, len(ServerState.__members__))


if __name__ == '__main__':
    main(verbosity=2)
