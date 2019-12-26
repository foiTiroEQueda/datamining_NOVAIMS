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
#3013 of the 10296 don't have children
df.loc[df['Children']==1, 'Children'].count()
#7262 of the 10296 have children


##Premiums
df['Motor Premium'].describe()
df['Household Premium'].describe()
df['Health Premium'].describe()
df['Life Premium'].describe()
df['Work Premium'].describe()
#it is difficult to analyze without proper business background




##First Premium Year
df['FirstPYear'].describe()
df['FirstPYear'].drop_duplicates()
#it is possible to identify some errors, namely an impossibly high value and NaN

##MonthSalary
df['MonthSalary'].describe()
#Not enough to identify potential errors

df.loc[df['MonthSalary']<618.33]


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

##Checking if there are duplicated ids
df[df.duplicated(['CID'])]
#no duplicated ids


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


##MonthSalary
#Salaries below the minimum wage are possible, and without context, it is impossible to know (...)
#(...) if this value is a salary (particular customer) or profit (company customer).
#Nevertheless, it is important to analyze each of these cases, in order to determine if this customers (...)
#(...) can be considered in risk for not being able to pay the premiums.
removedOrModified = {'incomeBelowMinimumWage': df.loc[df['MonthSalary']<618.33].copy(deep=True)}



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

removedOrModified['dataWithAge'] = df.copy(deep=True)

df = df.drop(['Age', 'BirthYear'], axis=1)


##Premium Values > YearlySalary

