'''Naive Bayesian Classifier

- version -
python=3.8.11

code by DeneV
'''

class NBC(object):
    '''Use Naive Bayesian Classifier to classify data into two classes
    
    Example:
        >>> # data = [[f11, f12, f13 ...], 
                      [f21, f22, f23 ...],
                        ... 
                     ]
        >>> model = NavieBayesian(data)
        >>> model.fit()
        >>> model.predict(f1, f2, f3 ...)

    Functions:
        fit()
        predict(probability=False, *features)
    '''

    def __init__(self, data):
        self._data = data 
        self._dict_1, self._dict_2 = self.init_dicts()
        self._class_1 = list(self._dict_1.keys())[0]
        self._class_2 = list(self._dict_2.keys())[0]
        
    def init_dicts(self):
        dict_1 = {}
        dict_2 = {}
        class_1 = None
        class_2 = None
        for i in range(len(self._data)):
            class_ = self._data[i][-1].lower()

            if class_1 is None:
                class_1 = class_
                dict_1[class_] = 0
                
            elif class_2 is None:
                if class_ != class_1:
                    dict_2[class_] = 0
                    return dict_1, dict_2

    def count_features(self, datas, dict):
        for data in datas:
            data = data.lower()
            if data in dict.keys():
                dict[data] += 1
            else:
                dict[data] = 1

    def fit(self):
        '''Train model with given data'''
        for i in range(len(self._data)):
            datas = self._data[i]
            if datas[-1].lower() in list(self._dict_1.keys()):
                self.count_features(datas, self._dict_1)
            if datas[-1].lower() in list(self._dict_2.keys()):
                self.count_features(datas, self._dict_2)
            
    def add_mp(self, feature, class_):
        print(f'*p({feature}/{class_}) = 0')
        choice = input('Do you want to add values? [Y/N]> ')
        if choice in ['Y', 'y']:
            print(' p is a prior estimate. (0<p<=1)')
            print(' m is weight given to prior.')
            p = float(input('- p > '))
            m = float(input('- m > '))
            return m*p, m
        else:
            return 0, 0

    def predict(self, *features, prob=False):
        '''Return the class of classification
        * prob=True; print probability of each class.
        * Probability with the strongest assumption on independence.

        Args:
            prob (boolean, optional): whether to print probability or not
            *features (str): features affecting prediction

        Returns:
            str: result of classification
        '''
        if not features:
            return None
        n_class_1 = self._dict_1[self._class_1]
        n_class_2 = self._dict_2[self._class_2]
        all = n_class_1 + n_class_2
        class_1 = n_class_1 / all
        class_2 = n_class_2 / all

        for feature in features:
            feature = feature.lower()

            if feature in self._dict_1.keys():
                class_1 = class_1 * (self._dict_1[feature] / n_class_1)
            else:
                mp, m = self.add_mp(feature, self._class_1)
                class_1 = class_1 * (mp / n_class_1 + m)

            if feature in self._dict_2.keys():
                class_2 = class_2 * (self._dict_2[feature] / n_class_2)
            else:
                mp, m = self.add_mp(feature, self._class_2)
                class_2 = class_2 * (mp / n_class_2 + m)
        
        if prob:
            p = class_1 + class_2
            class_1 /= p
            class_2 /= p
            print(f'p({self._class_1}) = {class_1:.3f}')
            print(f'p({self._class_2}) = {class_2:.3f}')

        if class_1 > class_2:
            return self._class_1
        else:
            return self._class_2

def sample_data():
    '''Sample data of playing tennis'''

    label = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'Play']
    data = [
        ['Sunny', 'Hot', 'High', 'Weak', 'No'],
        ['Sunny', 'Hot', 'High', 'Strong', 'No'],
        ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
        ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
        ['Sunny', 'Mild', 'High', 'Weak', 'No'],
        ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
        ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
        ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
        ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Strong', 'No'],
    ]
    return label, data

def test_module():
    '''Test module'''
    label, data = sample_data()
    cfr = NBC(data)
    cfr.fit()

    # Normal Data
    features = 'sunny', 'mild', 'high', 'strong'
    result = cfr.predict(*features)
    print(f'\n{features}\n=> {result}\n')
    
    # Unexpected Data
    features = 'sunny', 'mild', 'Noise'
    result = cfr.predict(*features)
    print(f'\n{features}\n=> {result}')
    
if __name__ == '__main__':
    test_module()