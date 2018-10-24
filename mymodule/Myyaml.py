# -*- coding:utf-8 -*-


def load(ya):
    import yaml
    f = open('../password/' + ya + '.yml', 'r+')
    y = yaml.load(f)
    return y
