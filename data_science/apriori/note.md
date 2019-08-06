Association Rule Mining

* 機器學習的標準流程
    * Gathering data
    * Preparing that data
    * Choosing a model
    * Training
    * Evaluation
    * Hyperparameter tuning
    * Prediction

* Association rules are **if-then** statements that help to show the probability of relationships between data items within large data sets in various types of databases.
    * transactions, web mining
    * 星期五、尿布與啤酒
    * we want to find **strong rules**
* **Rule-based**, **unsupervised** machine learning method

---
| TID   | Items                      |
|:-----:|:--------------------------:|
| 1     | Bread, Milk                |
| 2     | Bread, Diaper, Beer, Eggs  |
| 3     | Milk, Diaper, Beer, Coke   |
| 4     | Bread, Milk, Diaper, Beer  |
| 5     | Bread, Milk, Diaper, Coke  |

## Definitions
### Frequent Itemset
* Itemset: A collection of one or more items
    * Example: {Milk, Bread, Diaper}
* k-itemset
    * An itemset that contains k items
* Support Count
    * Frequency of occurrence of an itemset
    * cnt({Bread, Milk, Diaper}) = 2
* Support
    * Fraction of transactions that contain an itemset
    * support({Milk, Bread, Diaper}) = 2/5
* Frequent Itemset
    * An itemset whose support is greater than or equal to a minsup

### Association Rule
* X -> Y, where X and Y are itemsets
    * {Milk, Diaper} -> {Beer}
* confidence:
    * conf(X=>Y) = support(X ∪ Y) / support(X) = P(Y|X) (conditional probability)
* strong rules:
    rules that satisfies certain threshloding (ex: minsup, minconf)

## Mining Association Rules
### Brutal Force
#### Procedures
1. List all possible association rules
2. compute the support and confidence for each rule
3. Prune rules that fail the minsup and minconf

#### Problems
For an itemset {Milk, Bread, Diaper}, it can generate the following rules:

```
{Milk, Diaper} -> {Bread}
{Milk, Bread} -> {Diaper}
{Milk} -> {Bread, Diaper}
{Bread, Diaper} -> {Milk}
{Bread} -> {Diaper, Milk}
{Diaper} -> {Milk, Bread}
```

* They are binary partitions of the same itemset
    * suuport可以預先算好
    * 再從預先算好的support去算confidence

### Apriori

#### Basic Concepts
* Pruning (剪枝)
    * If an itemset is frequent, then all of its subsets must also be frequent

* Frequent Itemset Generation
    * Generate all itemsets whose support >= minsup

* Rule Generation
    * Generate high confidence rules from each frequent itemset, where each rule is a binary partitioning of a frequent itemset

#### Algorithm

##### Description
1. Let k=1 (1-itemset)
2. Generate frequent itemsets of length 1
3. Repeat until no new frequent itemsets are identified
    * Generate length (k+1) candidate itemsets from length k
    frequent itemsets
    * Prune candidate itemsets containing subsets of length k
    that are infrequent
    * Count the support of each candidate by scanning the DB
    * Eliminate candidates that are infrequent, leaving only
    those that are frequent

##### Key point
* 分候選集(C)和頻繁集(L)
* 每一次利用前一次頻繁集的結果產生這次的候選集，算出候選集的support並做pruning


## Takeaway
* Machine Learning 基本流程
* probability
    * conditional / joint distribution
* apriori
    * lattice
    * algorithm

## References
1. [DMTM Lecture 16 Association rules](https://www.slideshare.net/pierluca.lanzi/dmtm-lecture-16-association-rules)
2. [Big Data經典案例：星期五、尿布與啤酒](https://www.digitimes.com.tw/tw/dt/n/shwnws.asp?cnlid=10&cat=35&id=401927)
3. [你怎麼處理顧客交易資訊？Apriori演算法](https://medium.com/marketingdatascience/%E4%BD%A0%E6%80%8E%E9%BA%BC%E8%99%95%E7%90%86%E9%A1%A7%E5%AE%A2%E4%BA%A4%E6%98%93%E8%B3%87%E8%A8%8A-apriori%E6%BC%94%E7%AE%97%E6%B3%95-1523b1f8443b)