nullPremiumsAsZero = df.copy(deep=True)
nullPremiumsAsZero['Motor Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Household Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Health Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Life Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['Work Premium'].fillna(0, inplace=True)
nullPremiumsAsZero['YearlySalary'] = nullPremiumsAsZero['MonthSalary']*14
nullPremiumsAsZero = nullPremiumsAsZero.loc[~nullPremiumsAsZero['YearlySalary'].isna()]

nullPremiumsAsZero['TotalPremiums'] = nullPremiumsAsZero['Motor Premium'] + nullPremiumsAsZero['Household Premium'] + nullPremiumsAsZero['Health Premium'] + nullPremiumsAsZero['Life Premium'] + nullPremiumsAsZero['Work Premium'] 


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
#In this (real) cases, children is marked as 0, income is filled with profit, education is not filled, etc. (...)
#(...) and the only way to tell what kind of customer is is to check the NIF (not present in this dataset)
#Nevertheless, and despite not removing this observation, it will be appended to the(...)
#(...) removedOrModified dictionary, for further analysis.

removedOrModified['totalPremiumsMuchHigherThanSalary'] = nullPremiumsAsZero.loc[nullPremiumsAsZero['YearlySalary']<nullPremiumsAsZero['TotalPremiums']].copy(deep=True)

##FirstPYear
df.loc[df['FirstPYear']>2016]
#Since the clustering analysis will have a narrow base of observations to work with, it is better (...)
#(...) to exclude this observation, given the identified error and the difficulty of accuratly (...)
#(...) predicting the true value for FirstPYear of this observation
removedOrModified['impossibleFirstPYear'] = df.loc[df['FirstPYear']>2016].copy(deep=True)
df = df.drop([9294])

df['FirstPYear'].max()
#Data indicates that there is not a single insurance policy made after 1998. This is something to check.
#Since we are dealing with aggregated data, this means that there were no new customers since 1998. NOT NECESSARILY
#Is there a new db with more information? Is this an error?

#The company might have given this on purpose, or maybe this is an old db that they though of segmenting
#Calculate years as customer relative to 1998, and not to 2016


##ClaimsRate
#Amount paid by the insurance company (€)/ Premiums (€)  
#(In the last two years)

#Not possible to do coherence verification with the existing data.



#***
#***1.1.5 Variable transformations and Missing Values Treatment***
#***
#"Firstly, understand that there is NO good way to deal with missing data"
#https://towardsdatascience.com/how-to-handle-missing-data-8646b18db0d4




##Assessing the percentage of missing values by observation
df = df.reset_index()
df = df.drop(columns=['index'])

missingValuesForRows = df.isnull().sum(axis=1)
missingValuesForRows = pd.DataFrame(missingValuesForRows)
missingValuesForRows.drop_duplicates()

#12 variables (excluding customer id)
#for rows with 3 or 4 variables with missing values, the said row has 25% or 33% of missing values
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
#Then the rest


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
correctedObservations_premiums = correctedObservations_premiums.append(df.loc[pd.isnull(df['Household Premium'])])
correctedObservations_premiums = correctedObservations_premiums.append(df.loc[pd.isnull(df['Health Premium'])])
correctedObservations_premiums = correctedObservations_premiums.append(df.loc[pd.isnull(df['Life Premium'])])
correctedObservations_premiums = correctedObservations_premiums.append(df.loc[pd.isnull(df['Work Premium'])])
correctedObservations_premiums  = correctedObservations_premiums['CID'].drop_duplicates()
correctedObservations_premiums.count()
#212 of 10282 observations (2%) are going to be corrected due to missing values in premium variables 
#(not counting the 13 observations already excluded that had missing values in premium variables)


removedOrModified['motorPremiumNull'] = df.loc[df.index.isin(df.loc[pd.isnull(df['Motor Premium'])].index)].copy(deep=True) 
removedOrModified['householdPremiumNull'] = df.loc[df.index.isin(df.loc[pd.isnull(df['Household Premium'])].index)].copy(deep=True)  
removedOrModified['healthPremiumNull'] = df.loc[df.index.isin(df.loc[pd.isnull(df['Health Premium'])].index)].copy(deep=True)  
removedOrModified['lifePremiumNull'] = df.loc[df.index.isin(df.loc[pd.isnull(df['Life Premium'])].index)].copy(deep=True)  
removedOrModified['workPremiumNull'] = df.loc[df.index.isin(df.loc[pd.isnull(df['Work Premium'])].index)].copy(deep=True)  

#household has 0 missing values
df['Motor Premium'].fillna(0, inplace=True)
df['Health Premium'].fillna(0, inplace=True)
df['Life Premium'].fillna(0, inplace=True)
df['Work Premium'].fillna(0, inplace=True)



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


##Correlation Matrix for a better understanding 
corrMatrix(df)
#-0.99 correlation between CMV and Claims Rate
#what to do, what to do, what to do


##Educ
#Transform missing values in "Educ" to "0" and convert "Educ" to a numerical variable
#0 - Missing
#1 - Basic
#2 - High School
#3 - BSc/MSc
#4 - PhD --> Goes to 3, and 3 becomes Higher Education

#Missing values are now marked with 0
df.loc[df['Educ'].isnull(), 'Educ'] = "0"

for ind, i in enumerate(df['Educ'].drop_duplicates(), start=0):
    df.loc[df['Educ']==i, 'Educ'] = int(i[0])

del ind, i
df.loc[df['Educ']==4, 'Educ'] = 3

missingEduc = df.loc[df['Educ']==0]
#interesting how the vast majority of records with missing values in Educ have missing values in FirstPYear
#system bug? Assuming that FirstPYear is generated by the system, could be that there was some cause that (...)
#(...) removed FirstPYear and Educ?
#Long shot, but it could be
removedOrModified['noEducInfo'] = missingEduc.copy(deep=True)

#There isn't a good base of variables to predict missing values for educ
#This is a case of Missing at Random, so removing the observations could cause less harm than filling (...)
#(...)them with artificial values, such as mode 

df = df.loc[df['Educ']!=0]


##MonthSalary
#Not knowing if providing salary information is mandatory or not for this insurance company, (...)
#(...) missing values in this variable could be due to people not wanting do disclose that information.
#In this case, it is not wise to remove this observations, given that it could be (...)
#(...) Missing not at Random (MNAR): Two possible reasons are that the missing value depends (...)
#(...) on the hypothetical value (e.g. People with high salaries generally do not want to reveal their (...) 
#(...) incomes in surveys) or missing value is dependent on some other variable’s value(...)
#(...) (e.g. Let’s assume that females generally  (...)
#(...) don’t want to reveal their ages! Here the missing value in age variable is impacted by gender variable)


#fill with median
#There isn't enough variables to accuratly predict values for MonthSalary
#Given what was said in the introduction below ##MonthSalary, observations must not be removed
#To minimize the impact of this missing values, the best is to fill missing values with the median

df['MonthSalary'].mean()
df['MonthSalary'].describe()
df['MonthSalary'].median() #2501


df['MonthSalary'].fillna((df['MonthSalary'].median()), inplace=True)

##FirstPYear
#Missing values are 0.3% of total observations
#And it would not be cautious to predict values for this variable
#There is no plausible justification for this missing values (it was not due to intentional (...)
#(...) non disclosure of data, or lack of data.). 
#Most probable of being Missing Completely at Random (MCAR): 
#The fact that a certain value is missing has nothing to do with its hypothetical (...)
#(...) value and with the values of other variables
#Best option is to remove

removedOrModified['noFirstPYearinfo'] = df.loc[pd.isnull(df['FirstPYear'])].copy(deep=True)
df = df.loc[~pd.isnull(df['FirstPYear'])]

##CustMonVal
#No missing values

##ClaimsRate
#No missing values



#***
#***1.1.6 Outlier Treatment***
#***


##IQR

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
outdf = df[(df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))]


