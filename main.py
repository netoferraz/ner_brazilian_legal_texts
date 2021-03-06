import argparse
import os

from pyseqlab.features_extraction import FOFeatureExtractor, HOFeatureExtractor
from pyseqlab.fo_crf import FirstOrderCRF, FirstOrderCRFModelRepresentation
from pyseqlab.ho_crf import HOCRFAD, HOCRFADModelRepresentation
from pyseqlab.hosemi_crf_ad import HOSemiCRFAD, HOSemiCRFADModelRepresentation

from kashgari.tasks.seq_labeling import BLSTMCRFModel

from crf import CRFModel
from embedding import EmbeddingModel

from utils import LENER_DATASET_DIR

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        type=str,
        required=True,
        choices=("FirstOrderCRF", "HOCRFAD", "HOSemiCRFAD", "BLSTMCRF"),
    )
    parser.add_argument(
        "--method", type=str, required=True, choices=("CRF", "EMBEDDING")
    )

    args = parser.parse_args()

    output_path = os.path.join(os.path.dirname(__file__), "output")

    model = None

    if args.method == "CRF":

        if args.model == "FirstOrderCRF":

            model = CRFModel(
                FirstOrderCRF,
                FirstOrderCRFModelRepresentation,
                FOFeatureExtractor,
                output_path,
            )

        elif args.model == "HOCRFAD":

            model = CRFModel(
                HOCRFAD, HOCRFADModelRepresentation, HOFeatureExtractor, output_path
            )

        elif args.model == "HOSemiCRFAD":

            model = CRFModel(
                HOSemiCRFAD,
                HOSemiCRFADModelRepresentation,
                HOFeatureExtractor,
                output_path,
            )

        else:

            raise Exception(
                "Model unknown for CRF. Please use FirstOrderCRF, HOCRFAD or HOSemiCRFAD"
            )

    elif args.method == "EMBEDDING":

        if args.model == "BLSTMCRF":

            model = EmbeddingModel(BLSTMCRFModel)

    if model is not None:
        model.train(epochs=60)
        model.evaluate("test")
