#!/bin/bash

psql -U student -d photon <<EOF
SELECT * FROM players;
EOF