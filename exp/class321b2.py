#!/usr/bin/env python
import sys
import os
import subprocess
import traceback
import pdb
from bdb import BdbQuit
subprocess.Popen('find ./exp/.. -iname "*.pyc" -delete'.split())
sys.path.insert(0, '.')
os.nice(19)
from main import main
name = __file__.split('/')[-1].split('.')[0]  # name is filename

args = [
    '--name', name,
    '--dataset', 'charades_ego_video_plus_charades',
    '--print-freq', '1',
    '--arch', 'resnet50_3d',
    '--wrapper', 'actor_observer_with_classifier_wrapper',
    '--metrics', 'triplet_accuracy_metric;triplet_top5_metric;triplet_top10_metric;triplet_top50_metric;top1_metric',
    '--video-metrics', 'top1_metric;charades_map_metric',
    '--metric', 'actor_observer_classification_task_CharadesmAP',
    '--tasks', 'alignment_3d_task;actor_observer_classification_task;actor_observer_charades_task',
    '--actor-observer-classification-task-dataset', 'charades_ego_video_only_first',
    '--criterion', 'actor_observer_with_classifier_criterion',
    '--train-file', '/nfs.yoda/gsigurds/CharadesEgo_v1_train.csv;/nfs.yoda/gsigurds/Charades_v1_train.csv',
    '--val-file', '/nfs.yoda/gsigurds/CharadesEgo_v1_test.csv;/nfs.yoda/gsigurds/Charades_v1_test.csv',
    '--data', '/scratch/gsigurds/CharadesEgo_v1_rgb/;/scratch/gsigurds/Charades_v1_rgb/',
    '--pretrained',
    '--resume', '/nfs.yoda/gsigurds/caches/' + name + '/model.pth.tar' +
                ';/nfs.yoda/gsigurds/ai2/caches/i3d12b2/model_best.pth.tar',
    '--decay', '0.95',
    '--lr', '1e-5',
    '--classifier-weight', '1000.0',
    '--lr-decay-rate', '8',
    '--batch-size', '6',
    '--video-batch-size', '6',
    '--train-size', '1.0',
    '--val-size', '0.1',
    '--cache-dir', '/nfs.yoda/gsigurds/caches/',
    '--epochs', '50',
    '--workers', '8',
    #'--evaluate',
    '--share-selector',
]
sys.argv.extend(args)
try:
    main()
except BdbQuit:
    sys.exit(1)
except Exception:
    traceback.print_exc()
    print('')
    pdb.post_mortem()
    sys.exit(1)
