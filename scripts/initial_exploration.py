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


# %%   SET PARAMETERS

aws_profile = 'dgrant'
aws_bucket = 'dwg-aws-bucket'
aws_path = 'projects/marketing/KAG_conversion_data.csv'

# %%   INGEST DATA

test = aws.read_s3csv_to_df(aws_profile=aws_profile, bucket=aws_bucket,
                            path=aws_path)

# %%   MANIPULATE DATA

"""
Click-through-rate (CTR). 
This is the percentage of how many of our impressions became clicks. A high CTR 
is often seen as a sign of good creative being presented to a relevant audience. 
A low click through rate is suggestive of less-than-engaging adverts (design 
and / or messaging) and / or presentation of adverts to an inappropriate 
audience. What is seen as a good CTR will depend on the type of advert (website 
banner, Google Shopping ad, search network test ad etc.) and can vary across 
sectors, but 2% would be a reasonable benchmark.

Conversion Rate (CR). 
This is the percentage of clicks that result in a 'conversion'. What a 
conversion is will be determined by the objectives of the campaign. It could be 
a sale, someone completing a contact form on a landing page, downloading an 
e-book, watching a video, or simply spending more than a particular amount of 
time or viewing over a target number of pages on a website.

Cost Per Click (CPC). 
Self-explanatory this one: how much (on average) did each click cost. While it 
can often be seen as desirable to reduce the cost per click, the CPC needs to be
considered along with other variables. For example, a campaign with an average 
CPC of £0.5 and a CR of 5% is likely achieving more with its budget than one 
with a CPC of £0.2 and a CR of 1% (assuming the conversion value is the same.

Cost Per Conversion. 
Another simple metric, this figure is often more relevant than the CPC, as it 
combines the CPC and CR metrics, giving us an easy way to quickly get a feel for
campaign effectiveness.
"""
