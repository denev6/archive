"""Compute Polynomial Regression and Mean Squared Error, 
   and also provide visible graph.

- Version -
python = 3.8.11
numpy = 1.20.3
scikit-learn = 0.24.2
matplotlib = 3.4.2

code by DeneV
"""

import numpy as np
import matplotlib.pyplot as plt

class Regression(object):
    """Functions for Linear and Polymonial Regression.

    Examples:
        >>> x = [0, 1, 1, 2, 4, 5, 6, 7, 8, 10, 13]
        >>> y = [0, 1, 2, 4, 6, 7, 8, 10, 11, 13, 11]
        >>> reg = Regression(x, y, 3)
        >>> function = reg.get_function()
        >>> MSE = reg.get_MSE()
        
    Functions:
        arrange_x(),\n
        get_weights(X, Y),\n
        get_function(),\n
        predict_y(x_value, weights=None),\n
        list_predicted_y(x_values, weights=None),\n
        get_MSE(X=None, Y=None, weights=None),\n
        get_kFoldCV(k)\n
        get_LOOCV(),\n
        show_graph(title=None, second=None)
    """

    def __init__(self, X, Y, degree=1):
        self._degree = degree
        self._X = X
        self._Y = Y
        self._weights = self.get_weights()

    def arrange_x(self, X=None):
        """Make a new X-matrix for Matrix multiplication

        Args:
            X (list, optional): list of x-values
        
        Returns:
            list: (number of data)x(degree of function) X-matrix
        """
        if X is None:
            X = self._X
        X_ = []
        for i in X:
            temp = []
            for d in range(self._degree+1):
                temp.append(i**d)   
            X_.append(temp)
        return X_

    def get_weights(self, X=None, Y=None):
        """Return weights of function

        Args:
            X (list, optional): list of x-values
            Y (list, optional): list of {y-values|x}
        
        Returns:
            list: list of weights
        """
        if X is None:
            X = self._X
        if Y is None:
            Y = self._Y
        X = self.arrange_x(X)
        X = np.array(X)
        Y = np.array(Y)
        XT = np.transpose(X)
        A = np.dot(XT, X)
        invA = np.linalg.inv(A)
        b = np.dot(XT, Y)
        w = np.dot(invA, b)
        return w

    def get_function(self):
        """Return function with weight
        
        Returns:
            str: line of function with y and x^n
        """
        weights = list(map(str, self._weights))
        weights[1] = f'{weights[1]}x'
        if len(weights) > 2:
            for i in range(2, len(weights)):
                weights[i] = f'{weights[i]}x^{i}'
        return f'y = sum({weights})'
    
    def predict_y(self, x, weights=None):
        """Predict y-value of specific x-value
        
        Args:
            x (int, float): x-value to predict
            weights (list, optional): weights of regression function

        Returns:
            float: y-value
        """
        if weights is None:
            weights = self._weights
        temp = [weights[i] * (x**i) for i in range(len(weights))]
        y = sum(temp)
        return y   

    def list_predicted_y(self, X, weights=None):
        """Predict y-values of x-values
        
        Args:
            X (list): x-values to predict
            weights (list, optional): weights of regression function

        Returns:
            list: list of predicted y-values
        """
        if weights is None:
            weights = self._weights
        Y = []
        for x in X:
            y = self.predict_y(x, weights)
            Y.append(y)
        return Y
        
    def get_MSE(self, X=None, Y=None, weights=None):
        """Retrun Mean Squared Error

        Args:
            X (list, optional): x-values of test set
            Y (list, optional): y-values of test set
            weights (list, optional): weights of regression function
        
        Returns:
            float: Mean Squared Error
        """
        if X is None:
            X = self._X
        if Y is None:
            Y = self._Y
        if weights is None:
            weights = self._weights
        Y_ = self.list_predicted_y(X, weights)
        sum_error = 0
        for i in range(len(X)):
            sum_error += (Y[i] - Y_[i]) ** 2
        MSE = sum_error / len(X)
        return MSE
    
    def get_kFoldCV(self, k):
        """Returns k-Fold Cross Validation result

        Args:
            k (int): split data into (k-1) training set and 1 test set
                     if k is max, return LOOCV.

        Returns:
            float: result of CV
        """
        if k == 'max':
            k = len(self._Y)
        MSEs = []
        index = len(self._Y) // k
        for i in range(k):
            # test_set
            if i == (k-1):
                test_X = self._X[i*index:]
                test_Y = self._Y[i*index:]
                training_X = self._X[:i*index]
                training_Y = self._Y[:i*index]
            else:
                test_X = self._X[i*index:(i+1)*index]
                test_Y = self._Y[i*index:(i+1)*index]
                training_X = self._X[:i*index] + self._X[(i+1)*index:]
                training_Y = self._Y[:i*index] + self._Y[(i+1)*index:]
            temp_w = self.get_weights(training_X, training_Y)
            temp_MSE = self.get_MSE(test_X, test_Y, temp_w)
            MSEs.append(temp_MSE)
        CV = np.mean(MSEs)
        return CV

    def show_graph(self, dot=True, func=True, title=None, second=None):
        """Show scattered data and function graph

        Args:
            title (str, optional): title of the coordinate plane
            second (int, optional): second to show the table

        Example:
            >>> # show 5 second
            >>> reg.show_graph(second=5)
            >>> # open until the user close
            >>> reg.show_graph()
        """
        if dot is True:
            X = np.array(self._X)
            Y = np.array(self._Y)
            plt.scatter(X, Y, color='r')
        if func is True:
            x_ = [x_value for x_value in range(self._X[0]-3, self._X[-1]+3)]
            y_ = self.list_predicted_y(x_)
            plt.plot(x_, y_, linestyle='-')
        if title:
            plt.title(title)
        if second:
            plt.show(block=False)
            plt.pause(second)
            plt.close()
        else:
            plt.show()


