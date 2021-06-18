import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rc, plot
# import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_recall_curve, classification_report
from sklearn.model_selection import train_test_split


def binary_class():
    true_answer_cvs = pd.read_csv('/Users/bmacha/PycharmProjects/djangoProject/media/gender_submission.csv')
    user_answer_cvs = pd.read_csv('/Users/bmacha/PycharmProjects/djangoProject/media/submission.csv')
    checked_field = 'Survived'
    true_answer = true_answer_cvs[checked_field]
    user_answer = user_answer_cvs[checked_field]
    class_true_values = 0
    class_false_values = 0
    for i in true_answer:
        if i == 0:
            class_false_values += 1
        else:
            class_true_values += 1
    if class_true_values * 1.5 < class_false_values or class_false_values * 1.5 < class_true_values:
        return binary_f(true_answer, user_answer)
    else:
        return binary_accuracy(true_answer, user_answer)


def binary_accuracy(true_answer, user_answer):
    trues = 0
    falses = 0
    for i in zip(true_answer, user_answer):
        if i[0] == i[1]:
            trues += 1
        else:
            falses += 1
    accuracy_ = trues / (trues + falses) * 100
    return accuracy_


def binary_f(true_answer, user_answer):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in zip(true_answer, user_answer):
        if i[0] == 1 and i[1] == 1:
            tp += 1
        elif i[0] == 0 and i[1] == 1:
            fp += 1
        elif i[0] == 0 and i[1] == 0:
            tn += 1
        else:
            fn += 1
    print(tp, tn, fp, fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    betta = 1
    f1 = (1 + betta * betta) * (precision * recall) / ((betta * betta * precision) + recall) * 100
    return f1
