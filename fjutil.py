#!/usr/bin/env python
#coding: utf-8
from __future__ import print_function
import sys

class ProgressBar(object):
    def __init__(self, label = "Progress", bar_length = 40,
                 slug = "#", space = " "):
        self.label = label
        self.bar_length = bar_length
        self.slug = slug
        self.space = space

    def write(self, percent):
        slugs = self.slug * int(round(percent * self.bar_length))
        spaces = self.space * (self.bar_length - len(slugs))
        sys.stdout.write("\r{label}: [{bar}] {percent}%".format(
            label   = self.label,
            bar     = slugs + spaces,
            percent = int(round(percent * 100))
        ))
        sys.stdout.flush()

    def begin(self):
        self.write(0.0)

    def end(self):
        self.write(1.0)
        sys.stdout.write('\n')

def printCounter(counter, format = "{} {}"):
    for item in sorted(counter.keys()):
        print(format.format(item, counter[item]))
