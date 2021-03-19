import unittest
try:
    from services.assess_risk import RiskAssessor
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.assess_risk import RiskAssessor


class TestPortfolioCreator(unittest.TestCase):

    def setUp(self) -> None:
        self.q1_answer = 55
        self.q2_answer = 27
        self.q3_answer = "I don't know yet"


if __name__ == '__main__':
    unittest.main()