#
#make sure to pip install mir_eval


from mir_eval.separation import bss_eval_sources
<<<<<<< HEAD
from mir_eval.separation import evaluate


def evaluat(reference_sources, target_sources):
    return evaluate(reference_sources, target_sources) 


def evaluate_sources(reference_sources, estimated_sources):
=======

def evaluate_sources(reference_sources, target_sources):
>>>>>>> 86025c8f668dd0c7c2ab34ca566d9496ff75d107
    """
    Parameters: convert the .wav files into audio before inputting
    ----------
    reference_sources : np.ndarray, shape=(nsrc, nsampl)
        matrix containing true sources (must have same shape as
        estimated_sources)
    estimated_sources : np.ndarray, shape=(nsrc, nsampl)
        matrix containing estimated sources (must have same shape as
        reference_sources)
    Returns
    -------
    sdr : np.ndarray, shape=(nsrc,)
        vector of Signal to Distortion Ratios (SDR)
    sir : np.ndarray, shape=(nsrc,)
        vector of Source to Interference Ratios (SIR)
    sar : np.ndarray, shape=(nsrc,)
        vector of Sources to Artifacts Ratios (SAR)
    """
<<<<<<< HEAD
    sdr, sir, sar, perm = bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)
    return {
        'sdr': sdr,
        'sir': sir,
        'sar': sar,
        'perm': perm
    }


print('test')
=======
    sdr, sir, sar, _ = bss_eval_sources(reference_sources, target_sources, compute_permutation=False)
    return {
        'sdr': sdr,
        'sir': sir,
        'sar': sar
    }
>>>>>>> 86025c8f668dd0c7c2ab34ca566d9496ff75d107
