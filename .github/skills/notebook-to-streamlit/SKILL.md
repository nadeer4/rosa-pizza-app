---
name: notebook-to-streamlit
description: Convert the analysis logic in notebook.ipynb (Rosa's Pizza delivery-promise analysis) into a Streamlit app (app.py), reusing the notebook's functions without changing their calculations. Use when building or updating the Streamlit app for this repository.
---

# Notebook to Streamlit

## Goal
Build `app.py`, a Streamlit app that helps Rosa choose the best promised
delivery time for a zone and time block, using the same logic as `notebook.ipynb`.

## Step 1: Read the notebook first
- Open `notebook.ipynb` and find these functions: `late_cost`, `net_profit`,
  and `best_promise`.
- Copy their logic into `app.py` exactly. Do not change any formula.
  - cost per late order = refund + churn_orders × margin
  - net profit = orders × margin − late orders × cost per late order
  - an order is late when its delivery time is greater than the promise
- Keep `seed=1` as the default so results match the notebook.

## Step 2: Use the starter package, never rewrite it
- Import from the starter package:
  `from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times`
- Do NOT define your own ZONES, TIME_BLOCKS, COSTS, PROMISE or delivery_times.
- Skip notebook-only code: `!pip install` lines, test prints, and tables
  printed for Parts I and II.

## Step 3: Adapt notebook code for Streamlit
- Replace `print()` warnings with Streamlit elements (e.g. `st.warning`).
  In `best_promise`, report the "best promise at the edge of the range"
  warning in the app instead of printing it.
- Cache the expensive search with `@st.cache_data` so repeated clicks are fast.

## Step 4: Required user interface
1. Dropdown (`st.selectbox`) for the zone, options from `ZONES`.
2. Dropdown (`st.selectbox`) for the time block, options from `TIME_BLOCKS`.
3. Inputs for the range of promises to try: minimum, maximum and step
   (minutes). Defaults: 20, 90, 5. Validate that minimum < maximum and
   step > 0; show `st.error` and stop if not.
4. Inputs for the costs, with defaults taken from `COSTS`:
   profit margin per order ($), churn (lost future orders) per late order,
   refund per late order ($).
5. A button ("Find best promise"). Only run the calculation after it is clicked.
6. Results: the recommended promise and its net profit, plus a comparison with
   today's promise (`PROMISE`, 45 minutes) when 45 is in the range, and a line
   chart of net profit vs promise.

## Step 5: Supporting files
- Create `requirements.txt` containing:
  streamlit
  numpy
  pandas
  git+https://github.com/zhouy185/rosa-starter.git
- Do not add personal information anywhere (the repository is public).

## Step 6: Check your work
- Confirm that with default inputs, Far West + Fri/Sat eve recommends
  55 minutes with net profit of about $1,212 (matching the notebook).
- Tell the user how to run it locally: `streamlit run app.py`.