# LayoutLand
## by Jeff Weekley and Montana Fowler
### CMPM 202 Final Project Winter 2020

#### Notes
this runs the trained model
python run_model.py --image cart.png

this trained the model on just the airplane and add icons
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/

this was the og train call on all the default folders
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/