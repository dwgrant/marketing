# %%

import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time

# %%
g_auth = GoogleAuth()
# %%
g_auth.LocalWebserverAuth()
# %%
drive = GoogleDrive(g_auth)

# Auto-iterate through all files that matches this query
file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    time.sleep(1)


# %%

leads = pd.read_csv('data/KAG_conversion_data.csv')
