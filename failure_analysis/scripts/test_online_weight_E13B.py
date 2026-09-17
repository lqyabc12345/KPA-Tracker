import numpy as np
from scipy.stats import pearsonr


print("="*60)
print("ONLINE KEYPOINT WEIGHT TEST")
print("="*60)


kp_history = np.load(
    "failure_analysis/results/pred_child_kp_history.npy"
)


joint_history = np.load(
    "failure_analysis/results/optimized_joint_state_history.npy"
)


print("kp:", kp_history.shape)
print("joint:", joint_history.shape)


def compute_weight(
        kp_history,
        joint_history,
        window=20,
        alpha=0.2
):

    num_frames = kp_history.shape[0]
    num_kp = kp_history.shape[1]


    weights_all=[]

    # E13-B:
    # previous smoothed weight for EMA
    prev_weight = None


    for t in range(num_frames):

        start=max(0,t-window)


        kp_seq=kp_history[start:t+1]

        joint_seq=joint_history[start:t+1]


        # ---------------------------------
        # E13-B initialization stage
        # no enough history
        # use uniform weight
        # ---------------------------------

        if len(kp_seq)<3:

            smooth_weight = np.ones(num_kp)

            prev_weight = smooth_weight

            weights_all.append(
                smooth_weight
            )

            continue



        # ---------------------------------
        # E13-B:
        # correlation score
        # + motion score
        # ---------------------------------

        corr_scores=[]
        motion_scores=[]



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


            # correlation

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


            # motion magnitude

            motion_scores.append(
                kp_motion.mean()
            )



        corr_scores=np.array(
            corr_scores
        )

        motion_scores=np.array(
            motion_scores
        )



        # ---------------------------------
        # E13-B:
        # normalize two signals
        # before fusion
        # ---------------------------------

        corr_scores = (
            corr_scores /
            (corr_scores.mean()+1e-8)
        )


        motion_scores = (
            motion_scores /
            (motion_scores.mean()+1e-8)
        )



        # ---------------------------------
        # E13-B final reliability score
        #
        # 70% observability
        # 30% motion
        # ---------------------------------

        scores = (
            0.7*corr_scores
            +
            0.3*motion_scores
        )



        weight = (
            scores /
            (scores.mean()+1e-8)
        )



        # ---------------------------------
        # EMA temporal smoothing
        # ---------------------------------

        if prev_weight is None:

            smooth_weight = weight

        else:

            smooth_weight = (
                alpha*weight
                +
                (1-alpha)*prev_weight
            )


        prev_weight=smooth_weight


        weights_all.append(
            smooth_weight
        )



    return np.array(weights_all)



weights=compute_weight(
    kp_history,
    joint_history
)

np.save(
    "failure_analysis/results/E13B_online_weights.npy",
    weights
)


print()
print("weight shape:")
print(weights.shape)


print()

for i in [0,10,50,100,200,376]:

    print(
        "frame",
        i,
        weights[i]
    )


print()

print(
    "mean weight:"
)

print(
    np.mean(weights,axis=0)
)

print(
"weight std:"
)

print(
np.std(weights,axis=0)
)