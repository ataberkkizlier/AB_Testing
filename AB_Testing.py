'''Facebook recently introduced a new type of bidding, "average bidding", as an alternative to the existing type of bidding called "maximum bidding".
One of our clients, bombabomba.com, decided to test this new feature and wants to run an A/B test to see if average bidding brings more conversions than maximum bidding.
The A/B test has been running for 1 month and bombabomba.com is now waiting for you to analyze the results of this A/B test. The ultimate measure of success for Bombabomba.com is Purchase. Therefore, the focus should be on the Purchase metric for statistical testing.'''

import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

'''Step 1: Read the data set named ab_testing_data.xlsx which consists of control and test group data. Assign control and test group data to separate variables'''

df_c = pd.read_excel("/Users/ataberk/Desktop/Miuul Bootcamp/week 4/ABTesti/ab_testing.xlsx", sheet_name = "Control Group")
df_t = pd.read_excel("/Users/ataberk/Desktop/Miuul Bootcamp/week 4/ABTesti/ab_testing.xlsx", sheet_name = "Test Group")

'''Step 2: Analyze the control and test group data.'''
df_c.head()
df_t.head()

df_c.describe().T
df_t.describe().T

df_c.isnull().sum()
df_t.isnull().sum()

df_c.info()
df_t.info()

df_c.shape # (40, 4)
df_t.shape # (40, 4)


'''Step 3: After the analysis, combine the control and test group data using the concat method.'''

df_c["Bidding"] = "maximum_bidding"
df_t["Bidding"] = "average_bidding"
df = pd.concat([df_c, df_t], ignore_index = True)


'''Task 2: Defining the Hypothesis of the A/B Test'''

'''
Step 1: Define the hypothesis. 
H0 : 
M1 = M2
H1 : M1!= M2
Step 2: Analyze the purchase (gain) averages for the control and test group.'''

#No difference between control and test group purchase averages.
#There is a difference between control and test group purchase averages.

df_c["Bidding"] = "maximum_bidding"

df_c.groupby("Bidding").agg({"Purchase": "mean"})
#Bidding
#maximum_bidding 550.89406

df_t["Bidding"] = "average_bidding"

df_t.groupby("Bidding").agg({"Purchase": "mean"})

#average_bidding 582.10610

df.groupby("Bidding").agg({"Purchase":"mean"})
#average_bidding 582.10610
#maximum_bidding 550.89406

'''Task 3: Hypothesis Testing
Step 1: Make assumption checks before hypothesis testing.
These are Normality Assumption and Variance Homogeneity. Test whether the control and test groups comply with the normality assumption separately on the Purchase variable.
Normality Assumption :
H0: The assumption of normal distribution is met. H1: The assumption of normal distribution is not met.
p < 0.05 H0 RED, p > 0.05 H0 CANNOT BE REJECTED
According to the test result, is the normality assumption met for the control and test groups? Interpret the p-value values obtained.
Homogeneity of Variance :
H0: Variances are homogeneous.
H1: Variances are not homogeneous.
p < 0.05 H0 RED, p > 0.05 H0 CANNOT BE REJECTED'''

test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "maximum_bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = 0.9773, p-value = 0.5891, > 0.50. It fits the niormal distrubition.


test_stat, pvalue = shapiro(df.loc[df["Bidding"] == "average_bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541, >0.50, It fits the normal distrubiton.

test_stat, pvalue = levene(df.loc[df["Bidding"] == "maximum_bidding", "Purchase"],
                           df.loc[df["Bidding"] == "average_bidding", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 2.6393, p-value = 0.1083 > 0.05 H0 can't be rejected.
# H0: Variances are Homogeneous.

'''Test whether the homogeneity of variance is ensured for the control and test groups on the Purchase variable. According to the test result, is the normality assumption met? Interpret the p-value values obtained.
Step 2: Select the appropriate test according to the results of Normality Assumption and Homogeneity of Variance.'''
# Since the assumptions are met, an independent two sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no statistically significant difference between the control group and test group purchase averages)
# H1: M1 != M2 (There is a statistically significant difference between the control group and test group purchase averages)
# p<0.05 HO RED, p>0.05 HO CANNOT REJECT

'''Step 3: Considering the p_value obtained as a result of the test, interpret whether there is a statistically significant difference between the control and test group purchase averages.'''

test_stat, pvalue = ttest_ind(df.loc[df["Bidding"] == "maximum_bidding", "Purchase"],
                              df.loc[df["Bidding"] == "average_bidding", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = -0.9416, p-value = 0.3493 >0.05 H


'''Task 4: Analysis of Results
Step 1: State which test you used and why.
Step 2: Make a recommendation to the customer based on the test results you obtained.'''