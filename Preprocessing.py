#!/usr/bin/env python
# coding: utf-8

# In[107]:


import pandas as pd
from sqlalchemy import create_engine

# Credentials to database connection
hostname="localhost"
dbname="project"
uname="root"
pwd=getpass.getpass(prompt="Password:\n")


# In[62]:


# Create dataframe
df = pd.read_csv('C:/Users/bornf/Documents/Northeastern/2022 Fall/DS5110 IDMP/Project/Python/Medicine.txt', sep='\t', encoding = 'unicode_escape')

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname, pw=pwd))
df.dropna()
df


# In[35]:


engine.execute('alter table medicine modify column PRODUCTID varchar(4)')


# In[36]:


engine.execute('alter table medicine add primary key(PRODUCTID)')


# In[57]:


df = pd.read_csv('C:/Users/bornf/Documents/Northeastern/2022 Fall/DS5110 IDMP/Project/Python/DoMH.csv', encoding = 'unicode_escape')


# In[58]:


df = df[df['Programs/Services'] == "MENTAL HEALTH SERVICES"]
df = df.head(10)
df = df.rename(columns={"Provider Name": "Rehab_Name","Provider Classification": "Rehab_Type","Phone Number": "Number","Location 1": "Location"})
df = df[['Rehab_Name','Rehab_Type','Location','Number']]
val = [1,2,3,4,5,6,7,8,9,10]
df.insert(loc=0,column='Rehab_ID',value=val)
df


# In[59]:


df.to_sql('rehab', engine, index=False)