#Number of observations that fall beyond the defined thresholds, by variable

for cv in outdf.columns.values:
    if len(outdf[cv].dropna())>0:
        print(cv)
        print(str(len(outdf[cv].dropna())) + " out of " + str(len(outdf[cv])) + " (" + str(round(len(outdf[cv].dropna())/len(outdf[cv])*100,2)) + "%)")
        print("---------------------------------------------------------")

#Take a better look at household, life and work

##Boxplots


#----------
sb.boxplot(x = df['Motor Premium'], orient='h', whis=10) #>2000

#----------
sb.boxplot(x = df['Household Premium'], orient='h', whis=5) #>2000

testedf = df.copy(deep=True)
testedf = testedf.loc[testedf['Household Premium']<2000]
sb.boxplot(x = testedf['Household Premium'], orient='h')
del testedf
#between 1350 and 2000 are 26 relatively sparse observations. When looking to (...)
#(...) the box plot of testedf, it is possible to observe the boxplot for (...)
#(...) the household premium variable with outliers >2000 removed, and it is easy (...)
#(...) to observe that there is an almonst continuous line of observations until 1350.
#This values will also be considered outliers, despite observations >2000 being more clear outliers.

#----------
sb.boxplot(x = df['Health Premium'], orient='h', whis=5) #>500

testedf = df.copy(deep=True)
testedf = testedf.loc[testedf['Health Premium']<5000]
sb.boxplot(x = testedf['Health Premium'], orient='h', whis=5) #>500
del testedf
#>500 and <5000: 2 observations, clearly observable in the boxplot of testedf (obs >5000 removed)
#>5000: 2 observations

#----------
sb.boxplot(x = df['Life Premium'], orient='h') #>300
sb.boxplot(x = df['Life Premium'], orient='h', whis=5) #>300

#----------
sb.boxplot(x = df['Work Premium'], orient='h') #>250 ou >300
sb.boxplot(x = df['Work Premium'], orient='h', whis=5) #>300

#----------
sb.boxplot(x = df['ClaimsRate'], orient='h', whis=5)

#----------
sb.boxplot(x = df['MonthSalary'], orient='h', whis=5) #>5500

#----------
sb.boxplot(x = df['CustMonVal'], orient='h', whis=5)



