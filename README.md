# LayoutLand
## by Jeff Weekley and Montana Fowler
### CMPM 202 Final Project Winter 2020


<img width="983" alt="screenshot1" src="https://user-images.githubusercontent.com/24569677/77204434-f1fe0900-6aaf-11ea-9fce-5e674d71023a.png">
<img width="980" alt="screenshot2" src="https://user-images.githubusercontent.com/24569677/77204437-f2969f80-6aaf-11ea-8031-06c9a983cb65.png">
<img width="977" alt="screenshot3" src="https://user-images.githubusercontent.com/24569677/77204438-f32f3600-6aaf-11ea-9e7f-5d19417f3697.png">

#### TODO
- collect layout information into database
- send screenshot form to more people to get more data
- possibly reveal histagrams when explaining AI
- add what are your most used apps on your front page? (optional)
- setup html template for the results to propagate
- make score javascript use forbidden pairs to dock points
- check new model with the apps that did poorly before and update their scores
- make it so you cant accidentally add more children
- maybe show in solution background how they got points
- add try again button
- 

#### DONE
- retrain to icons that we are dealing with 
- get training to work for github repo
- put in new crop dimensions for iphone ten sent by jeff
- make screenshot upload go into crop.py
- gather new images for master list
- maybe integrate crop.py and run_model.py
- make run model work on a series of images
- run classifier in the UI
- put jeff's python code for histagrams in
- checkin on video re: jeff
- put all of jeffs new images in to retrain
- build base for the javascript game UI wise
- write overleaf paragraphs for jeff
- checkin with jeff on overleaf UI
- make icons bigger 
- make them not leave but just grey out in the left
- check what top apps classify as to make it better
- write pseudocode
- put underlying heuristic AI backend in layout format
- get forbidden neighbors written into a file and passing json, for scoring
- collect images for more apps & add those in to retrain
- after testing is done remove text
- determine how the scoring happens
- make the solution show up in the solution box
- make score field
	- should I breakdown points?
- make score javascript count points of good apps by zones


#### Notes
https://apps.apple.com/us/story/id1484100916
most used apps of 2019
YouTube
Instagram
Snapchat
TikTok
Messenger
Gmail
Netflix
Facebook
Google Maps
Amazon
Spotify
DoorDash
WhatsApp
FaceApp
Uber
YOLO
Hulu
Venmo
Bitmoji
Google Chome

also some default apple apps:
Apple Maps
Messages
Mail
Safari
Camera
Photos
Phone
FaceTime
Music



this runs the trained model
python run_model.py --image cart.png
python run_model.py --image ..\data\jeff\C0.jpg

TO RUN SERVER
set FLASK_APP=layoutLand.py
flask run

python retrain.py --image_dir training_images_selected/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 1000 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2000 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck
python retrain.py --image_dir training_images_selected/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 4000 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2000 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck

this trained the model on just the airplane and add icons
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/

this one i got to train on selected properly with enough iterations
python retrain.py --image_dir training_images_selected/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 1000--learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2000  --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/

this was the og train call on all the default folders
python retrain.py --image_dir test/ --output_graph output/saved_model.pb --output_labels output/saved_model.pbtxt --how_many_training_steps 100 --learning_rate 0.30 --testing_percentage 25 --validation_percentage 25 --eval_step_interval 50 --train_batch_size 2 --test_batch_size -1 --validation_batch_size -1 --bottleneck_dir /tmp/bottleneck/


classify most common to see what happens
most used apps of 2019
YouTube
Instagram
Snapchat
TikTok
Messenger
Gmail
Netflix
Facebook
Google Maps
Amazon
Spotify
DoorDash
WhatsApp
FaceApp
Uber
YOLO
Hulu
Venmo
Bitmoji
Google Chome

also some default apple apps:
Apple Maps
Messages
Mail
Safari
Camera
Photos
Phone
FaceTime
Music