def test_module():
    """Test functions of Regrssion()"""
    # data
    x = [2, 3, 6, 7, 8, 10, 14, 15, 16, 17]
    y = [2, 4, 4, 9, 10, 6, 10, 13, 18, 14]
    print('Data')
    print('x =', x)
    print('y =', y)
    
    # init weight of Linear Regression
    linear_reg = Regression(x, y)

    print('\n Case 1 : linear regression')
    try:
        linear_func = linear_reg.get_function()
        print(linear_func)
    except Exception as exp:
        print('Case 1 failed:', exp)
    
    # init weight of polynomial regression
    cubic_reg = Regression(x, y, 3)

    print('\n Case 2 : polynomial regression -cubic function')
    try:
        cubic_func = cubic_reg.get_function()
        print(cubic_func)
    except Exception as exp:
        print('Case 2 failed:', exp)
    
    print('\n Case 2-1 : predict y-value')
    try:
        x_value = 14
        y_value = cubic_reg.predict_y(x_value)
        print(f'x = {x_value};           y = {y[x.index(x_value)]}')
        print(f'x = {x_value}; predicted_y = {y_value}')
    except Exception as exp:
        print('Case 2-1 failed:', exp)
    
    print('\n Case 2-2 : get MSE')
    try:
        MSE = cubic_reg.get_MSE(x, y)
        print(f'MSE = {MSE}')
    except Exception as exp:
        print('Case 2-2 failed:', exp)
    
    print('\n Case 2-3 : show graph')
    try:
        cubic_reg.show_graph(title='Test', second=3)
    except Exception as exp:
        print('Case 2-3 failed:', exp)

    print('\n Case 3 : get k-FoldCV(k-Fold Cross Validation)')
    try:
        CV = cubic_reg.get_kFoldCV(5)
        print(f'MSE = {CV}')
    except Exception as exp:
        print('Case 3 failed:', exp)

    print('\n Test complete. \n')


if __name__ == '__main__':
    # start module test
    test_module()