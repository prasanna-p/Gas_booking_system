#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 17:58:31 2019

@author: prasanna
"""
from projectmain import create_app

app = create_app()

if __name__=='__main__':
    app.run(debug=True)
    