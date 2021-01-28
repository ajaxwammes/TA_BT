class ImpactCalculator:

    def __init__(self,environment_org):
        self.environment = environment_org

    def quantified_impact(self):
        co2_reduction = sum(self.environment['No_stocks']*self.environment['Co2'])
        electricity_reduction = sum(self.environment['No_stocks']*self.environment['kWh'])
        clean_water = sum(self.environment['No_stocks']*self.environment['liter'])
        recycled = sum(self.environment['No_stocks'] * self.environment['Co2'])
        print('Co2 reduction (KG): ',co2_reduction)
        print('Electricity reduction (kWh): ', electricity_reduction)
        print('Clean water produced (liters): ', clean_water)
        print('Materials recycled (tonnes): ', recycled)