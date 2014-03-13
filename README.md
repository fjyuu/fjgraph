# 研究用プログラム #

## 動作を確認した環境 ##

* Python 2.7.5
* CPLEX 12.5

## 依存モジュールのインストール ##

    $ pip install -r requirements.txt

## テスト ##

    $ python -m unittest discover -v -f

## ライブラリ ##

* `fjexperiment.py`
* `fjgraph.py`
* `fjutil.py`

## ランダムグラフアンサンブルを定義するファイル ##

本プログラムでは，ランダムグラフアンサンブルの定義をJSONファイルで記述します．以
下のファイルが見本です．

* `sample-ensemble/multi-graph.json`: 頂点数と辺数を指定（自己ループ多重辺を許す）
* `sample-ensemble/n-m-graph.json`: 頂点数と辺数を指定（自己ループ多重辺を許さない）
* `sample-ensemble/specified-degree-dist.json`: 次数分布を指定（自己ループ多重辺を許す）

次数分布は非負整数の配列で表します．次数分布が `[2, 4, 6]` だと，次数が0の頂点が
2個，次数が1の頂点が4個，次数が2の頂点が6個です．

## 実験スクリプト ##

* `vc_dist.py`
* `ip_lp.py`
* `prob_dist_min_vc.py`

### `vc_dist.py` ###

与えられたグラフアンサンブルにおける，

* IP-平均頂点被覆分布
* LP-平均頂点被覆分布

を実験的に求める．

実行例：

    # ヘルプ
    $ ./vc_dist.py --help

    # デフォルトパラメータで実行
    $ ./vc_dist.py ensemble.json

    # 試行回数：2000，gnuplot用結果出力ファイル名：result1
    $ ./vc_dist.py --trials 2000 --output result1 ensemble.json

### `ip_lp.py` ###

与えられたグラフアンサンブルに対して，

* LPで解いたときの1/2の個数の平均
* LPで解いたときの目的関数値 / IPで解いたときの目的関数値 の平均
* LP最適値の平均
* IP最適値の平均
* LP最適値とIP最適値が等しくなる確率
* LP最適値とIP最適値の差の平均

を実験的に求める．

実行例：

    # ヘルプ
    $ ./ip_lp.py --help

    # デフォルトパラメータで実行
    $ ./ip_lp.py ensemble.json

    # 試行回数：2000
    $ ./ip_lp.py  --trials 2000 ensemble.json

### `prob_dist_min_vc.py` ###

与えられたグラフアンサンブルに対して，

* IP-最小頂点被覆最適値がdelta以上の確率分布
* LP-最小頂点被覆最適値がdelta以上の確率分布

を実験的に求める．

実行例：

    # ヘルプ
    $ ./prob_dist_min_vc.py --help

    # デフォルトパラメータで実行
    $ ./prob_dist_min_vc.py ensemble.json

    # 試行回数：2000，gnuplot用結果出力ファイル名：result2
    $ ./prob_dist_min_vc.py --trials 2000 --output result2 ensemble.json

### `prob_dist_min_cut.py` ###

与えられたグラフアンサンブルに対して，

* 全域最小カット重みがdelta以上の確率分布
* s-t最小カット重みがdelta以上の確率分布

を実験的に求める．

実行例：

    # ヘルプ
    $ ./prob_dist_min_cut.py --help

    # デフォルトパラメータで実行
    $ ./prob_dist_min_cut.py ensemble.json

    # 試行回数：2000，gnuplot用結果出力ファイル名：result3
    $ ./prob_dist_min_cut.py --trials 2000 --output result3 ensemble.json

## ライセンス ##

MITライセンス
