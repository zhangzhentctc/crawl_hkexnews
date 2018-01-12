import numpy as np
import pandas as pd

# prepare for data
data = np.arange(1,101).reshape((10,10))
data_df = pd.DataFrame(data)

# change the index and column name
data_df.columns = ['A','B','C','D','E','F','G','H','I','J']
data_df.index = ['a','b','c','d','e','f','g','h','i','j']

# create and writer pd.DataFrame to excel
writer = pd.ExcelWriter('Save_Excel.xlsx')
data_df.to_excel(writer,'page_1',float_format='%.5f') # float_format 控制精度
writer.save()