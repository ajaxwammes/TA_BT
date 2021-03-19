from services.configs import risk_questions

class RiskAssessor:

    def __init__(self):
        self.status = None

    def get_risk_level(self, q1_answer, q2_answer, q3_answer):
        score_q1 = risk_questions.q1[q1_answer]
        score_q2 = risk_questions.q2[q2_answer]
        score_q3 = risk_questions.q3[q3_answer]
        total_score = score_q1 + score_q2 + score_q3
        print(total_score)
        res_key, res_val = min(risk_questions.items(), key=lambda x: abs(total_score - x[1]))
        return res_key