##Outlier separation
#----------
motorOutliers = df.loc[df['Motor Premium']>2000] #6 observations
#----------
houseOutliers = df.loc[df['Household Premium']>1350] 
#----------
healthOutliers = df.loc[df['Health Premium']>500] #4 observations
#----------
lifeOutliers = df.loc[df['Life Premium']>300] #15 observations
#----------
workOutliers = df.loc[df['Work Premium']>400] #5 observations
#----------
monthSalaryOutliers = df.loc[df['MonthSalary']>5500] #2 observations

#CMV
#https://www.irmi.com/term/insurance-definitions/indemnification
#CMV is highly affected by indemnification. If it occours, CMV most likely will drop below 0
#This variable is only really useful for cases where no indemnification has occured.

teste = df.loc[df['CustMonVal']<2500]
teste = teste.loc[teste['CustMonVal']>-10000]
sb.boxplot(x = teste['CustMonVal'], orient='h', whis=5)
del teste
teste = df.loc[df['CustMonVal']>2500]
del teste


#Cases where CMV is very high denote clear outliers, given high premiums and possibly no indemnifications
#Seems like a very volatile variable
#Nevertheless, it inclues information about claims (due to indemnifications), which could be more useful (...)
#(...) to the overall clustering and analysis than Claims Rate, given that claims rate is for a 2 year period only
#In short, claims rate has a short period when compared with cmv and cmv inclues claims in the formula so...


#Remove claims rate and analyze CMV outliers again, keeping in mind that customers with claims will be (...)
#(...) clearly separated from the other in the cmv distribution.

df = df.drop(columns=['ClaimsRate'])




##CMV outlier analysis
#(annual profit) X (number of years that they are a customer) - (acquisition cost) 
sb.boxplot(x = df['CustMonVal'], orient='h', whis=5)

#----
#Plot is almost impossible to analyze due to observations below -25000
testedf = df.copy(deep=True)
testedf = testedf.loc[testedf['CustMonVal']<-25000]
del testedf
#6 observations below -25000

#----
#Remove obs below -25000 from plot
testedf = df.copy(deep=True)
testedf = testedf.loc[testedf['CustMonVal']>-25000]
sb.boxplot(x = testedf['CustMonVal'], orient='h', whis=5)
#Remove obs below -5000 and above 5000
testedf = testedf.loc[testedf['CustMonVal']<5000]
testedf = testedf.loc[testedf['CustMonVal']>-5000]
sb.boxplot(x = testedf['CustMonVal'], orient='h', whis=5)
#Remove obs below -1000 and above 1000
testedf = testedf.loc[testedf['CustMonVal']<1000]
testedf = testedf.loc[testedf['CustMonVal']>-1000]
sb.boxplot(x = testedf['CustMonVal'], orient='h')
del testedf

#Claims have enormous impact in CMV, and this should not be hidden after outlier treatment.
#A claim is relatively sporadic, and most customers will have no claims or few claims of little value, (...)
#(...) but usually, when big claims happen, they have a huge impact, and that huge impact needs to be (...)
#(...) noticeable in CMV. So, only obs with <-25000 are going to be considered as outliers (too big, will influence a lot more than intended)
CustMonValOutliers = df.loc[df['CustMonVal']<-25000]


#create a dict for outliers
outliers = {'CustMonValOutliers': CustMonValOutliers.copy(deep=True)}
outliers['motorOutliers'] = motorOutliers.copy(deep=True)
outliers['houseOutliers'] = houseOutliers.copy(deep=True)
outliers['healthOutliers'] = healthOutliers.copy(deep=True)
outliers['lifeOutliers'] = lifeOutliers.copy(deep=True)
outliers['workOutliers'] = workOutliers.copy(deep=True)
outliers['monthSalaryOutliers'] = monthSalaryOutliers.copy(deep=True)
del CustMonValOutliers
del motorOutliers
del houseOutliers
del healthOutliers
del lifeOutliers
del workOutliers
del monthSalaryOutliers

#removing outliers from df

#df: 10251 observations

