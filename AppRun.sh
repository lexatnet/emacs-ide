#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
VER=$(ls "${HERE}/usr/share/emacs/" | head -n 1)
export LD_LIBRARY_PATH=${HERE}/usr/lib/x86_64-linux-gnu/:$HERE/lib/x86_64-linux-gnu/:$HERE/usr/lib/:${HERE}/lib/:$LD_LIBRARY_PATH
export PATH=${HERE}/usr/sbin:${HERE}/usr/bin:$PATH
export EMACSPATH=${HERE}/usr/share/emacs/$VER/
export EMACSDATA=$EMACSPATH/etc
export EMACSDOC=$EMACSPATH/etc
export EMACSLOADPATH=$EMACSPATH/site-lisp:$EMACSPATH/lisp:$EMACSPATH/lisp/emacs-lisp
export INFOPATH=./local/share/info

"${HERE}"/usr/bin/python3 "${HERE}"/lexet/lexet.py "$@"
