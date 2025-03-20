from cvtoolkit.datasets.yolo_labels_dataset import YoloLabelsDataset

test_label_folder = "tests/data/labels"
img_shape = [1280, 720]


class TestYoloDataset:

    yolo_dataset: YoloLabelsDataset = YoloLabelsDataset(
        folder_path=test_label_folder, image_area=img_shape[0] * img_shape[1]
    )

    def test_init(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.get_filtered_labels()
        assert len(filtered_labels.keys()) == 2
        assert sum(len(labels) for labels in filtered_labels.values()) == 11

    def test_filter_by_class(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_class(
            class_to_keep=0
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 8

        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_class(
            class_to_keep=10
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 0

    def test_filter_by_class_list(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_class(
            class_to_keep=[3, 4]
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 2

    def test_filter_by_size(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_size(
            size_to_keep=[200, 400]
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 3

    def test_filter_by_size_perc(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_size_percentage(
            perc_to_keep=[0.0002, 0.0004]
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 4

    def test_filter_by_conf(self):
        self.yolo_dataset.reset_filter()
        filtered_labels = self.yolo_dataset.filter_by_confidence(
            conf_to_keep=0.8
        ).get_filtered_labels()
        assert sum(len(labels) for labels in filtered_labels.values()) == 6
