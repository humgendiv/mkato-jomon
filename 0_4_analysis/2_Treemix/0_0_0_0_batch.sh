./0_0_keep_fam.sh
./0_1_vcf2v4.2.sh
./0_1.1_noN.sh
./0_2_LD-pruning.sh
./0_3_make_clust.sh

#read -p "Hit enter(pops.clustの手直し終わったら): "

./0_4_vcf2treemix
./1_treemix.sh
./2_plot.sh