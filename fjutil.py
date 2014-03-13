#coding: utf-8

"便利な道具"

# Copyright (c) 2013 Yuki Fujii
# Licensed under the MIT License

from __future__ import division, print_function
import sys


class ProgressBar(object):
    "プログレスバー"

    def __init__(self, label="Progress", bar_length=40, slug="#", space=" "):
        self.label = label
        self.bar_length = bar_length
        self.slug = slug
        self.space = space

    def write(self, percent):
        slugs = self.slug * int(round(percent * self.bar_length))
        spaces = self.space * (self.bar_length - len(slugs))
        sys.stdout.write("\r{label}: [{bar}] {percent}%".format(
            label=self.label,
            bar=slugs + spaces,
            percent=int(round(percent * 100))
        ))
        sys.stdout.flush()

    def begin(self):
        sys.stdout.write('\n')
        self.write(0.0)

    def end(self):
        self.write(1.0)
        sys.stdout.write('\n\n')


def print_counter(counter, format="{} {}"):
    "カウンターを標準出力に書き出す"
    for item in sorted(counter.keys()):
        print(format.format(item, counter[item]))


def output_counter(counter, file, format="{} {}"):
    "カウンターをファイルに書き出す"
    for item in sorted(counter.keys()):
        file.write(format.format(item, counter[item]))
        file.write("\n")


def load_json_file(file):
    "jsonファイルを読み込む"
    import json
    f = open(file, "r")
    ret = json.load(f)
    f.close()
    return ret


def frange(start, stop, step):
    "stepが小数でも大丈夫なrange"
    while (step > 0 and start < stop) or (step < 0 and stop < start):
        yield start
        start += step


def cumulative_prob_dist(prob_dist, step=1):
    "確率分布から累積確率分布（x以上の確率の分布）を求める"

    cumulative_prob_dist = {}
    key_max = max(prob_dist.keys())
    sum_prob = 0.0
    for x in frange(key_max, 0, - step):
        if x in prob_dist:
            sum_prob += prob_dist[x]
        cumulative_prob_dist[x] = sum_prob
    cumulative_prob_dist[key_max + step] = 0

    return cumulative_prob_dist


def fillup_dist(dist, start=None, stop=None, step=1, fill=0.0):
    """分布を表すdistを補完する

    distが，startからstopまでの数をキーとして持っていなかった場合，
    fillで初期化する．
    """
    if start == None:
        start = min(dist.keys())
    if stop == None:
        stop = max(dist.keys())
    for key in frange(start, stop, step):
        if key not in dist:
            dist[key] = fill
    return dist


def str2float(*floats):
    """文字列を浮動小数点に変換する

    例：

    '1.1' -> 1.1
    '2e2' -> 200.0
    '2e'  -> 2.0
    """
    ret = []
    for value in floats:
        striped = value.rstrip("e")
        ret.append(float(striped))

    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)
