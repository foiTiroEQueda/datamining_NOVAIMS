# -*- coding: utf-8 -*-

list(df)

#Division of variables in Lob and Engage
VarsEngage = df[['YearsAsCustomer', 'Educ', 'AnnualSalary', 'LivingArea', 'Children', 'CustMonVal',]].copy(deep=True)
VarsLob = df[['Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium']].copy(deep=True)


