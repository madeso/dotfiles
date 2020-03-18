#!/bin/bash
grep $1 -i -r --include \*.cmake --include \CMakeLists.txt
