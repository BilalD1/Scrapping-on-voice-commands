from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import pickle, random, os
from flask import Flask, request, jsonify

class Cluster:
    def __init__(self):
        with open("sentences.txt", "r") as file:
            self.lines = file.readlines()
        self.sentences = []
        for line in self.lines:
            sentence = line.strip()
            self.sentences.append(sentence)
        del self.lines
        self.num_clusters = 7
        
        self.sentences = list(set(self.sentences))
        self.vectorizer = CountVectorizer()
        self.X = self.vectorizer.fit_transform(self.sentences)
    
    def clustering(self):
        # Clustering with K-means
        self.kmeans = KMeans(n_clusters=self.num_clusters)
        self.kmeans.fit(self.X)

        os.remove('kmeans_model.pkl')


        with open('kmeans_model.pkl', 'wb') as file:
            pickle.dump(self.kmeans, file)
    
    def predict_cluster(self, new_sentence):
        with open('kmeans_model.pkl', 'rb') as file:
            self.kmeans = pickle.load(file)
        
        self.input_vector = self.vectorizer.transform([new_sentence])
        self.cluster_label = self.kmeans.predict(self.input_vector)[0]
        return(self.cluster_label)
    
    def append_sentence(self,new_sentence):
        self.sentences.append(new_sentence)
        with open("sentences2.txt", "w") as file:
            for sentence in self.sentences:
                file.write(sentence + "\n")
    
    def get_clusters(self):
        self.cluster_list = []
        for cluster_id in range(self.num_clusters):
            self.cluster_sentences = [self.sentences[i] for i, label in enumerate(self.kmeans.labels_) if label == cluster_id]
            self.cluster_list.append(self.cluster_sentences)
            del self.cluster_sentences
        return self.cluster_list
    
    def scrap_clusters(self):
        self.scrap_clusters_list = []
        self.cluster_list = self.get_clusters()
        for cluster_id in range(self.num_clusters):
            self.choice = min(self.cluster_list[cluster_id])
            self.scrap_clusters_list.append(self.choice)
        return self.scrap_clusters_list
