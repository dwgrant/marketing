#!/usr/bin/env python
# coding: utf-8

"""[script_name.py]

[description]

Author:         Danny Grant
Origin Date:    DD MMM YYYY
Last Updated:   DD MMM YYYY
"""

# %%   PREP WORKSPACE

import scripts.functions.function_aws as aws
import matplotlib.pyplot as plt
import numpy as np


# %%   SET PARAMETERS

aws_profile = 'dgrant'
aws_bucket = 'dwg-aws-bucket'
aws_path = 'projects/marketing/KAG_conversion_data.csv'

# %%   INGEST DATA

test = aws.read_s3csv_to_df(aws_profile=aws_profile, bucket=aws_bucket,
                            path=aws_path)


# %%   DATA CLEANING

test['gender_male'] = [True if x == 'M' else False for x in test.gender]


# %%   FEATURE DEVELOPMENT

"""
Click-through-rate (CTR). 
This is the percentage of how many of our impressions became clicks. A high CTR 
is often seen as a sign of good creative being presented to a relevant audience. 
A low click through rate is suggestive of less-than-engaging adverts (design 
and / or messaging) and / or presentation of adverts to an inappropriate 
audience. What is seen as a good CTR will depend on the type of advert (website 
banner, Google Shopping ad, search network test ad etc.) and can vary across 
sectors, but 2% would be a reasonable benchmark.
"""

test['click_thru_rate'] = test.Clicks / test.Impressions

"""
Conversion Rate (CR). 
This is the percentage of clicks that result in a 'conversion'. What a 
conversion is will be determined by the objectives of the campaign. It could be 
a sale, someone completing a contact form on a landing page, downloading an 
e-book, watching a video, or simply spending more than a particular amount of 
time or viewing over a target number of pages on a website.
"""

test['conversion_rate'] = test.Clicks / test.Total_Conversion

"""
Cost Per Click (CPC). 
Self-explanatory this one: how much (on average) did each click cost. While it 
can often be seen as desirable to reduce the cost per click, the CPC needs to be
considered along with other variables. For example, a campaign with an average 
CPC of £0.5 and a CR of 5% is likely achieving more with its budget than one 
with a CPC of £0.2 and a CR of 1% (assuming the conversion value is the same.
"""

test['cost_per_click'] = test.Spent / test.Clicks

"""
Cost Per Conversion. 
Another simple metric, this figure is often more relevant than the CPC, as it 
combines the CPC and CR metrics, giving us an easy way to quickly get a feel for
campaign effectiveness.
"""

test['cost_per_conversion'] = test.Spent / test.Total_Conversion

# %%   QUESTION 01: Distribution of CTR

sum(test.click_thru_rate.isna())

# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=test.click_thru_rate,
                            bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('My Very Own Histogram')
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
plt.axvline(x=np.mean(test.click_thru_rate), color='#ff0000')
plt.axvline(x=np.median(test.click_thru_rate), color='#000000')
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

print(np.mean(test.click_thru_rate))
print(np.median(test.click_thru_rate))


# %%   QUESTION 02: Clear profiles for CTR?

test['ctr_high'] = [True if x > 0.0004 else False for x in test.click_thru_rate]

test_ctr_high = (
    test
    .query('ctr_high == True')
)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

# Plot violin plot on axes 1
ax1.violinplot((test
                .query('gender_male == True')
                .filter(['click_thru_rate'])), showmedians=True)
ax1.set_title('Male')

# Plot violin plot on axes 2
ax2.violinplot((test
                .query('gender_male == False')
                .filter(['click_thru_rate'])), showmedians=True)
ax2.set_title('Female')

plt.show()


fig2, (ax3, ax4) = plt.subplots(nrows=1, ncols=2)

# Plot violin plot on axes 1
ax3.violinplot((test_ctr_high
                .query('gender_male == True')
                .filter(['click_thru_rate'])), showmedians=True)
ax3.set_title('Male')

# Plot violin plot on axes 2
ax4.violinplot((test_ctr_high
                .query('gender_male == False')
                .filter(['click_thru_rate'])), showmedians=True)
ax4.set_title('Female')

plt.show()


# %%    AGE RELATED

test.age.unique()

fig3, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

ax1.violinplot((test
                .query('age == "30-34"')
                .filter(['click_thru_rate'])), showmedians=True)
ax1.set_title('30')
ax2.violinplot((test
                .query('age == "35-39"')
                .filter(['click_thru_rate'])), showmedians=True)
ax2.set_title('35')
ax3.violinplot((test
                .query('age == "40-44"')
                .filter(['click_thru_rate'])), showmedians=True)
ax3.set_title('40')
ax4.violinplot((test
                .query('age == "45-49"')
                .filter(['click_thru_rate'])), showmedians=True)
ax4.set_title('45')
plt.show()


fig4, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

ax1.violinplot((test_ctr_high
                .query('age == "30-34"')
                .filter(['click_thru_rate'])), showmedians=True)
ax1.set_title('30')
ax2.violinplot((test_ctr_high
                .query('age == "35-39"')
                .filter(['click_thru_rate'])), showmedians=True)
ax2.set_title('35')
ax3.violinplot((test_ctr_high
                .query('age == "40-44"')
                .filter(['click_thru_rate'])), showmedians=True)
ax3.set_title('40')
ax4.violinplot((test_ctr_high
                .query('age == "45-49"')
                .filter(['click_thru_rate'])), showmedians=True)
ax4.set_title('45')
plt.show()

# %%   INTEREST

test

len(test.interest.unique())