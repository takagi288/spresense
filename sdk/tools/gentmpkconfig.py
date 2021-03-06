#!/usr/bin/env python3
############################################################################
# tools/gentmpkconfig.py
#
#   Copyright 2018 Sony Semiconductor Solutions Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of Sony Semiconductor Solutions Corporation nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
############################################################################

import os
import sys
import glob

if len(sys.argv) < 2:
    print('output file not specified.', file=sys.stderr)
    sys.exit(1)

with open('Kconfig', 'r') as f:
    buf = f.read()

if sys.argv[1] == '-':
    outfile = sys.stdout
else:
    outfile = open(sys.argv[1], 'w')

print(buf, file=outfile)

EXCLUDES = ['nuttx', 'apps', 'sdk']

# Search top of Kconfig in the same level directories

kconfigs = glob.glob('../*/Kconfig')

# Add kconfigs from user application
if 'SPRESENSE_HOME' in os.environ:
    myapp_root = os.environ['SPRESENSE_HOME']
    if os.path.isdir(myapp_root):
        kconfigs = kconfigs + glob.glob(os.path.join(myapp_root, "Kconfig"))

for c in kconfigs:
    dn = os.path.dirname(c).split('/')[-1]

    # Add Kconfig excpet nuttx, apps and sdk directories

    if dn not in EXCLUDES:
        print('source "%s"' % c, file=outfile)

outfile.close()
