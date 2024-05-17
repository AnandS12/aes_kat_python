# aes_kat_python
Python script for Kat generation of aes in different modes\

prerequisite::\
pip install pycryptodome\
\
\
command::\
python3 tools/simrun/aes_mode_kat.py \<mode> \<kat_count> \<seurity_level> 

Examples:: \
 python3 tools/simrun/aes_mode_kat.py OFB 120 128\
 python3 tools/simrun/aes_mode_kat.py CFB 120 128\
 python3 tools/simrun/aes_mode_kat.py CTR 120 128\
 python3 tools/simrun/aes_mode_kat.py OFB 120 128\
 python3 tools/simrun/aes_mode_kat.py OFB 120 128

