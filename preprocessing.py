# -*- coding: utf-8 -*-
#*****************************************************************************
#************************************* 1 *************************************
#*****************************************************************************

#*************************** 1.1 DATA PREPROCESSING **************************
#***
#1.1.1 Create a single dataframe
#***
df = lob.merge(engage, on = 'Customer Identity')
df = df.drop(columns=['index_x', 'index_y'])
df = df.reset_index()
df = df.drop(columns=['index'])

#initial number of rows: 10296


#***
#1.1.2 Column rename
#***
df.columns = ['CID', 'Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium', 'FirstPYear', 'BirthYear', 'Educ', 'MonthSalary', 'LivingArea', 'Children', 'CustMonVal', 'ClaimsRate']

#***
#***1.1.3 Get some basic notions about the data***
#***

##Birth Year/Age
df['Age'] = 2016 - df['BirthYear']
df['Age'].describe()
#min: 15, max: 988

#Keep age, discard birth year
#Look for outliers, define thresholds, under 18 should not be considered valid


##Create "years as customer" to replace FirstPYear

##Education
df['Educ'].drop_duplicates()
#None, 1 - Basic, 2 - High School, 3 - BSc/MSc, 4 - PhD
#Convert to numerical scale

##Children
df['Children'].drop_duplicates()
df['Children'].isna().sum()
#21 of the 10296 are NaN (0.2%)
df.loc[df['Children']==0, 'Children'].count()
#3034 of the 10296 don't have children
df.loc[df['Children']==1, 'Children'].count()
#7262 of the 10296 have children


##Premiums
df['Motor Premium'].describe()
df['Household Premium'].describe()
df['Health Premium'].describe()
df['Life Premium'].describe()
df['Work Premium'].describe()
#it is difficult to analyze without proper business background, but using common sense,
#...max values are too high for an annual premium




##First Premium Year
df['FirstPYear'].describe()
df['FirstPYear'].drop_duplicates()
#it is possible to identify some errors, namely an impossibly high value and NaN

##MonthSalary
df['MonthSalary'].describe()
#Not enough to identify potential errors

##LivingArea
df['LivingArea'].drop_duplicates()
#Missing values present

##CustMonVal
#(annual profit from the customer) X (number of years that they are a customer) - (acquisition cost) 
df['CustMonVal'].describe()
df.loc[pd.isnull(df['CustMonVal'])]
#outliers here are difficult to classify as errors, due to the nature of this variable. A further analysis is needed

##ClaimsRate
#Amount paid by the insurance company (€)/ Premiums (€)  
#Note: in the last 2 years Motor 
df['ClaimsRate'].describe()
df.loc[pd.isnull(df['ClaimsRate'])]
#As in CustMonVal, it is difficult to classify outliers as errors, further analysis is needed

##Checking if there are missing ids
np.isnan(df['CID']).drop_duplicates()
#no missing ids





##By this basic analysis, it is possible to:
#- Exclude the variable "BirthYear", given the new variable "Age" is enough
#- Understand that "Educ" should be transformed to a numerical variable, containing only 0, 1, 2, 3, 4
#- A strategy should be defined for "Children", in order to deal with missing values, enabling the transformation to a Boolean variable
#- There should be further analysis to the Premium variables. This should not be aggregated into only one variable for every scenario,
#(...) as information about different insurance policy types is essential for some clustering scenarios
#- It is necessary to clean, perform coherence verification and further analyze "FirtPYear", "MonthSalary", CustMonVal" and "ClaimsRate"
#- Variables with possible discrepancies identified: Age, FirstPYear







#***
#***1.1.4 Coherence/discrepancy verification***
#***
#Strategy changed. Missing values treatment was first, but in the process it was discovered
#that, to use some missing values treatment techniques, data should already be somewhat free
#of inconsistencies. Basically, missing values treatment can be affected by coherence verification
#while the latter is not affected by the first

##FirstPYear before BirthYear
cvFirstPYearBirthYear = df.loc[~pd.isnull(df['FirstPYear'])]
cvFirstPYearBirthYear = cvFirstPYearBirthYear.loc[~pd.isnull(cvFirstPYearBirthYear['BirthYear'])]

