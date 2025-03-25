import sys
sys.path.append('/pytorch-chatbot/')

import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize


class NLPBot:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        with open('trained/intents.json', encoding='utf-8') as json_data:
            self.intents = json.load(json_data)

        self.FILE = "trained/data.pth"
        self.data = torch.load(self.FILE)

        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data['all_words']
        self.tags = self.data['tags']
        self.model_state = self.data["model_state"]

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

        self.bot_name = "Liter"

    

    def getPrediction(self, sentence):
        print(sentence)
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.05:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses']) + "\n" + prob.item().__str__()
        else: return None 