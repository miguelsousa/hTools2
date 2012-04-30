# [h] hTools2.modules.opentype

import os

def clear_features(font):
    font.features.text = ''

def import_features(font, fea_path):
    # make features file
    features_text = ''
    if os.path.exists(fea_path):
        fea = open(fea_path,'r')
        fea_text = fea.readlines()
        for line in fea_text:
            features_text += line
        fea.close()
    # set features
    font.features.text = features_text

def export_features(font, fea_path):
    if os.path.exists(fea_path):
		fea = open(fea_path, "w")
		fea.write(font.features.text)
		fea.close()