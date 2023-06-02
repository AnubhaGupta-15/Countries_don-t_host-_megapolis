#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install mysql-connector-python')


# In[1]:


import pandas as pd
import mysql.connector


# In[2]:


df=pd.read_excel('cities_population.xlsx')
df=df.where(pd.notnull(df), None)


# In[4]:


connection=mysql.connector.connect(host='localhost',port='3306',user='root',password='heyanu15')
cursor=connection.cursor()
cursor.execute("CREATE DATABASE Countries_dont_host_megapolis")


# In[7]:


connection = mysql.connector.connect(host='localhost',port='3306', user='root',password='heyanu15',database='Countries_dont_host_megapolis')
cursor = connection.cursor()

table = """
CREATE TABLE Details (
    Name VARCHAR(255),
    `Country name EN` VARCHAR(255),
    Population INT,
    `Country Code` CHAR(2)
)
"""
cursor.execute(table)

queries = "INSERT INTO Details(Name, `Country name EN`, Population, `Country Code`) VALUES (%s, %s, %s, %s)"

for index, row in df.iterrows():
    values = (row['Name'], row['Country name EN'], row['Population'], row['Country Code'])
    cursor.execute(queries, values)


connection.commit()


# In[14]:


connection = mysql.connector.connect(host='localhost',port='3306', user='root',password='heyanu15',database='Countries_dont_host_megapolis')
cursor = connection.cursor()

query = """
SELECT DISTINCT `Country Code`, `Country name EN`
FROM Details
WHERE Population < 10000000 AND `Country name EN` IS NOT NULL
ORDER BY `Country name EN`
"""
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

Results = pd.DataFrame(results, columns=['Country Code', 'Country Name'])


file = 'countries_without_megapolises.xlsx'
Results.to_excel(file,index=False)


# In[ ]:




