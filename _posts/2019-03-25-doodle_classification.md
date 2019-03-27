---
title: "Doodle Classification @ Kaggle"
date: 2019-03-25 08:26:28 -0400
categories: jekyll update
---
This is just a test docs<br/>
I want to update this docs with my code<br/>
The code may look like the following.<br/>
https://gist.github.com/ihoneymon/652be052a0727ad59601<br/>

Today, I want to share my experience of participating in one of Kaggle competition, [**Quick, Draw! Doodle Recognition Challenge**](https://www.kaggle.com/c/quickdraw-doodle-recognition) I will briefly introduce the challenge and start to explain dataset and others. This post may have the following sections.

1. Dataset
2. Feature extraction
3. Model selection
4. Evaluation
5. Ensemble
6. Submission

# 1. Dataset
Datasets are a set of CSV files. Each CSV file is a collection of images that people drew and the name of CSV file is a target that people are asked to draw. For example, in ant.csv file, all ant images that people draw were collected, including the key\_id and country code, i.e. the country code where each image was drawn. 

In this competition, participants are asked to classify images each of which are one of 340 labels. The list of labels are [LABEL]. Also it is important to note that each drawn image is provided in raw format and simplified format.

## 1.1 Raw format dataset
Raw format of data means no preprocessing has been applied on this dataset. People drew each target in their own devices, such as his i-phone, i-pad, desktop PC, or anything else. No matter what devices were used, raw-formatted CSV file contains values of each image including the key\_id and country code.
FIG1 explains how an image is handled under the raw-format.

![FIG1: representation of image data](http://jinkilee.github.io/img/doodle/fig1.png)

The raw-formatted train file is provided as a single ZIP file which contains list of following files.
- The Eiffel Tower.csv: Image of Eiffel Tower has been collected.
- The Great Wall of China.csv: Image of Great wall of China has been collected.
...
- ant.csv: Image of ant has been collected.
In a raw-formatted ZIP train file, there are 340 CSV files, because we are asked to classify 340 classes.

In this competition, we are supposed to be ranked from the accuracy of test dataset. This test dataset has xxxxx images and provided in raw-format.

```python
def print_hi(name):
    print("hello", name)
print_hi('Tom')
```

## 1.2 Simplified format dataset
Everything is same as raw-formatted dataset, but few difference should be noted.
- Each data point value is ranged from 0 to 255 (somehow normalized)
- Each data point value is an int type.
- No time data is provided for each image. That is, only (x, y) data is available.
- Test dataset is provided in simplified format (NOT raw-file format)

## 1.3 Read Raw/Simplified formatted dataset
Watching is better than Reading. For those who does not have enough time to read, dataset can be read as shown below.

Firstly, we can read the raw-formatted file like this.
```python
import pandas as pd
raw = pd.read_csv('/data/doodle/raw/The Eiffel Tower.csv')
raw.head()
```

And we can read the simplified-formatted file like this.
```python
import pandas as pd
simp = pd.read_csv('/data/doodle/simplified/The Eiffel Tower.csv')
simp.head()
```

Basically, whether it is raw-formatted or simplified one, the entire column does not change.
However the size of drawing column is much smaller with simplified-formatted file due to the following reasons
- simplified image has less data points than raw image.
- simplified image does not have time data.


# 2. Feature extraction
Before we extract feature, we should re-organize and shuffle our dataset, because each CSV file has only one label. We are going to read a chunck of data from each CSV and make a new CSV file which contains 340 different labels. Then to save capacity of disk space, we compressed the new CSV files. In this way, we created 100 newly-compressed CSV files all of which contain 340 labels, i.e. well-shuffled. Whole process of re-organization of dataset is explained in FIG2.

![FIG2: re-organization and shuffling of original data](http://jinkilee.github.io/img/doodle/fig2.png)

Also note that you should run the above process for simplified format and raw format both, if you want to use both of them.

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
