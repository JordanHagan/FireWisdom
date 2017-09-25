# Fire-Wisdom
### Data Science Immersive Cohort 49 Capstone Project

## About FireWise
*"Brush, grass and forest fires don’t have to be disasters. NFPA’s Firewise USA program encourages local solutions for safety by involving homeowners in taking individual responsibility for preparing their homes from the risk of wildfire. Firewise is a key component of Fire Adapted Communities – a collaborative approach that connects all those who play a role in wildfire education, planning and action with comprehensive resources to help reduce risk.*

*The program is co-sponsored by the USDA Forest Service, the US Department of the Interior, and the National Association of State Foresters.*

*To save lives and property from wildfire, NFPA's Firewise USA program teaches people how to adapt to living with wildfire and encourages neighbors to work together and take action now to prevent losses. We all have a role to play in protecting ourselves and each other from the risk of wildfire."*
<sub><b>[Source](http://www.firewise.org/about.aspx)</b></sub>

## Table of Contents
1. [About](#about)
2. [Natural Language Processing Tools](#natural-language-processing-tools)
    * [RNN](#rnn)
    * [NMF](#nmf)
    * [LDA](#lda)

## About
Data and what they can do with it has been a rising topic within the NFPA organization. They are hoping to discover new tools, and best practices to continue on with this project long after my partnership with them is over. We are very excited about this collaboration.

There are 2 goals to this project:
1. Natural Language Processing on historical data to gain valuable insights
2. Risk tool used to gain more insights into their Communities

## Natural Language Processing Tools
One of my personal goals of this project was to gain more knowledge around different NLP tools. The world is full of free-text fields that are full of useful data just waiting for us to mine! Exploring alternative methodologies around tapping into this data sounded fun and challenging.

### RNN ([code](https://github.com/JordanHagan/FireWisdom/blob/master/src/python/RNN.py))
FireWise had already mapped around 2,000 free text fields to the categories they identified.  My theory is that we could do all the normal NLP pre-model text processing, map that resulting text to numbers, put those numbers into a matrix, and run that matrix through a Recurrent Neural Network to hopefully have it learn by the words in the matrix, which category it maps to.

Right now, the RNN is operating at about 75% accuracy.  My theory as to why it is unable to identify which category the text belongs in is because free text fields can have more than 1 category within it. This situation is better handled by NMF or LDA.

### NMF ([code](https://github.com/JordanHagan/FireWisdom/blob/master/src/python/NMF_or_LDA.py))
*"Non-negative matrix factorization (NMF) is used for feature extraction and is generally seen to be useful when there are many attributes, particularly when the attributes are ambiguous or are not strong predictors. By combining attributes NMF can display patterns, topics, or themes which have importance."*
<sub><b>[Source](https://datascience.stackexchange.com/questions/10299/what-is-a-good-explanation-of-non-negative-matrix-factorization/15438)</b></sub>

*"NMF can be mostly seen as a LDA of which the parameters have been fixed to enforce a sparse solution. So it may not be as flexible as LDA if you want to find multiple topics in single documents, e.g., from long articles. But it could work very well out of box for corpora of short texts. This makes NMF attractive for short text analysis because its computation is usually much cheaper than LDA."*
<sub><b>[Source](http://nbviewer.jupyter.org/github/dolaameng/tutorials/blob/master/topic-finding-for-short-texts/topics_for_short_texts.ipynb)</b></sub>


### LDA ([code](https://github.com/JordanHagan/FireWisdom/blob/master/src/python/NMF_or_LDA.py))
*"In natural language processing, latent Dirichlet allocation (LDA) is a generative statistical model that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar."*
<sub><b>[Source](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)</b></sub>

*"LDA finds topics as a group of words that have high co-occurrences among different documents. On the other side, documents from the similar mixture of topics should also be similar, such that they can be described by these topics in a "compact" way. So ideally the similarity in the latent topic space would imply the the similarity in both the observed word space as well as the document space - this is where the word "latent" in the name come from."*
<sub><b>[Source](http://nbviewer.jupyter.org/github/dolaameng/tutorials/blob/master/topic-finding-for-short-texts/topics_for_short_texts.ipynb)</b></sub>
