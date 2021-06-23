#!/usr/bin/env python
# coding: utf-8

# In[1]:

import requests
# pretty print is used to print the output in the console in an easy to read format
from pprint import pprint


# In[2]:

# function to use requests.post to make an API call to the subgraph url
def run_query(q) :
    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


# In[3]:

query = """
{
swaps(orderBy: timestamp, orderDirection: desc, where:{pair: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"}) {
    id
    timestamp
    amount0In
    amount1In
    amount0Out
    amount1Out
    pair {
      token0 {
        id
        symbol
      }
      token1 {
        id
        symbol
      }
    }
  }

}
"""


# In[4]:

result = run_query(query)


# In[6]:

# pretty print the results
pprint(result)


# For plotting liquidity vs volume

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
x = np.arange(len(amount1Out))
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
   go.Scatter(x=x, y=amount1Out, name="Liquidity"),secondary_y=False,
)
fig.add_trace(
   go.Scatter(x=x, y=amount0Out, name="Volume"), secondary_y=True
)
# Add figure title
fig.update_layout(title_text="Uniswap Liquidity vs Volume")
# Set x-axis title
fig.update_xaxes(title_text="Blocks")
# Set y-axes title
fig.update_yaxes(title_text="Liquidity", secondary_y=False)
fig.update_yaxes(title_text="Volume", secondary_y=True)
fig.show()

