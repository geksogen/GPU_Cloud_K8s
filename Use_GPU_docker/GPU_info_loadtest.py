import tensorflow as tf
from tensorflow.python.client import device_lib

print(tf.test.is_built_with_cuda()) #проверка работы CUDA

print(tf.sysconfig.get_build_info(), "\n") #static numbers
sys_details = tf.sysconfig.get_build_info()
print('Prescribed CUDA version:', sys_details["cuda_version"]) #версия CUDA
print('Prescribed cuDNN version:', sys_details["cudnn_version"], "\n") #версия CUDNN

print(tf.reduce_sum(tf.random.normal([1000, 1000]))) #проверка тензоров
print(tf.config.list_physical_devices('GPU'), "\n") #проверка доступных видеокарт/GPU

print(device_lib.list_local_devices())
