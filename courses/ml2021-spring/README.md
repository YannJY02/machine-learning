# Machine Learning 2021 Spring

Core track: Hung-yi Lee Machine Learning 2021 Spring.

Source of truth: <https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php>
Official/sample code mirror: <https://github.com/ga642381/ML2021-Spring>

## Layout

- `prep/`: Colab and Pytorch tutorials.
- `units/`: lecture-first study units in official course order.
- `units/<unit>/slides/`: local official lecture PDFs, ignored by git.
- `units/<unit>/transcripts/`: local YouTube transcript markdown files, ignored by git except `README.md`.
- `units/<unit>/lesson-*.html`: standalone teaching pages generated from the matching local slides and transcripts.
- `units/<unit>/teaching-assets/<lesson-slug>/`: PDF-derived slide screenshots or other local visual assets used by a teaching page.
- `units/<unit>/homework/<hw>/`: assignment PDF, starter notebook, learner notebook, data, and review for that homework.

Local course assets live next to the unit or homework that uses them. Large PDFs, datasets, checkpoints, and official starter notebooks are intentionally ignored by git.
PDF-derived screenshots in `teaching-assets/` follow the same local-asset rule unless they are explicitly replaced by small learner-authored visuals.

Study order follows the YouTube playlist in [`learning-sequence.md`](learning-sequence.md).

## Units

| Unit | Topic | Status | Homework |
| --- | --- | --- | --- |
| 001 | [Introduction](units/001-introduction/) | active | hw1-regression |
| 002 | [Deep Learning](units/002-deep-learning/) | planned | hw2-classification |
| 003 | [CNN & Self-Attention](units/003-cnn-and-self-attention/) | planned | hw3-cnn, hw4-self-attention |
| 004 | [Theory of ML (Prof. Pei-Yuan Wu)](units/004-theory-of-ml-prof-pei-yuan-wu/) | planned | none |
| 005 | [Transformer](units/005-transformer/) | planned | hw5-transformer |
| 006 | [Generative Model](units/006-generative-model/) | planned | hw6-gan |
| 007 | [Self-Supervised Learning](units/007-self-supervised-learning/) | planned | hw7-bert, hw8-anomaly-detection |
| 008 | [Explainable AI / Adversarial Attack](units/008-explainable-ai-adversarial-attack/) | planned | hw9-explainable-ai, hw10-attack |
| 009 | [Domain Adaptation](units/009-domain-adaptation/) | planned | hw11-adaptation |
| 010 | [Privacy v.s. ML (Prof. Pei-Yuan Wu)](units/010-privacy-v-s-ml-prof-pei-yuan-wu/) | planned | none |
| 011 | [RL](units/011-rl/) | planned | hw12-rl |
| 012 | [Quantum ML (Prof. Hao-Chung Cheng)](units/012-quantum-ml-prof-hao-chung-cheng/) | planned | none |
| 013 | [Life-Long/Compression](units/013-life-long-compression/) | planned | hw13-compression, hw14-life-long-learning |
| 014 | [Meta Learning](units/014-meta-learning/) | planned | hw15-meta-learning |

## Status Vocabulary

- `planned`: resources are known, study not started.
- `active`: currently studying or coding.
- `review`: first attempt done, mistakes and open questions are being cleaned up.
- `done`: notes, practice, and review are good enough to revisit later.
