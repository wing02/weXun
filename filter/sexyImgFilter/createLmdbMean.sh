
rm -rf ./data/lmdb/*
rm -rf ./data/mean/*
I=
TRAINLMDB=trainLmdb$I
TESTLMDB=testLmdb$I
TRAINMEAN=trainMean$I
TESTMEAN=testMean$I
DATA=data

TOOLS=/home/lab401/Project/caffe/build/tools
RESIZE_HEIGHT=32
RESIZE_WIDTH=32
TRAIN_DATA_ROOT=/home/lab401/Project/weXun/imgFilter/
LMDB=data/lmdb
MEAN=data/mean

$TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $DATA/train.txt \
    $LMDB/$TRAINLMDB

$TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $DATA/test.txt \
    $LMDB/$TESTLMDB


$TOOLS/compute_image_mean -backend=lmdb $LMDB/$TRAINLMDB  $MEAN/${TRAINMEAN}.binaryproto
$TOOLS/compute_image_mean -backend=lmdb $LMDB/$TESTLMDB  $MEAN/${TESTMEAN}.binaryproto

echo "Done."
