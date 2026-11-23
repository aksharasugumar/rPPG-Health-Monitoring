# Advanced rPPG Vital Signs & Stress Monitor

This version upgrades the project from a single POS pipeline to a more robust **multi-stage rPPG ensemble**.

## Accuracy-focused improvements

1. **Multi-ROI facial measurement**
   - Forehead
   - Left upper cheek
   - Right upper cheek
   - Skin-pixel filtering
   - Quality-weighted ROI fusion

2. **rPPG ensemble**
   - POS
   - CHROM
   - Green-channel pulse
   - Robust median fusion rather than relying on one fixed method

3. **Signal quality gate**
   - Rejects frames with excessive facial motion
   - Rejects poor skin ROI quality
   - Uses ROI consistency as a quality feature

4. **Three-way heart-rate consensus**
   - Frequency-domain estimate
   - Autocorrelation estimate
   - Peak/beat interval estimate
   - Their agreement contributes to the displayed signal-quality confidence

5. **Temporal stabilization**
   - Band-pass filtering: 0.70–3.00 Hz
   - 12-second analysis window
   - Sudden-jump rejection/smoothing

6. **Natural camera preview**
   - No blue filter
   - No false-color camera image
   - BGR → RGB conversion occurs only where required by MediaPipe/PIL

## Important accuracy note

This is a research/academic implementation, not a clinically validated medical device. A displayed confidence value is an algorithmic signal-quality estimate, **not a claim of 95% measurement accuracy**. Real accuracy must be measured against a reference pulse oximeter/ECG using a documented validation protocol.

## Install

Use Python 3.10 or 3.11.

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If you previously installed a newer incompatible MediaPipe version:

```powershell
python -m pip uninstall -y mediapipe numpy
python -m pip install "numpy>=1.24,<2.0" "mediapipe==0.10.21"
python -m pip install scipy opencv-python Pillow matplotlib
python main.py
```

## Better measurement conditions

- Use a front-facing webcam at 720p or higher when possible.
- Keep the face centered and relatively still.
- Use stable, diffuse front lighting.
- Avoid strong backlighting and rapidly changing illumination.
- Keep the camera exposure from constantly changing if your webcam software permits it.
- Let the system collect several seconds of data before interpreting HR.

## Validation mode recommendation

For a final-year project, record simultaneous webcam video and a reference HR signal, then calculate MAE, RMSE, correlation and Bland–Altman bias/limits across subjects and lighting/motion conditions. This is much stronger evidence than assigning an arbitrary confidence percentage.


## Bold UI update
The dashboard typography, vital-number cards, chart titles, chart lines, and card borders have been increased for stronger visibility while keeping the natural-color camera and rPPG processing unchanged.


## Stress indicator alignment
The right-side vital cards use compact vertical spacing so the Stress Indicator remains fully visible and aligned with the other metric cards.
