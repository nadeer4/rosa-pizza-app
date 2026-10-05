import pandas as pd
import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times


def late_cost(costs):
    """Total cost ($) of one late order: refund + profit lost to churn."""
    return costs['refund'] + costs['churn_orders'] * costs['margin']


def net_profit(zone, time_block, promise, costs, seed=1):
    """Net profit ($) over four weeks for one zone, time block and promise."""
    times = delivery_times(zone, time_block, promise, seed=seed)
    n_orders = len(times)
    n_late = (times > promise).sum()
    return n_orders * costs['margin'] - n_late * late_cost(costs)


def best_promise(zone, time_block, promises, costs, seed=1):
    """Try each promise and return (best promise, its net profit, all profits).
    `all profits` is a dict {promise: net profit}, handy for charts in the app."""
    profits = {}
    for p in promises:
        profits[p] = net_profit(zone, time_block, p, costs, seed)

    best_p = max(profits, key=profits.get)   # promise with the highest profit

    # Warn if the best promise sits at an edge of the range
    if best_p == min(promises) or best_p == max(promises):
        st.warning(f"Best promise for {zone}, {time_block} is at the edge "
                   f"of the range ({best_p} min). Consider widening the range.")

    return best_p, profits[best_p], profits


@st.cache_data
def cached_best_promise(zone, time_block, promises, costs, seed=1):
    return best_promise(zone, time_block, list(promises), costs, seed)


st.title("Rosa's Pizza: Best Delivery Promise")

zone = st.selectbox("Zone", ZONES)
time_block = st.selectbox("Time block", TIME_BLOCKS)

st.subheader("Range of promises to try (minutes)")
c1, c2, c3 = st.columns(3)
p_min = c1.number_input("Minimum", value=20, step=1)
p_max = c2.number_input("Maximum", value=90, step=1)
p_step = c3.number_input("Step", value=5, step=1)

st.subheader("Costs")
c1, c2, c3 = st.columns(3)
margin = c1.number_input("Profit margin per order ($)",
                         value=float(COSTS['margin']), min_value=0.0)
churn = c2.number_input("Churn (lost future orders) per late order",
                        value=float(COSTS['churn_orders']), min_value=0.0)
refund = c3.number_input("Refund per late order ($)",
                         value=float(COSTS['refund']), min_value=0.0)

if st.button("Find best promise"):
    if p_min >= p_max:
        st.error("Minimum must be less than maximum.")
        st.stop()
    if p_step <= 0:
        st.error("Step must be greater than 0.")
        st.stop()

    costs = {'refund': refund, 'churn_orders': churn, 'margin': margin}
    promises = tuple(range(int(p_min), int(p_max) + 1, int(p_step)))
    best_p, profit, all_profits = cached_best_promise(
        zone, time_block, promises, costs, seed=1)

    st.success(f"Recommended promise: {best_p} minutes "
               f"(net profit ${profit:,.0f} over four weeks)")

    if PROMISE in all_profits:
        current = all_profits[PROMISE]
        st.write(f"Today ({PROMISE} min): ${current:,.0f}")
        st.write(f"Improvement: ${profit - current:,.0f} over four weeks")
    else:
        st.info(f"Today's promise ({PROMISE} min) is not in the range, "
                "so no comparison is shown.")

    chart = pd.DataFrame({"Net profit ($)": pd.Series(all_profits)})
    chart.index.name = "Promise (minutes)"
    st.line_chart(chart)
