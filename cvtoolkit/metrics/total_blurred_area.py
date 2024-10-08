import logging

import numpy as np


logger = logging.getLogger(__name__)


class TotalBlurredArea:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

    def update_statistics_based_on_masks(self, true_mask, predicted_mask):
        """
        Computes statistics for a given pair of binary masks.

        Parameters
        ----------
        true_mask numpy array of shape (height, width)
        predicted_mask numpy array of shape (height, width)

        Returns
        -------

        """
        self.tp += np.count_nonzero(np.logical_and(true_mask, predicted_mask))
        self.fp += np.count_nonzero(np.logical_and(~true_mask, predicted_mask))
        self.tn += np.count_nonzero(np.logical_and(~true_mask, ~predicted_mask))
        self.fn += np.count_nonzero(np.logical_and(true_mask, ~predicted_mask))

    def get_statistics(self):
        """
        Return statistics after all masks have been added to the calculation.

        Computes precision, recall and f1_score only in the end since it is redundant to
        do this intermediately.

        Returns
        -------

        """
        precision = (
            round(self.tp / (self.tp + self.fp), 3) if self.tp + self.fp > 0 else None
        )
        recall = (
            round(self.tp / (self.tp + self.fn), 3) if self.tp + self.fn > 0 else None
        )
        f1_score = (
            round(2 * precision * recall / (precision + recall), 3)
            if precision and recall
            else None
        )

        return {
            "true_positives": self.tp,
            "false_positives": self.fp,
            "true_negatives": self.tn,
            "false_negatives:": self.fn,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }
