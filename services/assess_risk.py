from services.utils import risk_assessment

class RiskAssessor:

    def __init__(self):
        self.status = None

    def get_risk_level(self, q1_answer, q2_answer, q3_answer, q4_answer):
        score_q1 = risk_assessment.q1[q1_answer]
        score_q2 = risk_assessment.q2[q2_answer]
        score_q3 = risk_assessment.q3[q3_answer]
        score_q4 = risk_assessment.q4[q4_answer]
        total_score = score_q1 + score_q2 + score_q3 + score_q4
        res_key, res_val = min(risk_assessment.risk.items(), key=lambda x: abs(total_score - x[1]))
        return res_key


