from sklearn.metrics import precision_recall_curve,auc,roc_auc_score,roc_curve,classification_report
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default="plotly_dark"
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
class Eval:
    """
    This Class is used to Evaluate a Trained Classifier Model. 
    
    Parameters:-
    -----------
    multiclass:- bool,
        Whether the problem is multiclass or not
        
    num_classes:- int,
        Used Only when multiclass=True
        
    classes:- A Dict mapping integer to class label
    """
    def __init__(self,multiclass=False,num_classes=2,classes={}):
        self.multiclass=multiclass
        self.num_classes=num_classes
        self.classes=classes
    def eval_metrics_binary(self,y_test,y_pred,p):
        """
        This Function Evaluates a Binary Classifier
        
        Parameters:-
        ------------
        y_test:- array of shape(n,)
        y_pred:- Predictions of Model to Evaluate(n,)
        p:-      Predicted Probablities (n,2)
        """
        


        precision,recall,_=precision_recall_curve(y_test,p)
        prc_auc=auc(x=recall,y=precision)

        fpr,tpr,_=roc_curve(y_test,p)
        roc_auc=roc_auc_score(y_test,p)

        fig=make_subplots(cols=2,subplot_titles=[f"ROC AUC: {np.round(roc_auc,2)}",f"AUC Precision Recall : {np.round(prc_auc,2)}"],)
        fig.add_trace(go.Scatter(x=fpr,y=tpr,mode="lines",line=dict(color="#56f700"),stackgroup=True),row=1,col=1)
        fig.add_trace(go.Scatter(x=recall,y=precision,stackgroup=True),row=1,col=2)
        fig['layout']['xaxis'].update(title_text="FPR")
        fig['layout']['xaxis2'].update(title_text="Recall")
        fig['layout']['yaxis'].update(title_text="TPR")
        fig['layout']['yaxis2'].update(title_text="Precision")
        fig.update_layout(showlegend=False)
        fig.show()


        print(classification_report(y_test,y_pred))
    def eval_metrics_multiclass(self,y_test,y_pred,p):
        """
        This Function Evaluates a Multi-Class Classifier
        
        Parameters:-
        ------------
        y_test:- array of shape(n,)
        y_pred:- Predictions of Model to Evaluate(n,)
        p:-      Predicted Probablities (n,num_classes)
        """
        colors=sns.color_palette('bright',n_colors=self.num_classes)
        fpr,tpr={},{}
        precision,recall={},{}
        for i in range(self.num_classes):
            fpr[i],tpr[i],_=roc_curve(y_test,p[:,i],pos_label=i)
            precision[i],recall[i],_=precision_recall_curve(y_test,p[:,i],pos_label=i)
        fig,ax=plt.subplots(ncols=2,figsize=(10,6))
        for i in range(self.num_classes):
            ax[0].plot(fpr[i],tpr[i],color=colors[i],linestyle='--',label=f"{self.classes[i]} Vs Rest")
            ax[1].plot(precision[i],recall[i],color=colors[i],linestyle='--',label=f"{self.classes[i]} Vs Rest")
        ax[0].legend(loc='best')
        ax[1].legend(loc='best')
        ax[0].set_title("ROC Curve")
        ax[1].set_title("Precision-Recall Curve")
        ax[0].set_xlabel("FPR")
        ax[0].set_ylabel("TPR")
        ax[1].set_xlabel("Precision")
        ax[1].set_ylabel("Recall")
        fig.set_facecolor('lightblue')
        fig.set_edgecolor('green')
        ax[0].set_facecolor('black')
        ax[1].set_facecolor('black')
        print(classification_report(y_test,y_pred))
    def get_metrics(self,y_test,y_pred,p):
        """
        This Function Evaluates a Multi-class Classifier
        
        Parameters:-
        ------------
        y_test:- array of shape(n,)
        y_pred:- Predictions of Model to Evaluate(n,)
        p:-      Predicted Probablities (n,2)
        """
        if self.multiclass:
            self.eval_metrics_multiclass(y_test,y_pred,p)
        else:
            self.eval_metrics_binary(y_test,y_pred,p)