cvFirstPYearBirthYear.loc[cvFirstPYearBirthYear['FirstPYear']<cvFirstPYearBirthYear['BirthYear']]
#1997 of 10252 (19.48% of non FirstPYear or BirthYear null observations)
#1997 of 10296 (19.4% of all observations)


##Age < 18 or Age > 120
#Year of db is 2016
#BirthYear > 1998 or BirthYear < 1896

#------ <18 -------------
cvBirthYear = df.loc[~pd.isnull(df['BirthYear'])]
cvBirthYearM18 = cvBirthYear.loc[cvBirthYear['BirthYear'] > 1998]
#116 of 10279 (1.129% of non BirthYear null observations)
#116 of 10296 (1.127% of all observations)

cvBirthYearM18['Children'].sum()/116

#An analysis of this observations reveals that:
#- All have Educ = 1
#- 75% has children
#- All have salary
#- All have insurance policies in each category (including motor, household and work compensation)
#(- and all have age <18)

#The data suggests that these are customers, but:
#- <18 don't have insurance
#- Not expected that <18 have children, salary, car and house

#This and the analysis from FirstPYear before BirthYear may suggest that the variable age is not to be trusted
#Although variables originated from user imput are less trustable that variables derived from system generated values,(...)
#(...) age is considerably important in the insurance context, given that age is considered not only in the calculation of (...)
#(...) insurance premiums but also in the decision of granting insurance to the customer.
#Nevertheless, tt is not possible, without more data and deeper context from the business, to clearly point out (...)
#that the problem is totally due to the variable age, given that FirstPYear also has discrepancies (missing values (...)
#(...) and non-date/impossible date values), which denotes the existence of errors in this variable, further (...)
#(...) confirming that there is no clear way to say that the variable age is responsible for every discrepancy.
#This reveals a low degree of trustability of the dataset provided, which inevitably confers a lower (...)
#(...) degree of trustability to the analysis that intended, while also considerably limiting (...)
#(...) the diversity and completeness of the said analysis, since age segmentation could be crucial (...)
#(...) to provide a complete analysis.
#Despite being a highly important dimension of the analysis, it is not possible to trust in the age (...)
#(...) variable, since there is not enough information to confirm that other age/birthdate values (...)
#(...) are not incorrect too.
#This is bad, really bad, and needs further scrutiny in the report.


cvBirthYear['BirthYear'].loc[cvBirthYear['BirthYear'] > 1998].drop_duplicates()
#BirthYear: 2000, 1999, 2001
#16, 17, 15 yo

#------- >120 ------------
cvBirthYear.loc[cvBirthYear['BirthYear'] < 1896]
#1 of 10279 (0.01 % of non BirthYear null observations)
#1 of 10296 (0.01 % of all observations)
#BirthYear: 1028
#988 yo


removedOrModified = {'dataWithAge': df.copy(deep=True)}

df = df.drop(['Age', 'BirthYear'], axis=1)


##Premium Values > YearlySalary
#Creating of YearlySalary var
df['YearlySalary'] = df['MonthSalary']*14

nullPremiumsAsZero = df.copy(deep=True)
nullPremiumsAsZero['Motor Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Household Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Health Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Life Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Work Premium'].fillna(0, inplace=True)
nullPremiumsAsZero = nullPremiumsAsZero.loc[~nullPremiumsAsZero['YearlySalary'].isna()]

#Creation of TotalPremiums var
df['TotalPremiums'] = nullPremiumsAsZero['Motor Premium'] + nullPremiumsAsZero['Household Premium'] + nullPremiumsAsZero['Health Premium'] + nullPremiumsAsZero['Life Premium'] + nullPremiumsAsZero['Work Premium'] 


nullPremiumsAsZero.loc[nullPremiumsAsZero['YearlySalary']<nullPremiumsAsZero['TotalPremiums']]
#1 of 10260 (0.01 % of non YearlySalary null observations)
#1 of 10296 (0.01 % of all observations)
#Health Premium is extremely high (28272), Total Premiums is 2x YearlySalary

