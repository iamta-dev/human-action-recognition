#!/bin/sh
python src/s6_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type video \
    --data_path data_test/tast-01.mp4 \
    --output_folder output