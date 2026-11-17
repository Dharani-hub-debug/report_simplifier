import pandas as pd
import streamlit as st

from checker import check_value, ranges, people
from texts import LANGUAGES, TEST_TEXT, UI

lang_name = st.sidebar.selectbox("Language", list(LANGUAGES.keys()))
lang = LANGUAGES[lang_name]
t = UI[lang]

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
for row in rows:
    test_name = row[t["test"]]
    flag = row["_flag"]
    info = TEST_TEXT[test_name][lang]
    with st.expander(f"{test_name}: {t[flag]}"):
        st.write(f"**{t['measures']}:** {info['measures']}")
        if flag == "LOW":
            st.write(f"**{t['meaning_low']}:** {info['low']}")
        elif flag == "HIGH":
            st.write(f"**{t['meaning_high']}:** {info['high']}")
        else:
            st.write(t["normal_msg"])
        st.caption(t["see_doctor"])