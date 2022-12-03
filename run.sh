#!/bin/sh

git clone https://github.com/giovannivz/us-midterms-2022-ap.git
git -C us-midterms-2022-ap pull --rebase

./convert-all.sh us-midterms-2022-ap
