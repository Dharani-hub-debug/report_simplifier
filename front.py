import pandas as pd
import streamlit as st

from audio import make_audio
from checker import check_value, ranges, people
from texts import LANGUAGES, TEST_TEXT, UI
from translator import translate

lang_name = st.sidebar.selectbox("Language", list(LANGUAGES.keys()))
lang = LANGUAGES[lang_name]
t = UI[lang]

view = st.sidebar.radio("Show explanation as", ["Text", "Audio"])

use_ai = False
if lang != "en":
    use_ai = st.sidebar.checkbox("Use AI translation (Gemini)")
    if use_ai:
        st.sidebar.caption(
            "AI translations can contain mistakes. "
            "Please check important information with a doctor."
        )

fallback_used = []


def get_text(test_name, part):
    english = TEST_TEXT[test_name]["en"][part]
    if lang == "en":
        return english
    if use_ai:
        result = translate(english, lang)
        if result:
            return result
        fallback_used.append(test_name)
    return TEST_TEXT[test_name][lang][part]


st.title(t["title"])
st.warning(t["disclaimer"])

name = st.selectbox(t["choose_person"], people["Name"])
person = people[people["Name"] == name].iloc[0]
st.write(f"**{person['Name']}**, {t['age']} {person['Age']}, {t[person['Gender']]}")

rows = []
for _, test in ranges.iterrows():
    test_name = test["test_name"]
    value = person[test_name]
    flag, low, high = check_value(test_name, value, person["Gender"])
    rows.append(
        {
            t["test"]: test_name,
            t["value"]: f"{value:g}",
            t["range"]: f"{low:g} - {high:g}",
            t["result"]: t[flag],
            "_flag": flag,
        }
    )

table = pd.DataFrame(rows).drop(columns="_flag")

flag_colors = {
    t["LOW"]: "background-color: #ffe0b2",
    t["HIGH"]: "background-color: #ffcdd2",
    t["NORMAL"]: "background-color: #c8e6c9",
}


def color_flag(val):
    return flag_colors.get(val, "")


st.dataframe(table.style.map(color_flag, subset=[t["result"]]), hide_index=True)

st.subheader(t["heading"])

# Collect the explanation for every test (translated if AI is ticked)
explanations = []
with st.spinner("Preparing, please wait..."):
    for row in rows:
        test_name = row[t["test"]]
        flag = row["_flag"]
        measures = get_text(test_name, "measures")
        if flag == "LOW":
            meaning_label = t["meaning_low"]
            meaning = get_text(test_name, "low")
        elif flag == "HIGH":
            meaning_label = t["meaning_high"]
            meaning = get_text(test_name, "high")
        else:
            meaning_label = None
            meaning = t["normal_msg"]
        explanations.append((test_name, flag, measures, meaning_label, meaning))

if view == "Text":
    for test_name, flag, measures, meaning_label, meaning in explanations:
        with st.expander(f"{test_name}: {t[flag]}"):
            st.write(f"**{t['measures']}:** {measures}")
            if meaning_label:
                st.write(f"**{meaning_label}:** {meaning}")
            else:
                st.write(meaning)
            st.caption(t["see_doctor"])
else:
    # Build one spoken script for the whole report
    script_parts = []
    for test_name, flag, measures, meaning_label, meaning in explanations:
        script_parts.append(f"{test_name}. {t[flag]}. {measures} {meaning}")
    script_parts.append(t["see_doctor"])
    script = "\n".join(script_parts)

    with st.spinner("Creating audio, please wait..."):
        audio_path = make_audio(script, lang)

    if audio_path:
        st.audio(audio_path, format="audio/mp3")
        st.caption(t["see_doctor"])
    else:
        st.error(
            "Audio could not be created (check your internet connection). "
            "Please switch to Text."
        )

if fallback_used:
    st.sidebar.warning(
        "The AI was unavailable for some sentences, so the built-in text is shown for them."
    )