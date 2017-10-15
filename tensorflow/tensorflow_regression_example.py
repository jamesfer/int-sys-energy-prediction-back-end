
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


import tensorflow as tf


# In[3]:


x_data = np.linspace(0.0, 10.0, 1000000)


# In[4]:


noise = np.random.rand(len(x_data))


# In[5]:


# y = mx + b

# b = 5


# In[6]:


y_true = (0.5 * x_data) + 5 + noise


# In[7]:


x_df = pd.DataFrame(data=x_data,columns=['X Data'])

y_df = pd.DataFrame(data=y_true,columns=['Y'])

x_df.head()


# In[8]:


my_data = pd.concat([x_df, y_df], axis=1)


# In[9]:


my_data.head()


# In[10]:


my_data.sample(n=250).plot(kind='scatter', x='X Data', y='Y')


# In[11]:


batch_size = 8 # 8 points at a time


# In[12]:


m = tf.Variable(0.81)
b = tf.Variable(0.17)


# In[13]:


xph = tf.placeholder(tf.float32, [batch_size])


# In[14]:


yph = tf.placeholder(tf.float32, [batch_size])


# In[15]:


y_model = m*xph + b


# In[16]:


error = tf.reduce_sum(tf.square(yph-y_model))


# In[17]:


optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
train = optimizer.minimize(error)


# In[18]:


init = tf.global_variables_initializer()


# In[19]:


with tf.Session() as sess:
    sess.run(init)
    
    batches = 10000
    
    for i in range(batches):
        rand_ind = np.random.randint(len(x_data), size=batch_size) # get random index [0, length(x_data)]
        
        feed = {xph: x_data[rand_ind], yph:y_true[rand_ind]}
        
        sess.run(train, feed_dict = feed)
    
    model_m, model_b = sess.run([m,b])


# In[20]:


model_m


# In[21]:


model_b


# In[22]:


y_hat = x_data*model_m + model_b


# In[23]:


my_data.sample(250).plot(kind='scatter', x='X Data', y='Y')
plt.plot(x_data, y_hat, 'r')


# # TF Estimator

# In[25]:


feat_cols = [tf.feature_column.numeric_column('x', shape=[1])]


# In[26]:


estimator = tf.estimator.LinearRegressor(feature_columns=feat_cols)


# In[27]:


from sklearn.model_selection import train_test_split


# In[28]:


x_train, x_eval, y_train, y_eval = train_test_split(x_data, y_true, test_size=0.3, random_state=101)


# In[29]:


print(x_train.shape) # 70% of data used to train the model


# In[30]:


print(x_eval.shape) # 30% of data used to test/evaluate


# In[32]:


input_func = tf.estimator.inputs.numpy_input_fn({'x':x_train}, y_train, batch_size=8, num_epochs=None, shuffle=True)


# In[33]:


train_input_func = tf.estimator.inputs.numpy_input_fn({'x':x_train}, y_train, batch_size=8, num_epochs=1000, shuffle=False)


# In[34]:


eval_input_func = tf.estimator.inputs.numpy_input_fn({'x':x_eval}, y_eval, batch_size=8, num_epochs=1000, shuffle=False)


# In[35]:


estimator.train(input_fn=input_func, steps=1000)


# In[36]:


train_metrics = estimator.evaluate(input_fn=train_input_func, steps=1000)


# In[37]:


eval_metrics = estimator.evaluate(input_fn=eval_input_func, steps=1000)


# In[38]:


print('TRAINING DATA METRICS')
print(train_metrics)


# In[39]:


print('EVALUATION DATA METRICS')
print(eval_metrics)


# In[43]:


brand_new_data = np.linspace(0,10,10)
input_fn_predict = tf.estimator.inputs.numpy_input_fn({'x': brand_new_data}, shuffle=False)


# In[45]:


list(estimator.predict(input_fn_predict)) # returns a list of dictionary of predictions


# In[50]:


predictions = []

# convert list of dictionary to array
for pred in estimator.predict(input_fn=input_fn_predict):
    predictions.append(pred['predictions'])


# In[51]:


predictions


# In[55]:


my_data.sample(250).plot(kind='scatter', x='X Data', y='Y')
plt.plot(brand_new_data, predictions, 'r*')


# In[ ]:




