'''
This script includes:

1. ClassifierOfflineTrain
    This is for offline training. The input data are the processed features.
2. class ClassifierOnlineTest(object)
    This is for online testing. The input data are the raw skeletons.
    It uses FeatureGenerator to extract features,
    and then use ClassifierOfflineTrain to recognize the action.
    Notice, this model is only for recognizing the action of one person.
    
TODO: Add more comments to this function.
'''

import numpy as np
import sys
import os
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import deque
import cv2

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.decomposition import PCA

# import postHumanAction
import requests
import json
from datetime import datetime

if True:
    import sys
    import os
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    sys.path.append(ROOT)

    from utils.lib_feature_proc import FeatureGenerator


# -- Settings
NUM_FEATURES_FROM_PCA = 50

# -- Classes


class ClassifierOfflineTrain(object):
    ''' The classifer for offline training.
        The input features to this classifier are already 
            processed by `class FeatureGenerator`.
    '''
    
    def __init__(self):
        self._init_all_models()

        # self.clf = self._choose_model("Nearest Neighbors")
        # self.clf = self._choose_model("Linear SVM")
        # self.clf = self._choose_model("RBF SVM")
        # self.clf = self._choose_model("Gaussian Process")
        # self.clf = self._choose_model("Decision Tree")
        # self.clf = self._choose_model("Random Forest")
        self.clf = self._choose_model("Neural Net")

    def predict(self, X):
        ''' Predict the class index of the feature X '''
        Y_predict = self.clf.predict(self.pca.transform(X))
        return Y_predict

    def predict_and_evaluate(self, te_X, te_Y):
        ''' Test model on test set and obtain accuracy '''
        te_Y_predict = self.predict(te_X)
        N = len(te_Y)
        n = sum(te_Y_predict == te_Y)
        accu = n / N
        return accu, te_Y_predict

    def train(self, X, Y):
        ''' Train model. The result is saved into self.clf '''
        n_components = min(NUM_FEATURES_FROM_PCA, X.shape[1])
        self.pca = PCA(n_components=n_components, whiten=True)
        self.pca.fit(X)
        # print("Sum eig values:", np.sum(self.pca.singular_values_))
        # print("Sum eig values:", np.sum(self.pca.explained_variance_ratio_))
        X_new = self.pca.transform(X)
        # print("After PCA, X.shape = ", X_new.shape)
        self.clf.fit(X_new, Y)

    def _choose_model(self, name):
        self.model_name = name
        idx = self.names.index(name)
        return self.classifiers[idx]

    def _init_all_models(self):
        self.names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
                      "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
                      "Naive Bayes", "QDA"]
        self.model_name = None
        self.classifiers = [
            KNeighborsClassifier(5),
            SVC(kernel="linear", C=10.0),
            SVC(gamma=0.01, C=1.0, verbose=True),
            GaussianProcessClassifier(1.0 * RBF(1.0)),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(
                max_depth=30, n_estimators=100, max_features="auto"),
            MLPClassifier((20, 30, 40)),  # Neural Net
            AdaBoostClassifier(),
            GaussianNB(),
            QuadraticDiscriminantAnalysis()]

    def _predict_proba(self, X):
        ''' Predict the probability of feature X belonging to each of the class Y[i] '''
        Y_probs = self.clf.predict_proba(self.pca.transform(X))
        return Y_probs  # np.array with a length of len(classes)


class ClassifierOnlineTest(object):
    ''' Classifier for online inference.
        The input data to this classifier is the raw skeleton data, so they
            are processed by `class FeatureGenerator` before sending to the
            self.model trained by `class ClassifierOfflineTrain`. 
    '''

    def __init__(self, model_path, action_labels, window_size, human_id=0):

        # -- Settings
        self.human_id = human_id
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        if self.model is None:
            # print("my Error: failed to load model")
            assert False
        self.action_labels = action_labels
        self.THRESHOLD_SCORE_FOR_DISP = 0.5

        # -- Time serials storage
        self.feature_generator = FeatureGenerator(window_size)
        self.reset()

        # RE_DATA_FACE
        self.re_data_face = "Unknow"
        self.re_data_px = 0
        self.re_data_py = 0

    def reset(self):
        self.feature_generator.reset()
        self.scores_hist = deque()
        self.scores = None

    def predict(self, skeleton):
        ''' Predict the class (string) of the input raw skeleton '''
        LABEL_UNKNOWN = ""
        is_features_good, features = self.feature_generator.add_cur_skeleton(
            skeleton)

        if is_features_good:
            # convert to 2d array
            features = features.reshape(-1, features.shape[0])

            curr_scores = self.model._predict_proba(features)[0]
            self.scores = self.smooth_scores(curr_scores)

            if self.scores.max() < self.THRESHOLD_SCORE_FOR_DISP:  # If lower than threshold, bad
                prediced_label = LABEL_UNKNOWN
            else:
                predicted_idx = self.scores.argmax()
                prediced_label = self.action_labels[predicted_idx]
        else:
            prediced_label = LABEL_UNKNOWN
        return prediced_label

    def smooth_scores(self, curr_scores):
        ''' Smooth the current prediction score
            by taking the average with previous scores
        '''
        self.scores_hist.append(curr_scores)
        DEQUE_MAX_SIZE = 2
        if len(self.scores_hist) > DEQUE_MAX_SIZE:
            self.scores_hist.popleft()

        if 1:  # Use sum
            score_sums = np.zeros((len(self.action_labels),))
            for score in self.scores_hist:
                score_sums += score
            score_sums /= len(self.scores_hist)
            # print("\nMean score:\n", score_sums)
            return score_sums

        else:  # Use multiply
            score_mul = np.ones((len(self.action_labels),))
            for score in self.scores_hist:
                score_mul *= score
            return score_mul

    def postHumanAction(self,face,face_acc,action,action_acc,position):

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%y %H:%M:%S")
        # dt_string = "10-03-2021 13:15:46"
        url = "http://localhost:5000/human-action/"
        data = {
            "classId":str("1"),
            "dateTime":str(dt_string),
            "face":str(face),
            "face_acc":str(face_acc),
            "action":str(action),
            "action_acc":str(action_acc),
            "position":str(str(position[0])+","+str(position[1]))
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(data), headers=headers)
        return " >>> [PRECESS]  person: %s %s,action: %s %s\n"%(face,face_acc,action,action_acc)
    
    def get_scores_image(self):
        action = "Unknow"
        action_acc = 0.00
        if self.scores is None:
            return action,action_acc

        max_id = max(self.scores)
        
        for i in range(0, len(self.action_labels)): 
            if max_id == self.scores[i]:
                action = self.action_labels[i]
                action_acc = self.scores[i]*100
                if action_acc < 80:
                    action = "Unknown"
                

        return action,action_acc

    def draw_scores_onto_image(self, img_disp,face_name,face_acc,position):


        if face_name == "Unknow":
            dx = int(position[0]) - int(self.re_data_px)
            dy = int(position[1]) - int(self.re_data_py)
            if (dx<6 or dx > -6) and (dy<6 or dy > -6) :
                face_name = self.re_data_face
            else:
                face_name = "Unknow"


        if self.scores is None:
            return

        max_id = max(self.scores)
        
        for i in range(0, len(self.action_labels)): 

            if max_id == self.scores[i]:
                # face_name = face_name
                face_acc = face_acc*100
                action = self.action_labels[i]
                action_acc = self.scores[i]*100
                # position = position

                txt_face_name = "Face: {}".format(face_name)
                txt_face_acc = "Accuracy: {:.2f}%".format(face_acc)
                txt_action = "Action: {}".format(action)
                txt_action_acc = "Accuracy: {:.2f}%".format(action_acc)
                txt_position = "Position: ({},{})".format(position[0],position[1])
                if action_acc > 10:
                    print(
                        self.postHumanAction(
                            face_name,
                            str("{:.2f}%".format(face_acc)),
                            action,str("{:.2f}%".format(action_acc)), 
                            position
                        )
                    )
                else:
                    print(" >>> [PRECESS]  Low Accuracy ...\n")   

                self.re_data_face = str(face_name)
                self.re_data_px = int(position[0])
                self.re_data_py = int(position[1])

        cv2.putText(img_disp, text=txt_face_name, org=(20, (40+120)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                    color=(0, 0, 255), thickness=2)
        cv2.putText(img_disp, text=txt_face_acc, org=(20, (40+160)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                    color=(0, 0, 255), thickness=2)  
        cv2.putText(img_disp, text=txt_action, org=(20, (40+200)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                    color=(0, 0, 255), thickness=2)
        cv2.putText(img_disp, text=txt_action_acc, org=(20, (40+240)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                    color=(0, 0, 255), thickness=2)
        cv2.putText(img_disp, text=txt_position, org=(20, (40+280)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                    color=(0, 0, 255), thickness=2)

