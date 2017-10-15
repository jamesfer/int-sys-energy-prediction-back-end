
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


hourly = pd.read_csv('hourly_combined_clean.csv')
hourly = hourly.drop(['repr','02:00:00', '03:00:00','04:00:00','05:00:00',
       '06:00:00', '07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00',
       '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00',
       '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00',
       '24:00:00'], axis=1)
hourly.columns


# In[3]:


hourly.head()


# In[4]:


cols_to_norm = ['day', 'month', 'year'] 


# In[5]:


hourly[cols_to_norm] = hourly[cols_to_norm].apply(lambda x: ((x - x.min()) / (x.max() - x.min()) )) #normalise the data
hourly.head()


# In[6]:


# TRAIN TEST SPLIT

# remove prediction column
x_data = hourly.drop('01:00:00', axis=1)
y_val = hourly['01:00:00']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x_data,y_val,test_size=0.3)


# In[7]:


import tensorflow as tf
country_group = tf.feature_column.categorical_column_with_hash_bucket('Country', hash_bucket_size=50)
day = tf.feature_column.numeric_column('day')
month = tf.feature_column.numeric_column('month')
year = tf.feature_column.numeric_column('year')


# In[8]:


# create embedded group coloumn out of country group for dense neural network
embedded_country_col = tf.feature_column.embedding_column(country_group, dimension=4)


# In[9]:


# feature columns
feat_cols = [embedded_country_col,day,month,year]


# In[10]:


x_data.head()


# In[11]:


y_val.head()


# In[12]:


input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train ,batch_size=10,num_epochs=1000,
                                            shuffle=True)


# In[13]:


# create deep neural network model
model = tf.estimator.DNNRegressor(hidden_units=[10,10,10],feature_columns=feat_cols)


# In[44]:


model.train(input_fn=input_func,steps=100000)


# In[45]:


# eval DNN
eval_input_func = tf.estimator.inputs.pandas_input_fn(X_train, y_train,batch_size=10,num_epochs=1,shuffle=False)

model.evaluate(eval_input_func)


# In[46]:


# predict
predict_input_func = tf.estimator.inputs.pandas_input_fn(
      x=X_test,
      batch_size=10,
      num_epochs=1,
      shuffle=False)


# In[47]:


model.predict(predict_input_func)


# In[48]:


pred_gen = model.predict(predict_input_func)


# In[49]:


predictions = list(pred_gen)


# In[50]:


predictions


# In[51]:


# create array of predicted value
final_preds = []
for pred in predictions:
    final_preds.append(pred['predictions'])


# In[52]:


from sklearn.metrics import mean_squared_error
# Root-mean-square deviation
mean_squared_error(y_test,final_preds)**0.5


# In[53]:


X_test


# In[54]:


print('Score:' + model.score(X_test, y_test))


# In[ ]:


plt.scatter(y_test, final_preds)
plt.xlabel('True Values')
plt.ylabel('Predictions')


# In[ ]:




