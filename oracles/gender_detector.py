import numpy as np
import pandas as pd
import pickle
import io

class GenderDetector:
    
    def __init__(self, freqDict,countStatics):
        self.freqDict = freqDict # freqDict is a dict contains frequence of char 
        self.countStatics = countStatics
        
    def detect(self, name): # no family name in name please
        female_index = 0;
        male_index = 0
        
        for c in name:
            if c in self.freqDict:
                female_index += self.freqDict[c]['F']
                male_index   += self.freqDict[c]['M']
            else:
                print('no char for {}',c)
        
        fScore = female_index * self.countStatics['M']/self.countStatics['F'];
        mScore = male_index
        return (fScore,mScore, fScore/(fScore+mScore + 0.00000001))

    @classmethod
    def load_from_file(cls,file_name):
        with open(file_name, 'rb') as in_s:
            gd=pickle.load(in_s)
            return gd

    def dump_as(self, file_name):
        with open(file_name, 'wb') as out_s:
            pickle.dump(self,out_s)
    
    @classmethod
    def create_from_data_file(cls,csv_data):
        ng = pd.read_csv(csv_data)
        d,gc = GenderDetector.train_model(ng)
        gd = GenderDetector(d,gc)
        return gd

    @classmethod
    def train_model(cls, ngc):
        dict = {} # 统计每个字在男女里面出现的次数
        genderCount = {'F':0,'M':0}
        for p in ngc.values:
            if pd.isnull(p[0]) or len(p[0]) > 3:
                continue
        
            if p[1] != 'M' and p[1] != 'F':
                continue
            
            # 姓不要参与统计
            for char in p[0][1:]:
                pair = {'F':0, 'M':0}
                if char in dict:
                    pair = dict[char]
        
                pair[p[1]] = pair[p[1]] + 1
                dict[char] = pair
            
            genderCount[p[1]] = genderCount[p[1]] + 1

        return (dict,genderCount)