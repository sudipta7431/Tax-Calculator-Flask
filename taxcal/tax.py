#OLD TAX SLAB
class Oldregime:
    def __init__(self,income):
        self.income = income
        self.tax = 0
    #TAX SLAB
    #0 - 250000
    def tax_less_2_5(self,income):
        self.tax += income * 0
        return self.tax
    #250000 - 500000
    def tax_less_5(self,income):
        self.tax += self.tax_less_2_5(250000)
        self.tax += (income - 250000) * 0.05
        return self.tax
    #500000 - 1000000
    def tax_less_10(self,income):
        self.tax += self.tax_less_5(500000)
        self.tax += (income - 500000) * 0.2
        return self.tax
    #1000000 - more
    def tax_grater_10(self,income):
        self.tax += self.tax_less_10(1000000)
        self.tax += (income - 1000000) * 0.3
        return self.tax

    def calculate(self):
        if self.income <= 500000:
            return 0
        elif self.income <= 1000000:
            return self.tax_less_10(self.income)
        else:
            return self.tax_grater_10(self.income)

#NEW TAX SLAB
class Newregime:
    def __init__(self,income):
        self.income = income
        self.tax = 0
    #TAX SLAB
    #0 - 300000
    def tax_less_3(self,income):
        self.tax += income * 0
        return self.tax
    #300001 - 600000
    def tax_less_6(self,income):
        self.tax += self.tax_less_3(300000)
        self.tax += (income - 300000) * 0.05
        return self.tax
    #600001 - 900000
    def tax_less_9(self,income):
        self.tax += self.tax_less_6(600000)
        self.tax += (income - 600000) * 0.1
        return self.tax
    #900001 - 1200000
    def tax_less_12(self,income):
        self.tax += self.tax_less_9(900000)
        self.tax += (income - 900000) * 0.15
        return self.tax
    #1200001 - 1500000
    def tax_less_15(self,income):
        self.tax += self.tax_less_12(1200000)
        self.tax += (income - 1200000) * 0.2
        return self.tax
    #1500000 - more
    def tax_grater_15(self,income):
        self.tax += self.tax_less_15(1500000)
        self.tax += (income - 1500000) * 0.3
        return self.tax

    def calculate(self):
        if self.income <= 500000:
            return 0
        elif self.income <= 600000:
            return self.tax_less_6(self.income)
        elif self.income <= 900000:
            return self.tax_less_9(self.income)
        elif self.income <= 1200000:
            return self.tax_less_12(self.income)
        elif self.income <= 1500000:
            return self.tax_less_15(self.income)
        else:
            return self.tax_grater_15(self.income)


def return_tax( gross_income, basic_sal, insurance_premium, House_ln_principal, House_ln_intarest, helth_ins, Donation, nps):
    old_tax = new_tax = old_taxable_income = 0
    pf = basic_sal*(12/100)
    c80 = (pf + insurance_premium + House_ln_principal + nps)
    #print(f'{pf} + {insurance_premium} + {House_ln_principal}+ {nps} = {c80}')
    d80 = (Donation + helth_ins+House_ln_intarest)
    #print(f'{Donation} + {helth_ins}+{House_ln_intarest} = {d80}')
    hra = basic_sal*(40/100)
    deduction = c80 + d80 + hra

    #old
    if gross_income <= 500000:
        old_tax = 0
    else:
        old_taxable_income = gross_income - deduction - 50000
        
    obj1 = Oldregime(old_taxable_income)
    if old_taxable_income <= 500000:
        old_tax = 0
    else:
        old_tax = obj1.calculate()
    
    
    obj2 = Newregime(gross_income - 50000)
    #new
    if gross_income <= 750000:
        new_tax = 0
    else:
        new_tax = obj2.calculate()

    return (old_tax * 1.04),(new_tax * 1.04),pf,c80,d80,hra,deduction

    #data_list = [old_tax,new_tax,pf,c80,d80,hra,deduction]


if __name__ == '__main__':
    gross_income = int(input())
    basic_sal = int(input())
    helth_ins = int(input())
    insurance_premium = int(input())
    House_ln_principal = int(input())
    House_ln_intarest = int(input())
    Donation = int(input())
    nps = int(input())

    print(return_tax(gross_income, basic_sal, insurance_premium, House_ln_principal, House_ln_intarest, helth_ins, Donation, nps))
    
    

