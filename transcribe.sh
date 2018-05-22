#!/bin/bash

# for filename in /Users/yijiaxu/Desktop/prosody_AED/adult_segment_all/*.wav; do 
# 	/Users/yijiaxu/kaldi-trunk/src/online2bin/online2-wav-nnet3-latgen-faster \
# 	--online=false --do-endpointing=false \
# 	--frame-subsampling-factor=3 \
# 	--config=/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/conf/online.conf \
# 	--max-active=7000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=1.0 \
# 	--word-symbol-table=/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt \
# 	/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/final.mdl /Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/HCLG.fst \
# 	'ark:echo mom mom|' \
# 	'scp:echo mom '$filename'|' \
# 	'ark:|/Users/yijiaxu/kaldi-trunk/src/latbin/lattice-best-path --acoustic-scale=1.0 ark:- ark,t:|/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/utils/int2sym.pl -f 2- /Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt \
# 	>> /Users/yijiaxu/Desktop/prosody_AED/text'
# 	# play $filename -q
# 	# sleep 1	
# 	# sleep 1
# 	# sleep 1
# done 

/Users/yijiaxu/kaldi-trunk/src/online2bin/online2-wav-nnet3-latgen-faster \
--online=false --do-endpointing=false \
--frame-subsampling-factor=3 \
--config=/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/conf/online.conf \
--max-active=7000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=1.0 \
--word-symbol-table=/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt \
/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/final.mdl /Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/HCLG.fst \
'ark:echo '$3' '$3'|' \
'scp:echo '$3' '$1'|' \
'ark:|/Users/yijiaxu/kaldi-trunk/src/latbin/lattice-best-path --acoustic-scale=1.0 ark:- ark,t:|/Users/yijiaxu/kaldi-trunk/egs/aspire/s5/utils/int2sym.pl -f 2- /Users/yijiaxu/kaldi-trunk/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt' 
# >> '$2''
# echo $'\n' >> $2
 