import os
from sklearn.model_selection import KFold
import subprocess


def perform_cross_validation(data_folder, config_file_path, num_folds_cv):
    # Create a KFold object
    kfold_cv = KFold(n_splits=num_folds_cv, shuffle=True)

    # Iterate over the folds
    for fold, (train_index, val_index) in enumerate(kfold_cv.split(data_folder)):
        # Create directories for the current fold
        train_dir = f"train_data/fold_{fold}/train"
        val_dir = f"train_data/fold_{fold}/val"
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

        # Split the data into train and validation sets
        train_files = [data_folder[i] for i in train_index]
        val_files = [data_folder[i] for i in val_index]

        # Copy the training and validation files to the respective directories
        for file in train_files:
            os.replace(file, os.path.join(train_dir, os.path.basename(file)))
        for file in val_files:
            os.replace(file, os.path.join(val_dir, os.path.basename(file)))

        # Train the model using the current fold's configuration file
        config_file_fold = f"config_fold_{fold}.yml"
        subprocess.run(["copy", config_file_path, config_file_fold], shell=True)

        # Train the model using the current fold's configuration file
        subprocess.run(["rasa", "train", "--config", config_file_fold])

        # Evaluate the model on the validation set for the current fold
        model_path = f"models/fold_{fold}"
        subprocess.run(["rasa", "test", "--model", model_path, "--test-data", val_dir])

        # Clean up the directories after evaluation
        subprocess.run(["rmdir", "/s", "/q", train_dir], shell=True)
        subprocess.run(["rmdir", "/s", "/q", val_dir], shell=True)
        subprocess.run(["del", "/q", config_file_fold], shell=True)


# Specify the paths and parameters
data_folder_path = "data/"
config_file_path = "config.yml"
num_folds_cv = 5

# Get a list of training data files
training_data_files = [os.path.join(data_folder_path, file) for file in os.listdir(data_folder_path)]

# Perform cross-validation
perform_cross_validation(training_data_files, config_file_path, num_folds_cv)
