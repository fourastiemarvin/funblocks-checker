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
                  tools/Parser/Sources/funterm.mfe
                } > tmp.txt << EOF
EOF
                cat tmp.txt
                rm tmp.txt
                if [[ $2 == "log" ]]
                then
                  xdg-open tools/Parser/Sources/proof.html
                fi
                ;;
        "conf")
                {
                  ./maude-2.7-hooks-linux/maude++ \
                  maude-2.7-hooks-linux/MFE-mfe-2.7/src/mfe.maude \
                  tools/Parser/Sources/funconf.mfe
                } > tmp.txt << EOF
EOF
                cat tmp.txt
                rm tmp.txt
                ;;
esac
