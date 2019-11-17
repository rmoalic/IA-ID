Évalutation de la fonction de distance
======================================

HTTPWeb 
50000 flows
fichier défi

KNN avec 5 voisins

euclidean (default)
-------------------
```
accuracy 0.9780 time 9798ms  false_positive  117 false_negative  103 recall 0.9741 prec 0.9728 F1 0.9735 AUC 0.9903 name KNeighborsClassifier-0
accuracy 0.9786 time 10319ms false_positive  109 false_negative  105 recall 0.9744 prec 0.9741 F1 0.9743 AUC 0.9909 name KNeighborsClassifier-1
accuracy 0.9777 time 9392ms  false_positive  117 false_negative  106 recall 0.9737 prec 0.9727 F1 0.9732 AUC 0.9922 name KNeighborsClassifier-2
accuracy 0.9805 time 9194ms  false_positive  104 false_negative   91 recall 0.9770 prec 0.9757 F1 0.9763 AUC 0.9919 name KNeighborsClassifier-3
accuracy 0.9771 time 10086ms false_positive  133 false_negative   96 recall 0.9742 prec 0.9707 F1 0.9724 AUC 0.9924 name KNeighborsClassifier-4
```

manhattan
---------
```
accuracy 0.9840 time 12455ms false_positive   87 false_negative   73 recall 0.9813 prec 0.9799 F1 0.9806 AUC 0.9947 name KNeighborsClassifier-0
accuracy 0.9832 time 12640ms false_positive   94 false_negative   74 recall 0.9808 prec 0.9790 F1 0.9799 AUC 0.9940 name KNeighborsClassifier-1
accuracy 0.9843 time 14788ms false_positive   86 false_negative   71 recall 0.9818 prec 0.9803 F1 0.9811 AUC 0.9957 name KNeighborsClassifier-2
accuracy 0.9840 time 15440ms false_positive   81 false_negative   79 recall 0.9807 prec 0.9805 F1 0.9806 AUC 0.9946 name KNeighborsClassifier-3
accuracy 0.9860 time 12629ms false_positive   70 false_negative   70 recall 0.9831 prec 0.9831 F1 0.9831 AUC 0.9942 name KNeighborsClassifier-4
```

chebyshev
---------
```
accuracy 0.9788 time 7045ms  false_positive  102 false_negative  110 recall 0.9742 prec 0.9750 F1 0.9746 AUC 0.9918 name KNeighborsClassifier-0
accuracy 0.9780 time 7099ms  false_positive  124 false_negative   96 recall 0.9748 prec 0.9721 F1 0.9735 AUC 0.9911 name KNeighborsClassifier-1
accuracy 0.9766 time 7019ms  false_positive  136 false_negative   98 recall 0.9736 prec 0.9700 F1 0.9717 AUC 0.9905 name KNeighborsClassifier-2
accuracy 0.9780 time 7265ms  false_positive  118 false_negative  102 recall 0.9740 prec 0.9725 F1 0.9732 AUC 0.9910 name KNeighborsClassifier-3
accuracy 0.9760 time 8728ms  false_positive  135 false_negative  105 recall 0.9726 prec 0.9699 F1 0.9712 AUC 0.9929 name KNeighborsClassifier-4
```

canberra
--------
```
accuracy 0.9953 time 209805ms false_positive   40 false_negative    7 recall 0.9960 prec 0.9926 F1 0.9943 AUC 0.9989 name KNeighborsClassifier-0
accuracy 0.9963 time 226036ms false_positive   32 false_negative    5 recall 0.9969 prec 0.9940 F1 0.9955 AUC 0.9990 name KNeighborsClassifier-1
accuracy 0.9954 time 187710ms false_positive   36 false_negative   10 recall 0.9958 prec 0.9932 F1 0.9945 AUC 0.9983 name KNeighborsClassifier-2
accuracy 0.9974 time 194218ms false_positive   24 false_negative    2 recall 0.9979 prec 0.9959 F1 0.9969 AUC 0.9998 name KNeighborsClassifier-3
accuracy 0.9965 time 200992ms false_positive   29 false_negative    6 recall 0.9969 prec 0.9947 F1 0.9958 AUC 0.9993 name KNeighborsClassifier-4
```

braycurtis
----------
```
accuracy 0.9848 time 40238ms false_positive   73 false_negative   79 recall 0.9812 prec 0.9818 F1 0.9815 AUC 0.9946 name KNeighborsClassifier-0
accuracy 0.9838 time 34695ms false_positive   76 false_negative   86 recall 0.9799 prec 0.9809 F1 0.9804 AUC 0.9937 name KNeighborsClassifier-1
accuracy 0.9826 time 38383ms false_positive   91 false_negative   83 recall 0.9795 prec 0.9787 F1 0.9791 AUC 0.9933 name KNeighborsClassifier-2
accuracy 0.9849 time 35082ms false_positive   92 false_negative   59 recall 0.9834 prec 0.9803 F1 0.9818 AUC 0.9955 name KNeighborsClassifier-3
accuracy 0.9841 time 35311ms false_positive   92 false_negative   67 recall 0.9820 prec 0.9796 F1 0.9808 AUC 0.9956 name KNeighborsClassifier-4
```

minkowski p=4
-------------
```
accuracy 0.9779 time 17108ms false_positive  122 false_negative   99 recall 0.9743 prec 0.9720 F1 0.9731 AUC 0.9904 name KNeighborsClassifier-0
accuracy 0.9772 time 16464ms false_positive  133 false_negative   95 recall 0.9743 prec 0.9707 F1 0.9725 AUC 0.9910 name KNeighborsClassifier-1
accuracy 0.9785 time 18747ms false_positive  115 false_negative  100 recall 0.9751 prec 0.9738 F1 0.9745 AUC 0.9923 name KNeighborsClassifier-2
accuracy 0.9754 time 18030ms false_positive  132 false_negative  114 recall 0.9708 prec 0.9691 F1 0.9700 AUC 0.9893 name KNeighborsClassifier-3
accuracy 0.9790 time 18804ms false_positive  107 false_negative  103 recall 0.9750 prec 0.9747 F1 0.9749 AUC 0.9918 name KNeighborsClassifier-4

```

Conslusion
==========

Au vu des indicateurs, la fonction canberra est la meilleur. Mais elle est très lente, la fonction manhattan est moin bonne mais s'execute en un temps plus résonable.
Elle semble plus adapter à notre utilisation.

