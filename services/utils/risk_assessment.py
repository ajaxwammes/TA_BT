#question: how much % of my wealth I want to invest?
q1 = {'20%' : (4),
      '40%' : (3),
      '60%' : (2),
      '80%' : (1),
      '100%' : (0)
      }

#question: what is my investment horizon?
q2 = {'Shorter than 5 years' : (0),
      'Between 5 and 10 years' : (1),
      'Between 10 and 15 years' : (2),
      'Longer than 15 years' : (3),
      "I don't know" : (1.5)
      }

#question: why am I investing?
q3 = {'Make the most out of my savings' : (1),
      'Pension' : (2),
      'Save for university' : (0),
      "I don't know" : (1.5)
      }

#question: do I consider recurring deposits?
q4 = {'Yes' : (1),
      'No' : (0)
      }

risk = {
      0 : (1),
      1 : (3),
      2 : (5),
      3 : (7),
      4 : (9)
      }