# loug-garou--
Speech analyse and intention classification in the game of werewolves



### Data

Data noted down manually from the TV show Pandakill.

### Environments and tools

- Python 3.6.3
- ipython 6.1.0
- jupyter 1.0.0
- HanLP 0.1.41 (python interface pyHanLP)
- jieba 0.39
- Keras 2.0.6 (with tensorflow 1.0.0 back end)
- Pandas 0.20.3
- Scikit-Learn 0.19.1



### File introduction



**original_text** the original noted down subtitle files named by the episode.



**demo-game-english.txt** for english readers, this is a piece of translated noted down subtitles.



**data_speech_all.csv** all the annotated and arranged speech part data.



**s1e101_behavior.json, s1e102_behavior.json, s1e102_behavior.json** annotated and arranged behavior part data exemple.



**userdict.txt** user dictionary which contains special game terms.



**prepare_easymode.py, prepare_hardmode.py** when construct the speech part and the behavior part, I had hesitations. In the beginning, I have tried to modelize the game to get general architecture to construct the two parts automatically by prepare_hardmode.py. But it turned out to be too difficult because the game is dynamic and unpredictable, there is so many exceptions and variations that to construct a general architecture becomes too expensive even considering the simplest rules. So I just extracted the paragraphs of speech for the speech part into csv files using prepare_easymode.py, and manually noted down the behavior records into json files.



**intent_classification_data_explore.ipynb** shows the basic statistical information of the speech data. I also add a little baseline of unsupervised clustering and look at its entropy to know it's effect.



**intent_classification_learning.ipynb** shows the machine learning methods and their performance including hyper parameter tuning for the intent classification task of the speech part.



**intent_classification_RNN.py, intent_classification_w2v.py** use RNN LSTMs to the classification task, one with pretrained Chinese word embedding (cf.  https://github.com/Embedding/Chinese-Word-Vectors) another not.



**intent_classification_LSTM.ipynb** shows the hyper parameters tuning of the neural network with GridSearch



**speech_summary_final.ipynb** uses the results of intent classification task, along with the syntax parsing with HaNLP to get precise sentence meaning, then to summarize the speech turn of each player. It then uses these information to construct a configuration of the game situation. Along with the behavior record information, it then calculates the penalty score of each possible wolf team every speech turn. The team who gets the least penalty score is the predicted wolf team.



**qui-sont-les-loups-garou.pdf** the PPT for my defense