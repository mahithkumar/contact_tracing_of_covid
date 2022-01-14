
import os
from flask import Flask, request, render_template
import pandas as pd
from sklearn.cluster import DBSCAN

app = Flask(__name__)


@app.route('/')
def home():
    

    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
  if request.method == 'POST':
        variable=request.form['infectedperson']
        file = request.files['jsonfile'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static', filename)
        file.save(file_path)  
  def get_infected_names(input_name):
    df = pd.read_json(file_path)
    epsilon = 0.0018288 # a radial distance of 6 feet in kilometers
    model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
    df['cluster'] = model.labels_.tolist()

    input_name_clusters = []
    for i in range(len(df)):
        if df['id'][i] == input_name:
            if df['cluster'][i] in input_name_clusters:
                pass
            else:
                input_name_clusters.append(df['cluster'][i])
    
    infected_names = []
    for cluster in input_name_clusters:
        if cluster != -1:
            ids_in_cluster = df.loc[df['cluster'] == cluster, 'id']
            for i in range(len(ids_in_cluster)):
                member_id = ids_in_cluster.iloc[i]
                if (member_id not in infected_names) and (member_id != input_name):
                    infected_names.append(member_id)
                else:
                    pass
    return infected_names
  output=get_infected_names(variable)

  return render_template('index.html', prediction_text='infected persons are {}'.format(output))


if __name__ == "__main__":
    app.run(port=5000,debug=True)