#This shows, once again, the incompleteness of the db. This observation reveals a scenario which is (...)
#(...) possible, depending on the context, in a variety of forms. For example, this Health policy (...)
#(...) could be of a family, whose spouse of the policy taker has a much higher income. Since there (...)
#(...) is no information about the nature of the customer (company or particular customer), this could (...)
#(...) also be a health policy of a company for all the employees, assuming that:
#There are real cases of insurance companies that require the exact same variables for companies or particular(...)
#(...) customers, with no stated practice for the filling of some variables that are not applicable for company customers.
#In this (real) cases, children is marked as 0, income is filled with profit, education is not filled, etc.
#Nevertheless, and despite not removing this observation, it will be appended to the(...)
#(...) removedOrModified dictionary, for further analysis.











#***
#***1.1.5 Variable transformations and Missing Values Treatment***
#***
#"Firstly, understand that there is NO good way to deal with missing data"
#https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4



##Removing the variable "BirthYear"
df = df.drop(columns=['BirthYear'])

##Assessing the percentage of missing values by observation
df = df.reset_index()
df = df.drop(columns=['index'])

missingValuesForRows = df.isnull().sum(axis=1)
missingValuesForRows = pd.DataFrame(missingValuesForRows)
missingValuesForRows.drop_duplicates()

#13 variables (excluding customer id)
#for rows with 3 or 4 variables with missing values, the said row has 23% or 30% of missing values
#as said in class, this threshold could be enough to exclude this observations (above 20% of missing values, consider excluding the observation)
missingValuesForRows.loc[missingValuesForRows[0]==3].count()     
missingValuesForRows.loc[missingValuesForRows[0]==4].count()
#3 observations with 3 missing values (0.03% of total observations)
#12 observations with 4 missing values (0.12% of total observations)     

missingValuesForRows.loc[missingValuesForRows[0]==3].index
#indexes 296, 488, 4423    
missingValuesForRows.loc[missingValuesForRows[0]==4].index
#indexes 862, 1133, 3165, 4022, 4113, 4271, 5983, 6439, 6614, 8585, 9398, 9788


df.loc[df.index.isin(missingValuesForRows.loc[missingValuesForRows[0]==3].index)]
#no pattern identified
df.loc[[296]] #FirstPYear, LivingArea, Children
df.loc[[488]] #Motor Premium, Life Premium, MonthSalary (has Health and Work Premium)
df.loc[[4423]] #Work Premium, FirstPYear, Educ

df.loc[df.index.isin(missingValuesForRows.loc[missingValuesForRows[0]==4].index)]
df.loc[[862]]  #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[1133]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[3165]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[4022]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[4113]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[4271]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[5983]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[6439]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[6614]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[8585]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[9398]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
df.loc[[9788]] #Motor Premium, Health Premium, Life Premium, Work Premium (Household Premium = 0) => No premium in any category
#Is there a pattern here (in the observations with 4 missing values)?
#Investigate if missing values in premium variables can be considered 0 (no insurance policy contracted in that category)
#Decide what to do with the 3 observations with 3 missing values, as they are loose observations (no pattern observed)


##Assessing the percentage of missing values by variable
missingValuesForVar = df.isna().sum()/10296*100
missingValuesForVar.loc[missingValuesForVar>0] 
#Life Premium is the only variable with more than 1% of missing values (1.01%)
#No reason to exclude any variable






##
#Missing values treatment
##
#First treat observations with 3 or 4 missing values (because it's only possible to treat them if they are first)
#Then treat premiums
#Then treat variables with no identified discrepancies (because, if other vars need to 
#use this vars for prediction, they have no missing values and no identified discrepancies)
#Then treat variables with identified discrepancies

##Treating observations with 3 or 4 missing values
#Treatment: Removal
removedOrModified['threeMissingValuesInSameObservation'] = df.loc[df.index.isin(missingValuesForRows.loc[missingValuesForRows[0]==3].index)].copy(deep=True)
removedOrModified['fourMissingValuesInSameObservation'] = df.loc[df.index.isin(missingValuesForRows.loc[missingValuesForRows[0]==4].index)].copy(deep=True)

