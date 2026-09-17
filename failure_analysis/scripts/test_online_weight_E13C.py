import numpy as np
from scipy.stats import pearsonr


print("="*60)
print("E13-C ONLINE KEYPOINT RELIABILITY WEIGHT")
print("="*60)



# ==================================================
# Load E9 / E10 history
# ==================================================

kp_history = np.load(
    "failure_analysis/results/pred_child_kp_history.npy"
)


joint_history = np.load(
    "failure_analysis/results/optimized_joint_state_history.npy"
)


print("kp shape:", kp_history.shape)
print("joint shape:", joint_history.shape)



def compute_weight(
        kp_history,
        joint_history,
        window=20,
        alpha=0.2
):


    num_frames = kp_history.shape[0]

    num_kp = kp_history.shape[1]


    weights_all=[]


    prev_weight=None



    for t in range(num_frames):


        start=max(
            0,
            t-window
        )


        kp_seq = kp_history[start:t+1]

        joint_seq = joint_history[start:t+1]



        # ==========================================
        # E13-C initialization
        # ==========================================

        if len(kp_seq)<3:


            smooth_weight=np.ones(num_kp)


            prev_weight=smooth_weight


            weights_all.append(
                smooth_weight
            )


            continue



        corr_scores=[]

        motion_scores=[]

        uncertainty_scores=[]



        # joint motion

        joint_motion=np.linalg.norm(
            np.diff(
                joint_seq,
                axis=0
            ),
            axis=1
        )



        for k in range(num_kp):


            kp_motion=np.linalg.norm(
                np.diff(
                    kp_seq[:,k,:],
                    axis=0
                ),
                axis=1
            )



            # ======================================
            # E13-C signal 1:
            # joint correlation
            # ======================================

            if np.std(kp_motion)<1e-8:

                corr=0

            else:

                corr,_=pearsonr(
                    kp_motion,
                    joint_motion
                )


            corr_scores.append(
                abs(corr)
            )



            # ======================================
            # E13-C signal 2:
            # motion magnitude
            # ======================================

            motion_scores.append(
                kp_motion.mean()
            )



            # ======================================
            # E13-C signal 3:
            # temporal stability
            #
            # lower variance = higher reliability
            # ======================================

            variance=np.mean(
                np.linalg.norm(
                    kp_seq[:,k,:]
                    -
                    kp_seq[:,k,:].mean(axis=0),
                    axis=1
                )
            )


            uncertainty_scores.append(
                1.0/(variance+1e-8)
            )



        corr_scores=np.array(
            corr_scores
        )

        motion_scores=np.array(
            motion_scores
        )

        uncertainty_scores=np.array(
            uncertainty_scores
        )



        # ==========================================
        # Normalize each reliability signal
        # ==========================================


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


        uncertainty_scores /= (
            uncertainty_scores.mean()
            +
            1e-8
        )



        # ==========================================
        # E13-C fusion
        #
        # correlation 50%
        # motion       30%
        # stability    20%
        # ==========================================


        score=(

            0.5*corr_scores

            +
            0.3*motion_scores

            +
            0.2*uncertainty_scores

        )



        weight = (
            score /
            (score.mean()+1e-8)
        )



        # ==========================================
        # EMA smoothing
        # ==========================================


        if prev_weight is None:

            smooth_weight=weight


        else:

            smooth_weight=(

                alpha*weight

                +

                (1-alpha)*prev_weight

            )



        prev_weight=smooth_weight


        weights_all.append(
            smooth_weight
        )



    return np.array(weights_all)




# ==================================================
# Run
# ==================================================


weights=compute_weight(
    kp_history,
    joint_history
)



print()

print("weight shape:")
print(weights.shape)



print()


for i in [
    0,
    10,
    50,
    100,
    200,
    376
]:

    print(
        "frame",
        i,
        weights[i]
    )



print()

print("mean weight:")
print(
    np.mean(
        weights,
        axis=0
    )
)


print()

print("weight std:")
print(
    np.std(
        weights,
        axis=0
    )
)



np.save(
    "failure_analysis/results/E13C_online_weights.npy",
    weights
)



print()

print(
    "saved:"
    " failure_analysis/results/E13C_online_weights.npy"
)