df = df.loc[df['Motor Premium']<=2000]
df = df.loc[df['Household Premium']<=1350] 
df = df.loc[df['Health Premium']<=500]
df = df.loc[df['Life Premium']<=300]
df = df.loc[df['Work Premium']<=400]
df = df.loc[df['MonthSalary']<=5500]
df = df.loc[df['CustMonVal']>=-25000]

#df: 10186 observations
#0.63% of observations were considered outliers and were removed


#***
#***1.1.7 Final Variable Manipulation***
#***


#manipulate existing variables
#create new variables


#---------------------------------------------------------------------------------------------
#NOT GOING TO BE DONE, BUT MENTION IN REPORT
#During the thought for verifying this variable, it became clear that the amount paid by the insurance (...)
#(...) company could play a different role of the claims rate in the analysis.
#Then, given that this rate is for two years, it is possible to obtain the value paid by (...)
#(...) the insurance company in the last two years.
#(Given that ClaimsRate is for every type of policy)
#---> Refer claims rate for every type of policy, subsequent analysis and indmenization analysis
#---------------------------------------------------------------------------------------------


##YearlySalary
df['YearlySalary'] = df['MonthSalary']*14
df = df.drop(columns=['MonthSalary'])


##YearsAsCustomer
df['YearsAsCustomer'] = 1998 - df['FirstPYear']
df = df.drop(columns=['FirstPYear'])


##Negative Premium Values
#There are two possible approaches to deal with negative premium values. Since we are dealing with (...)
#(...) aggregated values for premiums, there are several possible scenarios:
#- The value presented in a policy category is the sum of every premium paid by the insured (positive or 0)
#- The value presented in a policy category is the sum of every premium paid by the insured - value return due to cancelation of one policy (total value is still positive, sum of premiums paid > money given back)
#- The value presented in a policy category is the sum of every premium paid by the insured - value return due to cancelation of one policy (total value is negative, sum of premiums paid < money given back)
#- The value presented in a policy category is the sum of every premium paid by the insured - value return due to cancelation of one policy (total value is 0, sum of premiums paid = money given back)
#- The value presented in a policy category is the sum of money given back to the ensured (negative)
#Since we have no information about premium values isolated from money returned to the ensured, several issues arise, (...)
#(...) given that we may be considering for clustering customers with the same values for premiums that are in fact very different.
#A strategy to reduce this issues could be to transform negative premium values to 0, which would increase the clustering accuracy by (...)
#(...) removing the weight of value returned and considering only premium values. On the other hand, this strategy cannot be implemented, (...)
#(...) given that other returns could still be in the data, and that partial removal could bring more disadvantages than advantages.

#--> Negative premium values will be kept


##Creation of branches
#For clustering, it can be useful to perform two approaches, giving two different views:
#- Absolute values (clustering will occur based on absolute values) => df
#- Ratios and percentages (clustering will occur based on amount spent in a specific category in comparison with other categories) => df2

#------------------------------------------------------------------
#It would be useful to create the said branches, but that would imply a different strategy to deal with (...)
#(...) negative premium values, given that negative premium values will produce inaccurate ratios and totals.
#This strategy would only be possible, with the desired accuracy, if premium values and returned values to the insured would be separated.
#------------------------------------------------------------------

#df2 = df.copy(deep=True)

#Creation of TotalPremiums var
#df2['TotalPremiums'] = df2['Motor Premium'] + df2['Household Premium'] + df2['Health Premium'] + df2['Life Premium'] + df2['Work Premium'] 
#motor of first customer 375.85/665.56

#Transformation of premium vars in ratios
#df2['Motor Premium'] = df2['Motor Premium']/df2['TotalPremiums'] 
#df2['Household Premium'] = df2['Household Premium']/df2['TotalPremiums'] 
#df2['Health Premium'] = df2['Health Premium']/df2['TotalPremiums'] 
#df2['Life Premium'] = df2['Life Premium']/df2['TotalPremiums'] 
#df2['Work Premium'] = df2['Work Premium']/df2['TotalPremiums'] 
#df2['PercOfSalaryInPremiums'] = df2['YearlySalary']/df2['TotalPremiums']

