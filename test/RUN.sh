echo "TICA---------------------------------" > log
rm tica_model.pkl tica_trajs.h5
msmb tICA -i diheds/  --out tica_model.pkl   --transformed tica_trajs.h5  --n_components 4 >> log

#watch with
#python plot_tica.py


rm labeled_trajs.h5 
echo "KMEANS----------------------------------" >>log
msmb MiniBatchKMeans -i tica_trajs.h5   --transformed labeled_trajs.h5  --n_clusters 5 >>log
python plot_labeled.py > MSMBmembership.dat


