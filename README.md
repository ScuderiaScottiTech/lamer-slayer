# Annihilate lamers in your group
## A Convolutional Neural Network for Classifying Text Messages
This project includes everything you need to do Natural Language Processing (NLP), from a basic bot that restricts unintended users
to the Neural Network trainer and tester.
### Results
We have achieved 82-85% accuracy with this model and with just 2k messages per class.
### How can I use it?
You can use this project too, but you'll need some resources that we've already managed to get.

First, you'll need a proper dataset of messages that belong to specific classes (we support multiclass detection!).  
In the ``model-preparation`` folder there are some message extractors from Telegram JSON chat exports. 
Without entering too much into details, the bad-extractor retrieves the last N messages from a specific user that was banned by an authorized userid (i.e., an admin).  
The good-extractor, instead, retrieves that last N messages from a group.

Once you have downloaded the chat exports and organized them into classes, you can let the extractors do their work by running the Makefile with the following command:
```
make all -B
```
Then, run the trainer by executing ``python3 naturalprocess.py <train-directory>``  
If you're going to use this for your Telegram group, you'll need to create a bot and authenticate it using an API ID and API Hash, nothing new.
### Contributing
The NN design is far from perfect and can be improved; we have found that this level of complexity is appropriate for what we intended to do.  
If you have some experience in this field or want to enhance it further, here there are some techniques that could do it (from most likely to less likely)
- Better filtering of the dataset
- Auto dataset expander (e.g. bot that automatically scrapes messages from a list of groups/forums/whatever)
- L2 Regularization
- Different convolutional design
- Different activation functions
- Different cost functions