#For CID 488, it is important to note that 2 of the 3 missing values are from Premium variables, that are going to be treated after according
#with specific assumptions. For this reason, this record is not going to be excluded just yet.
df = df.drop([296, 4423])
df = df.loc[~df.index.isin(missingValuesForRows.loc[missingValuesForRows[0]==4].index)]



##Premiums
#In order to avoid hindering the analysis, missing values in premiums should be considered as 0
#since that there is no information available to explain the existence of missing values, and the data
#available is not enough to predict premium values, given the uniqueness associated with each person
#and the fact that customers can have policies with other insurance companies (predictions could point out
#that customer A might have the value X for certain premium, given other attributes, but it is not safe to
#assume that customer A doesn't have indeed that X for that premium in other insurance company)
#So, the safest assumption to make, and trying to avoid removing observations, is that missing information about
#premium values is due to that premium value being 0 (non existent)

correctedObservations_premiums = df.loc[pd.isnull(df['Motor Premium'])]
correctedObservations_premiums.append(df.loc[pd.isnull(df['Household Premium'])])
correctedObservations_premiums.append(df.loc[pd.isnull(df['Health Premium'])])
correctedObservations_premiums.append(df.loc[pd.isnull(df['Life Premium'])])
correctedObservations_premiums = correctedObservations_premiums['CID'].drop_duplicates()
correctedObservations_premiums.count()
#22 observations are going to be corrected due to missing values in premium variables 
#(not counting the 13 observations already excluded that had missing values in premium variables)

removedOrModified['motorPremiumNull'] = df.loc[~df.index.isin(df.loc[pd.isnull(df['Motor Premium'])].index)].copy(deep=True) 
removedOrModified['householdPremiumNull'] = df.loc[~df.index.isin(df.loc[pd.isnull(df['Household Premium'])].index)].copy(deep=True)  
removedOrModified['healthPremiumNull'] = df.loc[~df.index.isin(df.loc[pd.isnull(df['Health Premium'])].index)].copy(deep=True)  
removedOrModified['lifePremiumNull'] = df.loc[~df.index.isin(df.loc[pd.isnull(df['Life Premium'])].index)].copy(deep=True)  


df['Motor Premium'].fillna(0, inplace=True)
df['Household Premium'].fillna(0, inplace=True)
df['Health Premium'].fillna(0, inplace=True)
df['Life Premium'].fillna(0, inplace=True)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#falta work premium


##Children
#convert to a boolean variable
#To minimize the data loss (despite being only 0.2% of all observations):
#- It is more plausible to assume that, in case of missing value, there is no children

removedOrModified['noChildrenInfo'] = df.loc[pd.isnull(df['Children'])].copy(deep=True)
df['Children'].fillna(0, inplace=True)

df['Children'] = df['Children'].astype(bool)


##Living Area
df['LivingArea'].isna().sum()
#No missing values

##MonthSalary
df['MonthSalary'].isna().sum()
#-----------------decide what to do---------------------


##FirstPYear
df['FirstPYear'].isna().sum()
#30 of the 10296 are NaN (0.29%)
df.loc[df['FirstPYear'].isna()]
#-----------------decide what to do---------------------


##Age
df['Age'].isna().sum()
#-----------------decide what to do---------------------


##CustMonVal
#No missing values

##ClaimsRate
#No missing values


#---------------------------------------------------------------------------
##Transform missing values in "Educ" to "0" and convert "Educ" to a numerical variable
#Since KNN is the chosen method to deal with missing values, some precautions are necessary:
#- KNN will use other variables, so missing values and discrepancies in those variables must be dealt with beforehand


#Missing values are now marked with 0
df.loc[df['Educ'].isnull(), 'Educ'] = "0"

for ind, i in enumerate(df['Educ'].drop_duplicates(), start=0):
    df.loc[df['Educ']==i, 'Educ'] = int(i[0])


df.loc[df['Educ']==0, 'Educ'].count()
#17 of the 10296 are NaN (0.16%)
#Imputation of categorical variables:
#Missing values can be treated as a separate category by itself. We can create another category for the missing values and use them as a different level. This is the simplest method.
#or
#KNN (K Nearest Neighbors) --> Consider age and monthsalary
#https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4
#Use KNN


#KNN
#---------------------------------------------------------------------------









#manipulate existing variables
#create new variables
