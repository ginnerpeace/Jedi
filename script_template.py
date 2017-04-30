#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, re

printColor = '\033[0;32m'

def show_help():
    print('\033[1;33m')
    print('some helps')
    print('\033[1;32m')
    sys.exit(0)

def execute(args = []):
    try:
        print('excute')

    except Exception as e:
        print('\033[0;31mError!!!')
        print(Exception)
        print(e)
        print('\033[0m')
    finally:
        done()
        sys.exit(0)


def info(text = ''):
    print(printColor + text)

def done():
    print(printColor + 'Done.\033[0m')
    sys.exit(0)


def error(text = ''):
    print('\033[0;31m' + text + printColor)


def notice(text = ''):
    print('\033[0;33m' + text + printColor)

if __name__ == '__main__':
    args = sys.argv

    if '--help' in args or len(args) < 2:
        show_help()
    else:
        # 去除脚本文件名
        args.pop(0)
        execute(args)
