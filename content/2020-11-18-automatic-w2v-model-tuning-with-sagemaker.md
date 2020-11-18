---
title: Automatic word2vec model tuning using Sagemaker  
date: 2020-11-18    
comments: false  
tags: aws, sagemaker, machine learning  
keywords: python, data science, aws, sagemaker, s3, pyspark, blazingtext, word2vec, w2v, nlp
---

In this post, we continue our discussion about how to use AWS Sagemaker's BlazingText to train a word2vec model. In the [last post]({filename}2020-09-07-training-w2v-with-sagemaker-blazing-text.md) we learned how to set up, train and evaluate a single model. However, we essentially selected our hyperparameters at random, meaning our model is not likely to be performing as well as it could. Traditionally, we would either do a [grid search](https://en.wikipedia.org/wiki/Hyperparameter_optimization#Grid_search) to exhaustively find the best combination of hyperparameters, or a [random search](https://en.wikipedia.org/wiki/Hyperparameter_optimization#Random_search) to sample from these combinations. 

Sagemaker offers a third alternative, which is to use a method called [Bayesian optimisation](https://en.wikipedia.org/wiki/Hyperparameter_optimization#Bayesian_optimization). I will not pretend to understand how this works in detail, but the general idea is that, starting from a seed set of hyperparameters, the optimiser checks how each model performs against our objective metric and then tries to pick a set of hyperparameters that will improve the model performance in the next round of training. The tuning then continues until either the model cannot be further improved, or the maximum number of training rounds has been reached. This [excellent video from AWS](https://www.youtube.com/watch?v=xpZFNIOaQns) explains in more detail how it has been implemented in Sagemaker.

In this post I'll take you through how to tune a set of word2vec models using Sagemaker's inbuilt objective metric, the WS-353 goldsets, as well as discuss some practical considerations such as the cost of this tuning and the potential limitations of the WS-353 for some NLP tasks.

## Setting up our tuning

In order to get started, we'll use the exact same set up for the execution role, S3 bucket, training image and Sagemaker estimator which I discussed in the last post. We'll also start with the same set of hyperparameter we used for our last model.


```python
import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.tuner import (IntegerParameter, CategoricalParameter, ContinuousParameter, 
                             HyperparameterTuner)

role = get_execution_role()
bucket_name = 'sagemaker-blog-corpus-nlp'
tags = [{'Key': 'user:application', 'Value': 'BlazingText'}]

region_name = boto3.Session().region_name
container = sagemaker.amazon.amazon_estimator.get_image_uri(region_name, "blazingtext", "latest")

# Create estimator object
bt_model = sagemaker.estimator.Estimator(
    container,
    role,
    train_instance_count=1,
    train_instance_type='ml.c5.xlarge',
    train_volume_size=11,
    train_max_run=36000,
    base_job_name='blazingtext-blogs-sentences',
    input_mode='File',
    output_path='s3://{}/models/blazingtext'.format(bucket_name),
    tags=tags
)

# Set initial hyperparameters
bt_model.set_hyperparameters(
    mode="batch_skipgram",
    epochs=10, 
    min_count=40,
    sampling_threshold=0.0001,
    learning_rate=0.05,
    window_size=5,
    vector_dim=100,
    negative_samples=5,
    batch_size=11,
    evaluation=True,
    subwords=False
)

# Get path to training data
input_data = f"s3://{bucket_name}/cleaned_sentences.csv"
```

In order to use the automatic tuner rather than just training a single model, we need to take a couple of extra steps here. Firstly, we need to decide which hyperparameters we wish to tune and what ranges of possible values we'd like the tuner to test for each one. [This page](https://docs.aws.amazon.com/sagemaker/latest/dg/blazingtext-tuning.html) gives a guide on the most important hyperparameters and their recommended ranges for testing.


```python
hyperparameter_ranges = {
    'mode': CategoricalParameter(['batch_skipgram', 'cbow']),
    'learning_rate': ContinuousParameter(0.005, 0.05, scaling_type="Logarithmic"),
    'window_size': IntegerParameter(5, 30),
    'vector_dim': IntegerParameter(50, 100),
    'min_count': IntegerParameter(20, 50),
    'negative_samples': IntegerParameter(5,25)
}
```

Next, we need to set up our tuner. We indicate that we want the tuner to use the BlazingText estimator we created, and maximise the mean correlation with the WS-353 gold sets in order to optimise the model. We've also told the tuner to only try to test the hyperparameters we included in our `hyperparameter_ranges` dictionary above. Finally, we've also told the model that we only want to do up to 12 rounds of tuning, and that the model can run up to two training jobs in parallel.


```python
objective_metric_name = 'train:mean_rho'

tuner = HyperparameterTuner(
    bt_model,
    objective_metric_name,
    hyperparameter_ranges,
    max_jobs=12,
    max_parallel_jobs=2,
    objective_type='Maximize',
    tags=tags
)
```

We are finally ready to kick off our tuning job! Unlike when training a single job, when we execute this cell we won't get any feedback in the notebook. However, you can go to your Sagemaker dashboard and look at `Hyperparameter Tuning Jobs` under `Training` and you'll be able to see that the job has started. You're also able to shut down your Sagemaker notebook instance while you wait for the tuning job to finish. This is also something you might want to set to run overnight, as the total training time for these models was around 7.5 hours.


```python
tuner.fit({'train': input_data}, wait=False)
```

## Comparing our models and picking the best performing

Once our tuning job is finished, we can retrieve all of our model hyperparameters and performance metrics using Sagemaker search. The following code will retrieve all models contained in the S3 bucket I am using for this project, as I've asked it to retrieve all models from buckets containing `blog-corpus-nlp`. I took this code directly from [the video on automatic tuning](https://www.youtube.com/watch?v=xpZFNIOaQns) that I discussed at the beginning of this post.


```python
smclient = boto3.client(service_name = "sagemaker")

search_params = {
    "MaxResults": 100,
    "Resource": "TrainingJob",
    "SearchExpression": {
        "Filters": [
            {
            "Name": "InputDataConfig.DataSource.S3DataSource.S3Uri",
            "Operator": "Contains",
            "Value": "blog-corpus-nlp"
            },
            {
                "Name": "TrainingJobStatus",
                "Operator": "Equals",
                "Value": "Completed"
            },
        ],
    }
}
results = smclient.search(**search_params)
```

These results are returned in a rather messy JSON, so in order to make it a bit easier to check and compare these models, I'll extract the relevant data I want and put it in a `pandas` DataFrame. I'll also rank the table so that the models that performed best against the objective metric are at the top of the DataFrame.


```python
import pandas as pd
import numpy as np

def extractModelInfo(model_dict):
    model_name = model_dict["TrainingJobName"]
    bs = model_dict["BillableTimeInSeconds"]
    score = model_dict["FinalMetricDataList"][0]["Value"]
    hyperparams = model_dict["HyperParameters"]
    
    d1 = {"model_name": model_name, "billableSeconds": bs, "mean_rho": score}
    return {**d1, **hyperparams}

desired_fields = ["model_name", "mean_rho", "learning_rate", "min_count", "negative_samples", 
                  "mode", "vector_dim", "window_size", "billableSeconds"]

results_df = pd.DataFrame([extractModelInfo(results["Results"][i]["TrainingJob"]) 
                           for i in np.arange(1, len(results["Results"]))])
results_df = results_df.loc[results_df["mode"] != "skipgram", 
                            desired_fields].sort_values("mean_rho", ascending = False)
results_df
```

<div>
<table class="table table-bordered">
  <thead>
    <tr style="text-align: right;">
      <th style="text-align:center"><b>model_name</b></th>
      <th style="text-align:center"><b>mean_rho</b></th>
      <th style="text-align:center"><b>learning_rate</b></th>
      <th style="text-align:center"><b>min_count</b></th>
      <th style="text-align:center"><b>negative_samples</b></th>
      <th style="text-align:center"><b>mode</b></th>
      <th style="text-align:center"><b>vector_dim</b></th>
      <th style="text-align:center"><b>window_size</b></th>
      <th style="text-align:center"><b>billableSeconds</b></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-010-4a414e1b</td>
      <td style="text-align:center">0.7449</td>
      <td style="text-align:center">0.0116</td>
      <td style="text-align:center">32</td>
      <td style="text-align:center">6</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">100</td>
      <td style="text-align:center">28</td>
      <td style="text-align:center">1385</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-009-218d44a5</td>
      <td style="text-align:center">0.7447</td>
      <td style="text-align:center">0.0054</td>
      <td style="text-align:center">38</td>
      <td style="text-align:center">25</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">100</td>
      <td style="text-align:center">24</td>
      <td style="text-align:center">3163</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-009-218d44a5</td>
      <td style="text-align:center">0.7447</td>
      <td style="text-align:center">0.0054</td>
      <td style="text-align:center">38</td>
      <td style="text-align:center">25</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">100</td>
      <td style="text-align:center">24</td>
      <td style="text-align:center">3163</td>
    </tr>
        <tr>
      <td style="text-align:center">blazingtext-200627-1812-011-269247ac</td>
      <td style="text-align:center">0.7427</td>
      <td style="text-align:center">0.0055</td>
      <td style="text-align:center">38</td>
      <td style="text-align:center">25</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">99</td>
      <td style="text-align:center">24</td>
      <td style="text-align:center">3705</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-004-88f21ab4</td>
      <td style="text-align:center">0.7377</td>
      <td style="text-align:center">0.0059</td>
      <td style="text-align:center">36</td>
      <td style="text-align:center">18</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">80</td>
      <td style="text-align:center">24</td>
      <td style="text-align:center">2348</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-006-a80fdc2a</td>
      <td style="text-align:center">0.7368</td>
      <td style="text-align:center">0.00642</td>
      <td style="text-align:center">49</td>
      <td style="text-align:center">23</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">65</td>
      <td style="text-align:center">22</td>
      <td style="text-align:center">2727</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-005-0c7e32d9</td>
      <td style="text-align:center">0.7357</td>
      <td style="text-align:center">0.0060</td>
      <td style="text-align:center">36</td>
      <td style="text-align:center">18</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">79</td>
      <td style="text-align:center">24</td>
      <td style="text-align:center">2492</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-007-d617ec0b</td>
      <td style="text-align:center">0.7352</td>
      <td style="text-align:center">0.0066</td>
      <td style="text-align:center">49</td>
      <td style="text-align:center">23</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">66</td>
      <td style="text-align:center">22</td>
      <td style="text-align:center">2491</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-012-4b6fa554</td>
      <td style="text-align:center">0.7337</td>
      <td style="text-align:center">0.0105</td>
      <td style="text-align:center">39</td>
      <td style="text-align:center">11</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">90</td>
      <td style="text-align:center">30</td>
      <td style="text-align:center">1962</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-002-43d5a552</td>
      <td style="text-align:center">0.7311</td>
      <td style="text-align:center">0.0270</td>
      <td style="text-align:center">40</td>
      <td style="text-align:center">17</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">93</td>
      <td style="text-align:center">23</td>
      <td style="text-align:center">2587</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-008-b935f3c1</td>
      <td style="text-align:center">0.7211</td>
      <td style="text-align:center">0.0056</td>
      <td style="text-align:center">47</td>
      <td style="text-align:center">9</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">50</td>
      <td style="text-align:center">20</td>
      <td style="text-align:center">1289</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-001-2eab54f0</td>
      <td style="text-align:center">0.7201</td>
      <td style="text-align:center">0.0150</td>
      <td style="text-align:center">28</td>
      <td style="text-align:center">21</td>
      <td style="text-align:center">batch_skipgram</td>
      <td style="text-align:center">77</td>
      <td style="text-align:center">8</td>
      <td style="text-align:center">1889</td>
    </tr>
    <tr>
      <td style="text-align:center">blazingtext-200627-1812-003-c735efa6</td>
      <td style="text-align:center">0.6310</td>
      <td style="text-align:center">0.0101</td>
      <td style="text-align:center">23</td>
      <td style="text-align:center">10</td>
      <td style="text-align:center">cbow</td>
      <td style="text-align:center">57</td>
      <td style="text-align:center">15</td>
      <td style="text-align:center">769</td>
    </tr>
  </tbody>
</table>
</div>


As you can see, the best performing model used a skipgram architecture, had a learning rate of 0.01, a minimum count for each term of 32, used 6 negative samples, used a 100 dimension vector size and used a rather generous window size of 28 for checking proximate words. It also outperformed our previous model, with a `mean_rho` score of 0.74 (compared to 0.72 for the model we trained in the last post).

Let's check the neighbours we get from this model for the same two queries "family" and "sad" that we checked for the untuned model from the last post.


```python
!aws s3 cp s3://sagemaker-blog-corpus-nlp/models/blazingtext/blazingtext-200627-1812-010-4a414e1b/output/model.tar.gz - | tar -xz    
!pip install gensim
    
from gensim.models import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format('data/best_tuning_model/vectors.txt', binary=False)
```


```python
word_vectors.most_similar("family")
```




    [('relatives', 0.7486746907234192),
     ('grandparents', 0.7312743663787842),
     ('uncles', 0.7192485928535461),
     ('cousins', 0.7149008512496948),
     ('aunts', 0.7009657621383667),
     ('parents', 0.6931362152099609),
     ('aunt', 0.6655760407447815),
     ('grandpa', 0.6604502201080322),
     ('nephews', 0.6573513150215149),
     ('grandmother', 0.6546939611434937)]




```python
word_vectors.most_similar("sad")
```




    [('saddening', 0.7043677568435669),
     ('depressing', 0.6888615489006042),
     ('happy', 0.676035463809967),
     ('unhappy', 0.6721015572547913),
     ('depressed', 0.6692825555801392),
     ('cry', 0.6438484191894531),
     ('pathetic', 0.6382129192352295),
     ('upset', 0.6326898336410522),
     ('angry', 0.6272262930870056),
     ('heartbroken', 0.6254571080207825)]



Overall, the neighbours look around as good for "family" as for the previous model, but seem to look a little better for "sad", showing more relevant terms and less typos.

## How much did this training cost?

I was a little worried when I first started this experiment at home, as I was concerned that running a Sagemaker ML training instance for over 7 hours might be really expensive! Happily, the `ml.c5.xlarge` instances are surprisingly affordable, priced at US\$0.272 per hour in the Frankfurt region. The Sagemaker notebook instances are also reasonably priced, costing US\$0.0536 per hour. My total bill for running this entire training job is US\$2.84. Just remember to shut down your Sagemaker notebook instances when you're not using them, as they can add up quickly if you forget about them for a couple of days!

## A few final thoughts about the WS-353 as a metric

As you can see, for this general-purpose, English language dataset, the WS-353 metrics seemed to work very well for helping us evaluate and tune our word2vec models. However, there are some issues that some with using these datasets which you might want to be aware of for your own NLP projects. I encountered a few of these issues while using the Sagemaker automatic tuning process at my previous job.

Firstly, the WS-353 goldsets are entirely in English, and from what I could find out there is no option to specify the language of the training data and adjust the gold sets used to evaluate the model accordingly. This really limits their utility for non-English language NLP tasks.

Secondly, given that the associations between word pairs in the WS-353 are general, they may not capture associations in more specific domains. For example, in a general context, "java" might represent coffee and "python" might present a snake, and therefore be considered completely unrelated. However, in a job context, "Java" and "Python" would be much more likely to represent programming languages and therefore be quite similar.

In addition, [this interesting paper](https://arxiv.org/pdf/1605.02276.pdf) lists a number of other potential limitations of using the WS-353 for tuning, including issues with averaging over similarity and relatedness (which can semantically represent quite different things) and the potential for overfitting to these small datasets.

These considerations definitely don't invalidate the use of the BlazingText objective metric (well, at least for English-language tasks); however, like everything in data science it means that the tuning process should not be treated as a silver bullet, but should be evaluated within the context of the NLP task you have.

I hope this and the previous article gave you a practical overview on how to train word2vec models using BlazingText, its advantages over training locally, and how to potentially leverage the automatic tuning process to make a better performing model.
