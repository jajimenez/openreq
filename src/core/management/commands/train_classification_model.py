"""Train Classification Model command."""

import os
import pickle

from django.core.management.base import BaseCommand

import pandas as pd
from pandas import DataFrame

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    confusion_matrix, classification_report, accuracy_score
)

from core.models import ClassificationModel
from core.text import standardize_text


class Command(BaseCommand):
    """Django command to train an incident classification model."""

    def get_incidents(self) -> DataFrame:
        """Get the incidents data from the database.

        :return: Incidents data.
        :rtype: DataFrame
        """
        host = os.getenv("DB_HOST")
        db = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        connection = f"postgresql://{user}:{password}@{host}/{db}"

        return pd.read_sql(
            "SELECT C.username AS user, A.subject, A.description, "
            "B.name AS category FROM core_incident A "
            "LEFT JOIN core_category B ON A.category_id = B.id "
            "LEFT JOIN auth_user C on A.opened_by_id = C.id "
            "WHERE B.name IS NOT NULL "
            "ORDER BY A.id;",
            connection
        )

    def preprocess_data(self, incidents_df: DataFrame) -> DataFrame:
        """Preprocess the incidents data.

        :param nlp: Language model.
        :type nlp: Language
        :param incidents_df: Incidents data.
        :type incidents_df: DataFrame
        :return: Preprocessed data.
        :rtype: DataFrame
        """
        inc_df = incidents_df.copy(deep=True)
        inc_df["description"] = inc_df["description"].fillna("")

        inc_df["text"] = (
            inc_df["user"] +
            " " +
            inc_df["subject"] +
            " " +
            inc_df["description"]
        )

        inc_df = inc_df[["text", "category"]]
        inc_df.loc[:, "text"] = inc_df["text"].apply(standardize_text)

        return inc_df

    def split_data(self, incidents_df: DataFrame) -> tuple[DataFrame]:
        """Split the preprocessed incidents data.

        :param incidents_df: Preprocessed incidents data.
        :type incidents_df: DataFrame
        :return: Tuple containing 4 datasets: training features, test features,
        training labels, test labels.
        :rtype: tuple[DataFrame]
        """
        x = incidents_df["text"]
        y = incidents_df["category"]

        return train_test_split(x, y, test_size=0.2)

    def get_classification_model(self) -> Pipeline:
        """Get a pipeline that contains the classification model and a TFIDF
        vectorizer.

        :return: Pipeline object.
        :rtype: Pipeline
        """
        return Pipeline([
            ("tfidf", TfidfVectorizer()),
            ("svc", LinearSVC(dual=True, random_state=10))
        ])

    def evaluate_classification_model(
        self, cls_model: Pipeline, x_test: DataFrame, y_test: DataFrame
    ) -> tuple[str]:
        """Evaluate the classification model.

        :param cls_model: Classification model pipeline.
        :type cls_model: Pipeline
        :param x_test: Test features dataset.
        :rtype x_test: DataFrame
        :param y_test: Test labels dataset.
        :rtype y_test: DataFrame
        :return: Confusion matrix, classification report and accuracy score.
        :rtype: tuple[str]
        """
        # Predict the labels/categories of the test features
        y_pred = cls_model.predict(x_test)

        # Get the confusion matrix, the classfication report and the accuracy
        # score.
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred, zero_division=0.0)
        ac = accuracy_score(y_test, y_pred)

        return cm, cr, ac

    def print_model_evaluation(
        self, cls_model: Pipeline, cm: str, cr: str, ac: str
    ):
        """Print the evaluation results.

        :param cls_model: Classification model pipeline.
        :type cls_model: Pipeline
        :param cm: Confusion matrix.
        :type cm: str
        :param cr: Classification report.
        :type cr: str
        :param ac: Accuracy score.
        :type ac: str
        """
        # Confusion matrix
        self.stdout.write(
            "\n" + self.get_bordered_title("Confusion matrix") + "\n\n"
        )

        self.stdout.write("Classes: " + ", ".join(cls_model.classes_))
        self.stdout.write()
        self.stdout.write(str(cm))

        # Classification report
        self.stdout.write(
            "\n" + self.get_bordered_title("Classification report") + "\n\n"
        )

        self.stdout.write(cr)

        # Accuracy score
        self.stdout.write(
            "\n" + self.get_bordered_title("Accuracy score") + "\n\n"
        )

        self.stdout.write(str(ac))
        self.stdout.write()

    def get_bordered_title(self, title: str) -> str:
        """Get a bordered title.

        :param title: Source title.
        :type title: str
        :return: Bordered title.
        :rtype: str
        """
        hor = "+" + ("-" * (len(title) + 2)) + "+"
        return f"{hor}\n| {title} |\n{hor}"

    def save_model(self, cls_model: Pipeline):
        """Save the classification model to the database.

        :param cls_model: Classification model pipeline.
        :type cls_model: Pipeline
        """
        # Serialize the model as bytes
        model = pickle.dumps(cls_model)

        # Get the first existing model (it should be the only one)
        m = ClassificationModel.objects.first()

        if m:
            m.model = model
        else:
            m = ClassificationModel(model=model)

        # Save (create or update) the model
        m.save()

    def handle(self, *args, **kwargs):
        """Run the command logic."""
        # Read database data
        self.stdout.write("Loading incidents data...")
        incidents_df = self.get_incidents()

        # Preprocess data
        self.stdout.write("Preprocessing incidents data...")
        incidents_df = self.preprocess_data(incidents_df)

        # Split dataset into training and test datasets
        x_train, x_test, y_train, y_test = self.split_data(incidents_df)

        # Get the classification model
        cls_model = self.get_classification_model()

        # Train the model
        self.stdout.write("Training the incidents classification model...")
        cls_model.fit(x_train, y_train)

        # Evaluate model
        cm, cr, ac = \
            self.evaluate_classification_model(cls_model, x_test, y_test)

        # Print the evaluation results
        self.print_model_evaluation(cls_model, cm, cr, ac)

        # Save model
        self.stdout.write("Saving the classification model...")
        self.save_model(cls_model)

        self.stdout.write(self.style.SUCCESS("Done"))
