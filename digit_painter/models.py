from django.db import models
import io
import pickle
import numpy as np


class Digit(models.Model):
    base64_data = models.TextField()
    category = models.TextField()
    entry_type = models.CharField(max_length=100)

    @staticmethod
    def serialize(arr):
        """
        Serialize an array using BytesIO
        :return:
        """
        # buffer = io.BytesIO()
        # np.save(buffer, arr)
        # return buffer.getvalue().decode("latin-1")
        return pickle.dumps(arr).decode("latin-1")

    def get_array(self):
        """
        Returns the array contained in base64_data
        :return:
        """
        return pickle.loads(self.base64_data.encode("latin-1"))

    def __str__(self):
        return "Digit: id: {} | category: {} | entry_type: {}".format(self.id, self.category, self.entry_type)
