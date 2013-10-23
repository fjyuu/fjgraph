#coding: utf-8

"便利な道具"

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
