import unittest
try:
    from services.assess_risk import RiskAssessor
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.assess_risk import RiskAssessor


class TestPortfolioCreator(unittest.TestCase):

    def setUp(self) -> None:
        self.CustomerID = 1001
        self.q1_answer = '80%'
        self.q2_answer = 'Between 5 and 10 years'
        self.q3_answer = 'Pension'
        self.q4_answer = 'No'

    def test_get_risk_level(self):
        ra_obj = RiskAssessor()
        result = ra_obj.get_risk_level(q1_answer=self.q1_answer,
                                       q2_answer=self.q2_answer,
                                       q3_answer=self.q3_answer,
                                       q4_answer=self.q4_answer)
        true_output = 1
        assert result == true_output


    def test_run(self):
        ra_obj = RiskAssessor()
        q1_answer = '27'
        q2_answer = 'Between 5 and 10 years'
        q3_answer = 'Pension'
        q4_answer = 'Save extra for university'
        result = ra_obj.get_risk_level(q1_answer=q1_answer,
                                       q2_answer=q2_answer,
                                       q3_answer=q3_answer,
                                       q4_answer=q4_answer)
        print(result)

if __name__ == '__main__':
    unittest.main()