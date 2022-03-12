from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

dfs = []
for idx in ['0-999', '1000-1999', '2000-2999', '3000-3999', '4000-4999', '5000-5999', '6000-6999', '7000-7999', '8000-8999', '9000-9999']:
    df = pd.read_csv('data/{}.csv'.format(idx), skipinitialspace=True)
    dfs.append(df)
df_cryptopunks = pd.concat(dfs)
df_pred = pd.read_csv('data/pred.csv')
pred_mean = np.mean(df_pred['pred'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('CryptoPunks_NFT_Analysis_v3_Short.html')
    else:
        punk_id = request.form["punk_id"]
        target_punk = df_cryptopunks[df_cryptopunks['id']==int(punk_id)]
        punk_type = target_punk['type'].values[0]
        punk_acc = target_punk['accessories'].values[0]
        target_pred = df_pred[df_pred['punk_id']==int(punk_id)]
        if len(target_pred) == 0:
            pred = pred_mean
        else:
            pred = target_pred['pred'].values[0]
        pred = round(pred, 2)
        return render_template("CryptoPunks_NFT_Analysis_v3_Short.html", punk_id=punk_id,
                              punk_type=punk_type, punk_acc=punk_acc,
                              pred=pred)
    
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
