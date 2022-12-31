import pandas as pd
from sklearn.metrics import f1_score
import numpy as np
from scipy.stats import ttest_ind
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def get_bootstrap(data: pd.DataFrame, pred_name: str, target_name: str, metric: object, bootstrap_iterations: int):

    np.random.seed(42)

    scores = pd.DataFrame(data={
        "metric": 0.0,
    }, index=range(bootstrap_iterations))

    for i in range(bootstrap_iterations):
        sample = data.sample(frac=1.0, replace=True)
        scores.loc[i, "metric"] = metric(sample[pred_name], sample[target_name])
    return scores


def commit_ttest(metric_a: pd.Series, metric_b: pd.Series, alpha: float):

    pvalue = ttest_ind(metric_a, metric_b, alternative="less").pvalue

    logger.info(f"pvalue: {pvalue:g}")
    if pvalue < alpha:
        logger.info("Reject null hypothesis.")
    else:
        logger.info("Accept null hypothesis.")


if __name__ == "__main__":

    model_a_result = pd.read_csv('../data/lr_pred_target.csv')
    model_b_result = pd.read_csv('../data/rf_pred_target.csv')

    model_a_boot_res = get_bootstrap(model_a_result, 'prediction', 'TX_FRAUD', f1_score, 1000)
    model_b_boot_res = get_bootstrap(model_b_result, 'prediction', 'TX_FRAUD', f1_score, 1000)

    commit_ttest(model_a_boot_res['metric'], model_b_boot_res['metric'], 0.001)
