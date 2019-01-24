# -*- coding: utf-8 -*-
"""Run lrelease"""

import os
import platform

if platform.system() == 'Windows':
    os.system("lrelease i18n/hu.ts")
