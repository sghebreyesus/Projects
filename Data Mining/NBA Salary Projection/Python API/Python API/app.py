from flask import Flask, request, jsonify
import os
import pickle
import json
import pandas as pd
         
app = Flask(__name__)

@app.route('/')
def hello():
  
    return jsonify(
        {'Tittle':'NBA Salary Prediction',
         'Members':['Samuel','Lincoln','Randy','Simin']

        })


@app.route('/api/predict', methods=['POST'])
def run_model():
    request_data = request.get_json()
    
    efg = request_data['efgpercentage'].replace("$", "").replace("%", "")

    print(type(request_data['age']))
    loaded_model = pickle.load(open('nbamodel.pkl', 'rb'))

    pred = [[int(request_data['age']),
               int(request_data['g']),
               int(request_data['gs']),
               float(request_data['mp']),
               float(request_data['fga']),
               float(request_data['threep']),
               float(request_data['twopa']),
               float(efg)/100,
               float(request_data['trb']),
               float(request_data['ast']),
               float(request_data['stl']),
               float(request_data['blk']),
               float(request_data['pf']),
               float(request_data['pts'])]]
    salary = loaded_model.predict(pred)
    
    
    print("Pred")
    print(pred)
    
    # load processed dataframe
    file = open('out.csv')
    df =  pd.read_csv(file)
    
    df_list = list(['Age', 'G', 'GS', 'MP', 'FGA', '3P', '2PA', 'eFG%', 'TRB', 'AST', 'STL', 'BLK', 'PF', 'PTS'])  
    
    new_listlen = (len(df_list))-1
    
    print("new_listen")
    print(new_listlen)
    
    quantile_list = [0]*new_listlen
     
    print(salary)
    
    pred_requested  = pred[0]
    
    for i in range(new_listlen):
        quantile_list[i] = df[df_list[i+1]].quantile([0.25,0.5,0.75], interpolation='nearest')
        quantile_list[i] = quantile_list[i].tolist()
     
        update_pred = pred_requested.copy()
    
    for i in range(new_listlen):
        r = pred_requested[i+1]
        a = quantile_list[i]
        for j in range(3):
            g = a[j]
            gg = g - (g * 0.12)
            if (r >= gg) and (r < g):
               update_pred[i+1] = g
    
    salary_after_recomendation = loaded_model.predict([update_pred])
    salary_after_recomendation
    
    improved_features = []
    improved_stats = []
    for i in range(len(pred_requested)):
        if (update_pred[i] != pred_requested[i]):
            improved_features.append(df_list[i])
            stat_list = [pred_requested[i],update_pred[i]]
            improved_stats.append(stat_list)
    
    
    list_improvements = []
    print('If you improve these stats:\n')
    for i in range(len(improved_features)):
        list_improvements.append('From {0} to {1} for {2}'.format(improved_stats[i][0],improved_stats[i][1], improved_features[i]))
        print('From {0} to {1} for {2}'.format(improved_stats[i][0],improved_stats[i][1], improved_features[i]))
        
    
    print('\nYour salary can increase from {0} to {1}'.format(salary[0], salary_after_recomendation[0]))  
    
    x = {
        "salary": salary[0],
        "improvements":list_improvements,
        "salary_increased": salary_after_recomendation[0]
        }
    print("print json", x)
 
    y = json.dumps(x)

    return y
 

port = int(os.environ.get('PORT', 7373))
app.run(debug=False, host='0.0.0.0', port=port)