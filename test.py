from action_predict import action_prediction
from pie_data import PIE
import os
import sys
import yaml
import tensorflow as tf



gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
tf.config.experimental.set_visible_devices(devices=gpus[0:1], device_type='GPU')


def test_model(saved_files_path=None, path_pie=None):

    with open(os.path.join(saved_files_path, 'configs.yaml'), 'r') as yamlfile:
        opts = yaml.safe_load(yamlfile)
    print(opts)
    model_opts = opts['model_opts']
    data_opts = opts['data_opts']
    net_opts = opts['net_opts']

    tte = model_opts['time_to_event'] if isinstance(model_opts['time_to_event'], int) else \
                model_opts['time_to_event'][1]
    data_opts['min_track_size'] = model_opts['obs_length'] + tte

    if model_opts['dataset'] == 'pie':
            imdb = PIE(data_path=path_pie)
            imdb.get_data_stats()
    else:
            raise ValueError("{} dataset is incorrect".format(model_opts['dataset']))

    method_class = action_prediction(model_opts['model'])(**net_opts)

    beh_seq_test = imdb.generate_data_trajectory_sequence('test', **data_opts)
    acc, auc, f1, precision, recall = method_class.test(beh_seq_test, saved_files_path)


if __name__ == '__main__':

    saved_files_path='./data/models/pie/PVIM/ckpt/'
    path_pie = '/data/xl/data/PIE_dataset'
    test_model(saved_files_path=saved_files_path,path_pie = path_pie)