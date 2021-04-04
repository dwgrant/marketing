#!/usr/bin/env python
# coding: utf-8

"""[script_name.py]

[description]

Author:         Danny Grant
Origin Date:    DD MMM YYYY
Last Updated:   DD MMM YYYY
"""

# %%   PREP WORKSPACE

import pandas as pd
import io
import boto3
import os


# %%   FUNCTION: upload_df_to_s3csv

def upload_df_tp_s3csv(df: pd.DataFrame, aws_profile: str, bucket: str,
                       path: str, include_index: bool = False, sep: str = None):
    """


    -------
    :param df:
    :param aws_profile:
    :param bucket:
    :param path:
    :param include_index:
    :param sep:
    :return:
    """

    key_pub = os.getenv('AWS_ACCESS_KEY_ID')
    key_pri = os.getenv('AWS_SECRET_ACCESS_KEY')
    token = os.getenv('AWS_SESSION_TOKEN')

    session = boto3.Session(aws_access_key_id=key_pub,
                            aws_secret_access_key=key_pri,
                            aws_session_token=token,
                            profile_name=aws_profile)
    csv_buffer = io.StringIO()
    if sep is None:
        df.to_csv(csv_buffer, index=include_index)
    elif sep == 'pipe':
        df.to_csv(csv_buffer, index=include_index, sep='|')
    elif sep == 'tab':
        df.to_csv(csv_buffer, index=include_index, sep='\t')
    else:
        raise ValueError('Only comma, pipe, and tab separators are currently ' +
                         'supported. Comma is the default and does not need ' +
                         'to be specified.')

    s3_re = session.resource('s3')
    response = s3_re.Object(bucket, path).put(Body=csv_buffer.getvalue())
    response_code = response['ResponseMetaData']['HTTPStatusCode']
    if response_code == 200:
        return print('Successfully posted dataframe to S3 destination')
    else:
        return print('Error: Issue posting to S3')

# %%   FUNCTION: read_s3csv_to_df


def read_s3csv_to_df(aws_profile: str, bucket: str, path: str,
                     dtype_spec: dict = None, sep_spec: str = None,
                     usecols_spec: list = None):
    """

    :param aws_profile:
    :param bucket:
    :param path:
    :param dtype_spec:
    :param sep_spec:
    :param usecols_spec:
    :return:
    """
    key_pub = os.getenv('AWS_ACCESS_KEY_ID')
    key_pri = os.getenv('AWS_SECRET_ACCESS_KEY')
    token = os.getenv('AWS_SESSION_TOKEN')

    session = boto3.Session(aws_access_key_id=key_pub,
                            aws_secret_access_key=key_pri,
                            aws_session_token=token,
                            profile_name=aws_profile)

    s3 = session.resource('s3')

    item_raw = s3.Object(bucket_name=bucket, key=path)
    response = item_raw.get()
    item = response['Body'].read()

    if sep_spec is None:
        item_df = pd.read_csv(io.BytesIO(item),
                              low_memory=False,
                              dtype=dtype_spec,
                              usecols=usecols_spec)

    elif sep_spec is not None:
        item_df = pd.read_csv(io.BytesIO(item),
                              low_memory=False,
                              sep=sep_spec,
                              dtype=dtype_spec,
                              usecols=usecols_spec)

    else:
        raise ValueError("Check sep_spec vs pandas.read_csv's sep argument")

    return item_df
