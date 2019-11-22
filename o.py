# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import dash_daq as daq
from dataclasses import dataclass # Python 3.7以上


@dataclass
class charge: # 電荷chargeのクラス　座標(x,y,z)，電荷q
        x : float = 0.0
        y : float = 0.0
        z : float = 0.0
        q : float = 0.0

# 点電荷Qa,Qb,Qc,Qdの生成
Qa = charge(2, 0, 2, 1)
Qb = charge(-2, 0, 2, 1)
Qc = charge(0, 0.75, 1.5, -0.5)
Qd = charge(0, 6, 1, -0.1)

# 55行・40列の格子状の座標が納まった配列
xAxis = np.linspace(-4, 4, 40)
yAxis = np.linspace(-3, 8, 55)
xGrid, yGrid = np.meshgrid(xAxis, yAxis)

def v_oppai(x, y):
    """
    座標(x,y)上の電位vを計算する
    """
    v_a = 10*Qa.q / np.sqrt( (x-Qa.x)**2 + (y-Qa.y)**2 + (0-Qa.z)**2 )
    v_b = 10*Qb.q / np.sqrt( (x-Qb.x)**2 + (y-Qb.y)**2 + (0-Qb.z)**2 )
    v_c = 10*Qc.q / np.sqrt( (x-Qc.x)**2 + (y-Qc.y)**2 + (0-Qc.z)**2 )
    v_z = 10*Qd.q / np.sqrt( (x-Qd.x)**2 + (y-Qd.y)**2 + (0-Qd.z)**2 )
    return v_a + v_b + v_c + v_z


# Dashのインスタンスappを生成
app = dash.Dash(__name__) 

# インスタンスappに、コンポーネント（グラフやスライダなど）を配置
app.layout = html.Div(children=[
    html.H1(children='おっぱい関数　物理学的アプローチ'),
    dcc.Graph(id='py-graph'),
    html.Div(id='a-charge-output'),
    dcc.Slider(id='a-charge', 
        min=0.5, max=1.5, step=0.1, value=1.0, 
        marks={i/10: '{:.1f}'.format(i/10) for i in range(5,16)},
        ),
    ],
    style={
        "width" : '80%',
        'display' : 'inline-block',
        'paddingLeft' : 50,
        'paddingRight' : 50,
        'boxSizing' : 'border-box',            
        }
)

@app.callback(
    dash.dependencies.Output('a-charge-output', 'children'),
    [dash.dependencies.Input('a-charge', 'value')])
def update_output(value):
    """
    現在の点電荷Qa,Qbの電荷を表示する
    """
    return '点Ａ・点Ｂの電荷：{:.1f} クーロン'.format(value)

@app.callback(
    dash.dependencies.Output('py-graph', 'figure'),
    [dash.dependencies.Input('a-charge', 'value')])
def update_py_graph(q_charge):
    """
    点電荷Qa,Qbの電荷の大きさにより、ぱいグラフを再描画
    """
    Qa.q = Qb.q = q_charge # 点電荷Qa,Qbの電荷qに、電荷q_chargeを設定
    v = v_oppai(xGrid, yGrid) # 55行・40列の格子状の座標の電位vを計算
    # プロットデータの作成
    lines = []
    line_marker = dict(color='lightpink', width=3)
    # x軸方向の電位vの線
    for i, j, k in zip(xGrid, yGrid, v):
        lines.append(go.Scatter3d(x=i, y=j, z=k, mode='lines', line=line_marker))
    # ｙ軸方向の電位vの線
    for i, j, k in zip(xGrid.T, yGrid.T, v.T): # 転置.Tがポイント
        lines.append(go.Scatter3d(x=i, y=j, z=k, mode='lines', line=line_marker))
    # 点電荷Qa,Qb
    lines.append(go.Scatter3d(x=[Qa.x, Qb.x], y=[Qa.y, Qb.y], z=[Qa.z, Qb.z], 
        mode='markers', marker={'size':(100*Qa.q, 100*Qb.q), 'color':'red'})
    ),
    #  点電荷Qc,Qd
    lines.append(go.Scatter3d(x=[Qc.x, Qd.x], y=[Qc.y, Qd.y], z=[Qc.z, Qd.z],
        mode='markers', marker={'size':(50, 10), 'color':'blue'})
    ),

    return {
        'data': lines,
        'layout': go.Layout(
            height=1000, width=1500, 
            showlegend=False,
            title='電位的おっぱい',
            scene={'zaxis': {'title': 'V', }}
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True)
