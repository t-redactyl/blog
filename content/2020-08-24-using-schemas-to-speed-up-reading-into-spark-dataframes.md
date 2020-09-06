---
title: Using schemas to speed up reading into Spark DataFrames  
date: 2020-08-24   
comments: false  
tags: pyspark  
keywords: python, data science, aws, sagemaker, s3, pyspark
---

While Spark is the best thing since sliced bread for dealing with big data, I definitely realise I have a lot to learn before I can use it to its full potential. One trick I recently discovered was using explicit schemas to speed up how fast PySpark can read a CSV into a DataFrame.

When using `spark.read_csv` to read in a CSV in PySpark, the most straightforward way is to set the `inferSchema` argument to `True`. This means that PySpark will attempt to check the data in order to work out what type of data each column is. 

The problem with this operation is that it's quite memory intensive, especially for large datasets, as Spark needs to look at a sufficient amount of data in order to correctly infer the type. Imagine that you have a column with integers in the first 1000 rows, but then a string in the 1001th row. If PySpark had inferred this column was an `IntegerType` based on the top few rows, then we would end up with missing values for each of the rows containing a string. As such, PySpark either needs to scan the whole dataset, or randomly sample enough rows to infer the type.

One way we can get around this is by determining the type of the data beforehand and passing this information to PySpark using an schema. The syntax for this is pretty straightforward. Each column's name and type is defined using the `StructField` method from `pyspark.sql`:


```python
StructField("trip_id", StringType(), True)
```

The three arguments that `StructField` takes are the name you'd like to give the column, the column's data type, and whether the field can contain null values (as a boolean). The available column data types are also in `pyspark.sql`, and cover a wide type of possible data types, from string, float and integer to boolean and datetime. A `StructField` is created for each column, and these are passed as a list to `pyspark.sql`'s `StructType`. This schema can then be passed to `spark.read.csv`'s `schema` argument.


```python
StructType(
    [StructField("trip_id", StringType(), True),
    StructField("call_type", StringType(), True)]
)
```

In order to test how much faster it is to use a schema, I will be using the [Taxi Service Trajectory](https://archive.ics.uci.edu/ml/datasets/Taxi+Service+Trajectory+-+Prediction+Challenge,+ECML+PKDD+2015) dataset from the UCI Machine Learning Repository. This dataset has 9 columns and around 1.7 million rows.

We'll first set up our `SparkSession` to be able to access our data on S3:


```python
from pyspark import SparkConf
from pyspark.sql import SparkSession
import sagemaker_pyspark
import botocore.session

from time import time
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, BooleanType

session = botocore.session.get_session()
credentials = session.get_credentials()

conf = (SparkConf()
        .set("spark.driver.extraClassPath", ":".join(sagemaker_pyspark.classpath_jars())))

spark = (
    SparkSession
    .builder
    .config(conf=conf) \
    .config('fs.s3a.access.key', credentials.access_key)
    .config('fs.s3a.secret.key', credentials.secret_key)
    .appName("schema_test")
    .getOrCreate()
)
```

We'll also set up our data path:


```python
bucket = "sagemaker-pyspark"
data_key = "train.csv"
data_location = f"s3a://{bucket}/{data_key}"
```

Let's first time how long it takes to read in these data when PySpark has to infer the schema:


```python
t1 = time()

data_inferred = spark.read.csv(data_location, header = 'True', inferSchema = True)

t2 = time()
print('Completed in %s sec.' % (str(t2 - t1)))
```

    Completed in 28.1013503074646 sec.


We'll now compare how long it takes when we explicitly tell PySpark what the data schema is:


```python
t1 = time()

schema = StructType(
    [StructField("trip_id", StringType(), True),
    StructField("call_type", StringType(), True),
    StructField("origin_call", IntegerType(), True),
    StructField("origin_stand", IntegerType(), True),
    StructField("taxi_id", LongType(), True),
    StructField("timestamp", LongType(), True),
    StructField("day_type", StringType(), True),
    StructField("missing_data", BooleanType(), True),
    StructField("polyline", StringType(), True)]
)
data_schema = spark.read.csv(data_location, header = 'False', schema = schema)

t2 = time()
print('Completed in %s sec.' % (str(t2 - t1)))
```

    Completed in 2.506075620651245 sec.


The data are read in around 10 times faster when we give PySpark the schema rather than asking it to infer it! Obviously this is a more practical step when you have data with fewer variables, but when reading truly large data, it is an easy way to save some processing time.