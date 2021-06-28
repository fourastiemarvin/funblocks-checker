#!/usr/bin/env bash

case $1 in
        "init")
                cd tools/Parser/Sources/FunBlockParser/
                swift run
                cd -
                ;;
        "term")
                {
                  ./maude-2.7-hooks-linux/maude++ \
                  maude-2.7-hooks-linux/MFE-mfe-2.7/src/mfe.maude \
                  CLI/funterm.mfe
                } > tmp.txt << EOF
EOF
                cat tmp.txt
                rm -f tmp.txt
                rm -f CLI/log.txt
                if [[ $2 == "log" ]]
                then
                  xdg-open tmp/proof.html
                fi
                ;;
        "conf")
                {
                  ./maude-2.7-hooks-linux/maude++ \
                  maude-2.7-hooks-linux/MFE-mfe-2.7/src/mfe.maude \
                  CLI/funconf.mfe
                } > tmp.txt << EOF
EOF
                cat tmp.txt
                rm -f tmp.txt
                rm -f CLI/log.txt
                ;;
esac
