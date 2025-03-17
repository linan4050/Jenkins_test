#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Time       ：2024/7/18 17:18
# Author     ：author lin3
"""
import re

a = '1 packets transmitted, 1 received, 0% packet loss, time 0ms'
math_delay_data = re.search(r'[0-9] packets.*ms', a).group()
print(math_delay_data)
