# LayoutLand
## by Jeff Weekley and Montana Fowler
### CMPM 202 Final Project Winter 2020


#### TODO
- put jeff's python code for histagrams in
- put all of jeffs new images in to retrain
- maybe integrate crop.py and run_model.py
- make run model work on a series of images
- run classifier in the UI

#### DONE
- retrain to icons that we are dealing with 
- get training to work for github repo
- put in new crop dimensions for iphone ten sent by jeff
- make screenshot upload go into crop.py
- gather new images for master list

#### Notes
this runs the trained model
python run_model.py --image cart.png
python run_model.py --image ..\data\jeff\A0.jpg


this trained the model on just the airplane and add icons
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/

this one i got to train on selected properly with enough iterations
python retrain.py --image_dir training_images_selected/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 1000--learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2000  --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/

this was the og train call on all the default folders
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/