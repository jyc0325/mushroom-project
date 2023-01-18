import fiftyone as fo

# The directory containing the source images
data_path = "./created_images/1-1"

# The path to the COCO labels JSON file
labels_path = "./created_images/1-1/cocodata.json"

# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_type=fo.types.COCODetectionDataset,
    data_path=data_path,
    labels_path=labels_path,
)

if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows
    session = fo.launch_app(dataset)
    session.wait()