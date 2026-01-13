# Source - https://stackoverflow.com/a
# Posted by jakevdp, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-28, License - CC BY-SA 3.0

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import LeaveOneOut, cross_val_predict

x = np.array([[1,2],[3,4],[5,6],[7,8],[9,10]])             
y = np.array([12,13,19,18,15])
clf = LinearRegression().fit(x,y)
cv = LeaveOneOut(len(y))
for train, test in cv:
    x_train, y_train = x[train], y[train]
    x_test, y_test = x[test], y[test]
    clf.fit(x_train, y_train) # <--------------- note added line!
    y_pred_USING_x_test = clf.predict(x_test)
    y_pred_USING_x_train = clf.predict(x_train)
    print('y_pred_USING_x_test: ', y_pred_USING_x_test,
          'y_pred_USING_x_train: ', y_pred_USING_x_train)

print()
print(cross_val_predict(clf, x, y, cv=cv))
