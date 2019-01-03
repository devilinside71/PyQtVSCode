import os
from subprocess import call
os.system("lupdate -recursive %cd% -target-language hu_HU -ts i18n/hu.ts")
