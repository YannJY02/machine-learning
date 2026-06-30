# Notes

## Core Idea

Deep Learning training can fail for different reasons. In this unit, separate `Optimization` problems from `Overfitting`: if training loss itself stops improving, the first question is why `gradient descent` is not finding a better parameter region.

## Key Terms

- Classification
- Overfitting
- Optimizer
- Small Gradient
- Critical Point
- Local Minima
- Saddle Point
- Hessian
- Eigenvalue

## Learning Checkpoint

Current position: playlist video 04 transcript completed, using `slides/04-05-local-minima-batch-momentum-small-gradient-v7.pdf`.

## Lesson 04: Local Minima And Saddle Point

When training loss stops decreasing, it is not precise to immediately say the model is stuck in `local minima`. A point with near-zero `gradient` is a `critical point`, and it can be a `local minima`, `local maxima`, or `saddle point`.

The practical distinction is that a `local minima` has no nearby lower direction, while a `saddle point` still has directions that can reduce loss. The lecture uses the `Hessian` to reason about this local shape: all positive `eigenvalues` suggest `local minima`, all negative suggest `local maxima`, and mixed signs suggest a `saddle point`.

The main takeaway: in high-dimensional deep networks, being stuck is often more plausibly about `saddle point` or very small gradients than simply bad `local minima`. The next lesson should explain how `batch` and `momentum` help the optimizer keep moving.

## Open Questions

- How often do we actually diagnose `Hessian` or `eigenvalues` in real training?
- Is the practical fix usually optimizer choice, learning rate schedule, initialization, normalization, or batch design?
- How should I tell apart `Optimization` failure and `Generalization` failure from training/validation curves?

## Connections

- Official course page: <https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php>
- Official/sample code: <https://github.com/ga642381/ML2021-Spring>
- Transcript: `transcripts/04-local-minima-saddle-point.md`
