# RA-KPA Framework Figure v2 Design


## 1. Figure Goal


Figure 2 is the main overview figure of RA-KPA.

The figure should communicate:

1. Existing keypoint tracking assumes uniform reliability.

2. Keypoint reliability changes over time.

3. RA-KPA estimates reliability and dynamically adapts keypoint contribution.



The central message:


"Reliable keypoints should dominate optimization, while unreliable observations should be suppressed automatically."



---

# 2. Design Principle


Avoid a simple sequential pipeline.

Instead, emphasize:


## Reliability Adaptation Loop



The framework consists of:


Observation

↓

Reliability Estimation

↓

Adaptive Weight Generation

↓

Weighted Optimization

↓

Temporal Update



This creates an online reliability-aware tracking system.



---

# 3. Recommended Layout


Use three horizontal levels.



## Level 1: Tracking Input and Output


Top:



RGB / Depth Sequence

    |

    v

Keypoint Observation History

    |

    v

Refined Articulated Pose




This represents the tracking task.



---

## Level 2: RA-KPA Core Module


Middle:


Highlight with a large container:




+------------------------------------------------+

    Reliability-Aware Keypoint Adaptation


    Keypoint Reliability Estimation


             r_i^t


                |


                v



    Adaptive Weight Generation


             w_i^t


                |


                v



    Weighted Pose Optimization

+------------------------------------------------+




This is the main contribution.



---

## Level 3: Reliability Evidence


Bottom:


Show why reliability can be estimated.



Two inputs:



Motion Consistency

    +

Temporal Correlation

    |

    v

Reliability Score




These correspond to E12.



---

# 4. Final Figure Layout


Recommended:



                Input Sequence

                      |

                      v


         Keypoint Observation History


                      |

                      |

====================================================

      RA-KPA Reliability Adaptation Module


      Motion Consistency
              |
              |
              v


      Reliability Estimation

             r_i^t


              |

              v


      Adaptive Weight Generation

             w_i^t


              |

              v


      Weighted Optimization

====================================================

                      |

                      v


          Refined Tracking Result



                      |

                      |

                Temporal Update

                      |

                      +

                      |

          Keypoint History Buffer



---

# 5. Visual Elements


## Input


Do not use only text.

Include:


- RGB frame placeholder
- keypoint dots


Example:



Image




---

## Reliability Estimation


Show:

keypoint confidence bars:



kp1 █████

kp2 ██

kp3 █████

kp4 █




---

## Adaptive Weight


Show vector:


\[
w^t=[w_1,w_2,...,w_n]
\]



Example:


\[
[1.3,0.6,1.4,0.7]
\]



---

## Optimization


Show comparison:


Before:


\[
\sum_i ||e_i||^2
\]


RA-KPA:


\[
\sum_i w_i^t||e_i||^2
\]



---

# 6. Important Paper Message


The figure should visually separate:


## Existing Tracking


Uniform weight:

\[
w_i=1
\]



## RA-KPA


Adaptive:

\[
w_i^t
\]



This difference should be obvious.



---

# 7. Recommended Final Style


Use:


- clean white background
- limited colors
- rounded boxes
- thin arrows
- mathematical annotations


Similar style to CVPR/ICCV overview figures.



---

# 8. Implementation Strategy


Do NOT create the final figure completely with matplotlib.



Recommended workflow:


Step 1:

Python generate:

- keypoint visualization
- reliability curve
- weight vector


Step 2:

Export SVG/PDF.


Step 3:

Assemble in:

- Figma
- Illustrator
- Inkscape



Final figure exported as:


framework_overview.pdf

framework_overview.png



---

# 9. Caption Draft


"Overview of RA-KPA. Different from conventional keypoint-based trackers that treat all keypoints equally, RA-KPA estimates temporal keypoint reliability and adaptively adjusts keypoint contribution during pose optimization. The proposed reliability-aware adaptation enables robust articulated tracking under unreliable observations."
