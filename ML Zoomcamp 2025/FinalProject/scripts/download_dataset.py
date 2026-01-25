import tensorflow_datasets as tfds
from tqdm.auto import tqdm

print("Enterring download :")
my_data_dir = '../Data_tfds' 


""" download_config = tfds.download.DownloadConfig(
    download_mode=tfds.GenerateMode.REUSE_DATASET_IF_EXISTS,
    extract_dir=None,
    manual_dir=None,
    compute_stats=False
) 

(ds_train, ds_test), ds_info  = tfds.load('places365_small', split=['train','test'], 
                                            data_dir=my_data_dir,
                                            shuffle_files=True, 
                                            with_info=True, 
                                            as_supervised=True,
                                            download=True,
                                            download_config=download_config)

"""

(ds_train, ds_test), ds_info  = tfds.load('places365_small', split=['train','test'], 
                                            data_dir=my_data_dir,
                                            shuffle_files=True, 
                                            with_info=True, 
                                            as_supervised=True)

for item in tqdm(tfds.as_numpy(ds_train), desc="Loading Places365"):
    image = item["image"]
    label = item["label"]
    print(image.shape, label.shape)