# Medical Report Simplifier

**From confusing numbers to clear answers, in your language.**

Medical Report Simplifier is a web app that explains blood test reports in plain language. It checks each lab value against its reference range, marks it as Low, Normal or High, and explains what it means in English, Hindi or Kannada, as text or as audio.

> **Disclaimer:** This app explains lab values for general understanding only. It does not give a diagnosis or medical advice. Always consult a doctor about your results.

## Team
1. Ashwathi B Nair 

2. Dharani 

## The Problem

Lab reports are full of numbers and medical terms that most patients cannot easily understand. They are usually written in English and available only as text. Many patients, especially those who prefer Hindi or Kannada, or who find reading difficult, have to wait for a doctor to explain their results.

## Our Solution

The app turns each lab value into a short, simple explanation:

1. A patient report is selected from the data file.
2. Each value is compared with the reference range for the patient's gender.
3. The result is marked Low, Normal or High and colour-coded.
4. The app explains what the test measures and what a low or high value can mean.
5. The explanation is shown as text, or played as audio.

## Features

- **Three languages:** English, Hindi and Kannada.
- **Text or audio:** read the explanation, or listen to it.
- **Colour-coded results:** Low, Normal and High are clear at a glance.
- **Optional AI translation:** Gemini can translate the explanations on request, with the built-in hand-written text as an automatic fallback.
- **Privacy by design:** only generic explanation sentences are sent to the AI. Names, ages and lab values are never sent.
- **Rule-based checking:** Low, Normal and High come from fixed reference ranges, not from AI.
- **Caching:** translations and audio are saved, so the same text is never generated twice.
- **Safety reminders:** every result carries a reminder to consult a doctor.

## Tech Stack

- Python
- [Streamlit](https://streamlit.io/) for the web interface
- [pandas](https://pandas.pydata.org/) for reading and checking data
- [Google Gemini API](https://ai.google.dev/) for optional translation
- [gTTS](https://gtts.readthedocs.io/) (Google Text-to-Speech) for audio

## Project Structure

```
medical_report_simplifier/
├── front.py                 # Streamlit app (user interface)
├── checker.py               # Compares values with reference ranges
├── texts.py                 # Hand-written explanations and interface text (en, hi, kn)
├── translator.py            # Optional Gemini translation with caching
├── audio.py                 # Text-to-speech with caching
├── data/
│   └── reference_ranges.csv # Reference ranges for each test
├── samples/
│   └── Blood_reports_data_base.xlsx  # Sample patient reports
├── requirements.txt
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- An internet connection (needed for AI translation and audio)
- A Gemini API key, only if you want AI translation ([get one from Google AI Studio](https://aistudio.google.com/))

### Installation

```
git clone https://github.com/ashwathibnair2007-afk/medical_report_simplifier.git
cd medical_report_simplifier
pip install -r requirements.txt
```

### Set up the Gemini API key (optional)

The app works without a key, using the built-in text. To enable AI translation, create a file named `.env` in the project folder containing:

```
GEMINI_API_KEY=your-key-here
```

Never commit this file. It is listed in `.gitignore`.

### Run the app

```
python -m streamlit run front.py
```

The app opens in your browser at `http://localhost:8501`.

## How to Use

1. Choose a language in the sidebar (English, Hindi or Kannada).
2. Choose **Text** or **Audio** under "Show explanation as".
3. Select a patient from the list.
4. Read the colour-coded table and the explanations, or press play to listen.
5. For Hindi or Kannada, tick **Use AI translation (Gemini)** to try the AI version.

## Privacy and Safety

- Only the generic explanation sentences are sent to Gemini and to the text-to-speech service. No names, ages or lab values are sent.
- Result flags (Low, Normal, High) are decided by fixed rules, never by AI.
- AI translations can contain mistakes, so the app shows a warning when they are used. If the AI is unavailable, the hand-written text is shown instead.
- The sample data is for demonstration only. Do not upload real patient data to a public repository.

## Limitations

- The app currently works on the sample reports only. It cannot yet read an uploaded report.
- Hindi and Kannada text, and the audio, should be reviewed by native speakers before real use.
- Test names are spoken in English inside Hindi and Kannada audio.
- AI translation and audio need an internet connection.
- This is a student prototype and is not a medical device.

## Future Work

- Upload a report (PDF, photo or typed values) instead of using sample patients.
- Support more Indian languages.
- Add a slower audio option and a play button for each test.
- Review all translations with native speakers and medical professionals.
- Extend reference ranges to cover age, units and lab differences.

## Acknowledgements

Built as a project for a hackathon.
