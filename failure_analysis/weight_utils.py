import numpy as np
from scipy.stats import pearsonr



def compute_online_weight(
        kp_history,
        joint_history,
        window=20,
        ema_alpha=0.2,
        corr_weight=0.5,
        motion_weight=0.3,
        stability_weight=0.2
):
    """
    E13-C:
    Online Keypoint Reliability Weighting


    Args:
        kp_history:
            numpy array

            shape:
            (T, K, 3)

            T:
                temporal frames

            K:
                keypoints


        joint_history:

            numpy array

            shape:
            (T, joint_dim)


        window:

            temporal window size


        ema_alpha:

            EMA update factor


        corr_weight:

            joint-keypoint correlation contribution


        motion_weight:

            keypoint motion contribution


        stability_weight:

            temporal stability contribution


    Returns:

        weights:

            shape:

            (T,K)

    """



    # ===================================
    # E13-C online safety
    # kp history and joint history
    # may have one-frame delay
    # ===================================

    num_frames = min(
        kp_history.shape[0],
        joint_history.shape[0]
    )

    num_kp = kp_history.shape[1]



    weights_all = []
    # ==================================================
    # E13C ADD:
    # store temporal reliability score history
    #
    # r_i^t before EMA weight smoothing
    # used for paper analysis Figure 3
    # ==================================================

    reliability_all = []


    prev_weight = None



    for t in range(num_frames):


        # =====================================
        # temporal window
        # =====================================

        start = max(
            0,
            t-window
        )


        kp_seq = kp_history[start:t+1]

        joint_seq = joint_history[start:t+1]



        # =====================================
        # initialization
        #
        # first frames:
        # no enough temporal information
        #
        # use uniform weighting
        # =====================================

        if len(kp_seq) < 3:


            smooth_weight = np.ones(
                num_kp
            )


            prev_weight = smooth_weight


            weights_all.append(
                smooth_weight
            )


            continue



        corr_scores = []

        motion_scores = []

        stability_scores = []



        # joint motion

        joint_motion = np.linalg.norm(
            np.diff(
                joint_seq,
                axis=0
            ),
            axis=1
        )



        for k in range(num_kp):


            # =================================
            # keypoint motion
            # =================================

            kp_motion = np.linalg.norm(
                np.diff(
                    kp_seq[:, k, :],
                    axis=0
                ),
                axis=1
            )



            # =================================
            # 1.
            # motion-joint correlation
            # =================================


            if np.std(kp_motion) < 1e-8:


                corr = 0.0


            else:

                min_len = min(
                    len(kp_motion),
                    len(joint_motion)
                )

                if min_len < 2:

                    corr = 0.0

                else:

                    corr, _ = pearsonr(
                        kp_motion[:min_len],
                        joint_motion[:min_len]
                    )



            corr_scores.append(
                abs(corr)
            )



            # =================================
            # 2.
            # motion magnitude
            # =================================


            motion_scores.append(
                kp_motion.mean()
            )



            # =================================
            # 3.
            # temporal stability
            #
            # smaller variance:
            # higher reliability
            # =================================


            deviation = np.linalg.norm(
                kp_seq[:, k, :]
                -
                kp_seq[:, k, :].mean(axis=0),
                axis=1
            )


            uncertainty = deviation.mean()



            stability_scores.append(
                1.0 /
                (uncertainty + 1e-8)
            )



        corr_scores = np.asarray(
            corr_scores
        )


        motion_scores = np.asarray(
            motion_scores
        )


        stability_scores = np.asarray(
            stability_scores
        )



        # =====================================
        # normalize each signal
        #
        # avoid scale domination
        # =====================================


        corr_scores /= (
            corr_scores.mean()
            +
            1e-8
        )


        motion_scores /= (
            motion_scores.mean()
            +
            1e-8
        )


        stability_scores /= (
            stability_scores.mean()
            +
            1e-8
        )



        # =====================================
        # E13-C fusion
        #
        # S =
        # 0.5 correlation
        # +
        # 0.3 motion
        # +
        # 0.2 stability
        #
        # =====================================


        score = (

            corr_weight
            *
            corr_scores

            +

            motion_weight
            *
            motion_scores

            +

            stability_weight
            *
            stability_scores

        )

        # ==================================================
        # E13C ADD:
        # reliability score before normalization
        # ==================================================

        reliability_all.append(
            score.copy()
        )


        # normalize weight

        weight = (

            score /
            (score.mean()+1e-8)

        )



        # =====================================
        # EMA smoothing
        # =====================================


        if prev_weight is None:


            smooth_weight = weight


        else:


            smooth_weight = (

                ema_alpha
                *
                weight

                +

                (1-ema_alpha)
                *
                prev_weight

            )



        prev_weight = smooth_weight



        weights_all.append(
            smooth_weight
        )


    # ==================================================
    # E13C ADD:
    # expose reliability history
    # ==================================================

    compute_online_weight.reliability_history = np.asarray(
        reliability_all
    )

    return np.asarray(
        weights_all
    )