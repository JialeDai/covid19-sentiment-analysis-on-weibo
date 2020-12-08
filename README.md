# covid19-sentiment-analysis-on-weibo
Contriubutor: JialeDai, Song Zhang, Zijing Sun, Bailu Zhang, ZeChang Fang \
Instructor: Houwei Cao \
Website link: https://limitless-harbor-77448.herokuapp.com/
## Introduction
Data analysis is now a very common technique for people to get conclusion from large amount of information. People in western countries have already had a lot of study on how to use data to analysis sentiment and get conclusion from those data. We have done our research and find several references. Considering the outbreak in China is the most representative, since it has the entire increasing and decreasing period which is helpful for us to figure out the disease and people’s attitude change as the pandemic develops. So, we want to collect the user post on the social media and train a classifier to decide whether a certain a user post is positive or negative. We can use the model we train to analysis the sentiment on social media during the period of the disease outbreak. The model we trained can be used to classify all the post in our data set and the result will be presented as curves shown on our website. A well-designed web page can help people get the needed information conveniently. We plan to make an interactive map to show the how the infection changes the provinces in China and the countries all around the world.
## Project Methodologies
### Data
#### Data Collection
The datasets we use in our project can be mainly dividedly into three types, the data of user posts from sina weibo, the infection data of COVID-19 in China and worldwide data of COVID-19. \
Weibo users update their attitudes and feelings on the social media platform. Basically, we write the spider program to crawl the data from weibo website. The program is written by python.  We choose to use the chrome driver and selenium to simulate the operation. Using this method to crawl the data mainly has several advantages. First of all, in order to get access to all the post on weibo, we have to log in. However, the website sometimes needs the user to enter identifying code which is changeable and hard to tell by program. By using chrome driver, writing code to recognize the identifying code can be avoided because the we enter the necessary information such as username, password and identifying code in chrome driver manually by ourselves. In this way, login operation can be relatively simple compared with login by program. After logging in successfully, we use selenium to enter the keyword we originally set up in the program to the input area of weibo and do the click operation on the search button. Then we got the pages that displays the information. The default setting of Weibo is to search the key word by day. The weibo website has the limitation that when search can only get 50 pages maximum, which means we can only get 50 pages of data per day.  In order to get as much data as possible, we use the selenium to set the weibo to search the keyword by hours. In this case, the data scalar can be extended to 24 time larger. The program will check if the page has the content. Once the program finds the content, it will grab the specific content and save into the excel file. \
We make the heat map of the infection based on the data of China and the whole world. The infection data contains the reginal information, the number of confirmed, suspected and the dead cases in that certain region. The raw data set is collection others who also pay a lot of attention to this pandemic. We do the necessary processing and store the processed data into database.
#### Data Procerssing
The raw data we grabbed from weibo website is divided by every hour. The first of the processing is to combine the different sheet named by hour in the same day together. After we get the correct format of the data, we should do the data clean. Since the raw data is full of the noisy information which will cause the difficulty for the future labeling, training and prediction. We mainly want to remove the following irrelevant data: the key word tag wrapped by #, some content with special symbols such as @, the unnecessary line change (\n) and space (\t), the meaningless content like “转发微博”，“展开全文”. We choose to use the regular expression to extract and remove the noise information. The other information we need to deal with is the emoji symbol. Because the emoji is also an important way to express one’s feelings. In order to use the emoji to do the sentiment analysis, we choose to use the emoji package in python to convert the symbol to the code. Each symbol has its corresponding unique code. The last step about handling the weibo post data is to remove the repeat post since some people or bots are always repeating the same contents many times. The infection data of the china and the world is also processed and stored into the excel file as a appropriate format for displaying the map on the website.
#### Data Storage
In order to show the heat map on the website, back end is supposed to connect to the database to get the data and pass the data to the front end. We choose to use mongodb to store our data. Because such huge scaler data which can easily convert into key-value pair is relative suitable for mongodb. 
And we choose to save the post data in excel file. By doing so, we can view the post data and label the train set more conveniently.
### Front End
Because we want to design a dynamic and user interactive interface, excepted from CSS and HTML, JavaScript is widely implemented in our front end. Like the heatmap and word could in our project, both are realized through JS document. Here we reference some examples from ECHARTS.  The JS document it provides contains very powerful component, what we need to do is just understanding each attributes of the component and adjust it to what we want. \
Take the china heatmap for example, here I use timeline: {} as the biggest component, map: {} and bar: {} is the subcomponent under timeline: {}. It firstly maps the date, then maps the data to each providence in each day. \
![Picture1.png](https://i.loli.net/2020/12/08/6wOBiym5dS8LPcu.png) \
For this interface, we use the JS document world cloud. To realize the floating effect, we use component embedded in the component tooltip: {} which also shows the high flexibility of JS. The floating window is a new window, so it also involves some simple parameter transferring in JS. \
![Picture1.png](https://i.loli.net/2020/12/08/Xdet5xWFDLSUIEY.png) \
### Back end
For the back-end part, the database we use as mentioned before is MongoDB. The storing strategy of this database is based on document type. This database is convenient for our project, because we didn’t have any input data to store from our website. We have stored the virus infection data for both China and world. Besides, our sentiment analysis and keyword extraction result are also saved in the database. In order to connect and transfer our data from database to the front end, we use Django package to do this job.
### Keyword Extraction
For keyword extraction part, which is the core of building the word cloud. The target in our extraction is the 300,000 posts we have cleaned before. We use jieba API to do the extraction work by using built in function jieba.analysis.extract_tag. And this extraction is based on the TF-IDF (term frequency and inverse document frequency). For the whole process, first we get the top 50 keywords in all the posts. Those 50 keywords are the words we are going to show in our word cloud. Then, based on the situation in China, we divided the date into 5 periods: 12/1 - 1/22 is before Wuhan locked down, 1/23 - 2/18 the situation getting worse in China, 2/19 - 3/11 the situation in China getting better, 3/12 - 4/7 resuming work in China, 4/8 - 4/30 Wuhan unblocking. After that, we could get the weight, also called the percentage, of each keyword in those 5 periods. Finally, use each keyword as the key, and their weights as the value to form the dictionary, and store it into the database.
### Sentiment Analysis
Next, comes to the main part of our project, the sentiment analysis. This task is actually the supervised learning task, so the first thing we do is the labeling. We have labeled about 3 different datasets, and their properties are all mentioned in this slide. Because we are doing the classification model, so we have to make the number of samples in each class nearly equal with each other. For labeling approach, two members of our group each labels half of those datasets. By using the -1, 0, 1 for positive, neutral and negative posts. We take the percentage of different kinds of word to consider whether a sentence is negative or positive. For those neutral ones, we think post similar to news, report and advertisement all can be considered as the non-sentiment. One problem for labeling part is that we didn’t let our team members to write two labels for each post and check them twice. We just let them label each part of the dataset. So, there may be some bias in the labeling due to different judgement for different people. \
In model training part, we firstly would like to introduce one application we have purchased for extracting features. LIWC also called Linguistic Inquiry and Word Count. It is a text analysis program which can analysis the text and return the percentage of each category word in the input text. For example, it can consider some words as negative feeling and positive feeling. It can even draw more detailed emotions like sad, angry, and so on. Therefore, we use two kinds of features in our model: TF-IDF (term frequency and inverse document frequency) and LIWC feature. 3 algorithms are used in our training part: Naïve Bayes, Linear regression and SVM (Support Vector Machine). Through different combination of those datasets, features and algorithms, we have trained about 16 models. \
Unlike English, Chinese has no space between word and word, so before applying the feature extraction, we have to do the word segmentation for Chinese text. By using a package developed by the Qinhua university in China called Thulac, we can use the built-in function thulac.cut to perform segmentation. Besides, Sklearn is our choice to implement model algorithms. For example, Naïve Bayes uses sklearn.naive_bayes.MultinomialNB. Linear regression: uses sklearn.linear_model.LinearRegression. SVM uses sklearn.svm.SVC. SVD (Singular Vector Decomposition) uses sklearn.decomposition.TruncatedSVD. \
And following two figures are the results of our TF-IDF features’ dimension reduction. The first one is for the reduction of D2 dataset, and the second is for the reduction of D3. And the numbers in red rectangle box stands for the number of features. From those two figures, we could see the reduction didn’t improve the final accuracy for SVM model. So, we still focus on the training results without dimension reduction. \
![Picture1.png](https://i.loli.net/2020/12/08/xSDW8PRiahw4OjH.png) \
![Picture1.png](https://i.loli.net/2020/12/08/voV45kyaJctn7dz.png) \
Then, the following table is all our training results. From the result table we could see that first with the data increases, the model’s accuracy is also increasing. Besides, TF-IDF features have better performance than the LIWC features. SVM model actually has better performance on LIWC features than Naïve Bayes model. And finally, we have chosen the red one as our prediction model. 
| Model | Feature | Number of data | Accuracy/MSE |
|:--|:--|:--|:--|
|Naive Bayes| TFIDF | 1500 |73.0%|
| Linear Regression | TFIDF |1500| 2.15e+26 |
|SVM|TFIDF|1500| 70.8% |
|Naive Bayes|LIWC|1500|68.2%|
|Linear Regression|LIWC|1500|3.38|
| SVM |LIWC|1500|69.7%|
|Naive Bayes|TFIDF|2500|65.1%|
|SVM|TFIDF|2500|71.4%|
|Naive Bayes|LIWC|2500|60.0%|
|SVM|LIWC|2500|69.8%|
|Naive Bayes|TFIDF|6000|83.8%|
|SVM|TFIDF|6000|84.0%|
|Naive Bayes|LIWC|6000|67.8%|
|SVM|LIWC|6000|74.2%| 

For model prediction part, our target still is the 300 thousand cleaned posts. As mentioned before, we have used 6,000 training data, Naïve Bayes and TF-IDF feature model as our final model. During the processing, we first use this trained model predict the score of posts for each day. This score actually represents the type of each post and is include in the set {-1, 0, 1}, which is mentioned in labeling part. Then, calculate the mean of each day’s score, and the percentage of each type’s post. Finally, use date as key, prediction results as the value to form the dictionary, and store it to the database for the visualization. And the following figure is the counts for each kind of posts in our prediction result. We can see that the negative count is actually increasing faster than the positive count in the later period. \
![Picture1.png](https://i.loli.net/2020/12/08/fxkjsqKLEY4IGnM.png) 
## Project Result and Achievement
Generally speaking, the result of the project satisfies what we expect to do at the beginning. First of all, our project contains valuable information which is grabbed from the social media platform. The real data give our sentiment analysis strong validation science it can reflect people’s real reaction as the disease develops. We plot several curves to show our analysis. According to the curve, the trend of the sentiment is positively related to the Chinese cases and negatively related to the world cases. To be specific, before 1st march, the pandemic in China is relatively serious which our sentiment analysis shows post on social media are relatively positive. However, after 1st march, the pandemic in china is getting better and the weight of the negative post among the entire posts are increasing. At first, we think the result does not make sense. However, after checking the model and finding noting abnormal. We make a hypothesis that as the pandemic in China getting better, the cases outside China are increasing and people discuss the foreign condition and hold relatively negative attitude toward it. \ 
In order to validate our hysteresis, we also draw the curve of the confirmed cases all around the world and it turns out that our sentiment analysis result is positively related with the trend of world pandemic condition. In addition, we also build our topic model to make the word could base on the posts we collected. The topic model shows the curve of some word such as united states, Trump has, basically, the same trend as our sentient analysis outputs. And for some topics like mask, virus actually have the same trend as our sentiment analysis result. Such result can be taken as the evidence of our hypothesis.
## Conclusion and Future Work
For this project, we have learned the skill of collecting, processing and storing the data. We practice making the frond and build the back end. we also upload our website publicly to make more people know the things we worked on. The project of ours is valuable for people study on the COVID-19 ‘s development or do research about sentiment analysis. \
For the future work, we expect people can utilize the project as a reference for continuing the study in the area of natural language processing, machine learning, web crawler, website development and data visualization.
