''' Streamlit APP '''
import streamlit as st
import pandas as pd
from functions import options, options, calculate

st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

def get_session_state():
    ''' Function to create and persist session state '''
    return st.session_state

def load_data():
    ''' Function Loading Data '''
    data = pd.read_csv('./data.csv')
    data.drop(index=data.loc[data.sharpe =='-'].index.tolist(),inplace = True)
    data.drop(index=data.loc[data.beta =='-'].index.tolist(),inplace = True)
    data.drop(index=data.loc[data.alpha =='-'].index.tolist(),inplace = True)
    data.drop(index=data.loc[data.sortino =='-'].index.tolist(),inplace = True)
    data.drop(index=data.loc[data.sd == '-'].index.tolist(), inplace = True)
    data.alpha=data.alpha.astype("float64")
    data.sd=data.sd.astype('float64')
    data.beta=data.beta.astype('float64')
    data.sharpe= data.sharpe.astype ('float64')
    data.sortino=data.sortino.astype('float64')

    return data

def reset_state():
    ''' Function to reset session state '''
    st.session_state.input_age = 0
    st.session_state.input_amount = 0
    st.session_state.suggestions = None
    st.session_state.suggestions2 = None
    st.session_state.my_list = []
    st.session_state.selected_amc = None
    st.session_state.selected_amc2 = None
    st.session_state.equity = 0
    st.session_state.hybrid = 0
    st.session_state.debt = 0
    st.session_state.suggestions3 = None
    st.session_state.selected_amc3 = None
    st.session_state.suggestions4 = None
    st.session_state.selected_amc4 = None
    st.session_state.suggestions5 = None
    st.session_state.selected_amc5 = None

def main():
    
    ''' Function contains main program code '''
    session_state = get_session_state()
    if 'input_age' not in session_state:
        session_state.input_age = 0

    if 'input_amount' not in session_state:
        session_state.input_amount = 0

    if 'suggestions' not in session_state:
        session_state.suggestions = None

    if 'suggestions2' not in session_state:
        session_state.suggestions2 = None

    if 'my_list' not in session_state:
        session_state.my_list = []

    if 'selected_amc' not in session_state:
        session_state.selected_amc = None

    if 'selected_amc2' not in session_state:
        session_state.selected_amc2 = None

    if 'equity' not in session_state:
        session_state.equity = 0

    if 'hybrid' not in session_state:
        session_state.hybrid = 0

    if 'debt' not in session_state:
        session_state.debt = 0

    if 'suggestions3' not in session_state:
        session_state.suggestions3 = None

    if 'selected_amc3' not in session_state:
        session_state.selected_amc3 = None

    if 'suggestions4' not in session_state:
        session_state.suggestions4 = None

    if 'selected_amc4' not in session_state:
        session_state.selected_amc4 = None

    if 'suggestions5' not in session_state:
        session_state.suggestions5 = None

    if 'selected_amc5' not in session_state:
        session_state.selected_amc5 = None

    # st.set_page_config(layout='wide')

    st.title("InvestWise: Personalized Mutual Fund Investment Recommendations")
    age = st.text_input("Please Enter your Age:",  key="age_input")
    submit = st.button("Submit Age", key='submit_age')

    if submit:
        if age.isnumeric():
            age = int(age)
            if age < 100:
                st.success("Input Successful!")
                session_state.input_age = age
            else:
                st.error("Users over 100 are not accepted.")
        else:
            st.error('Please Enter appropriate Age.')

    amount = st.text_input("Please Enter Amount you wish to Invest:", key='amount_input')
    submit2 = st.button("Submit Amount", key='submit_amount')

    if submit2:
        if amount.isnumeric():
            amount = int(amount)
            if amount >= 1000:
                st.success("Amount Entered Successfully")
                session_state.input_amount = amount
            else:
                st.error("Amount must be greater than or equal to 1000")
        else:
            st.error("Please Enter Appropriate Amount.")

    st.write("Age: ",session_state.input_age)
    st.write("Amount: ",session_state.input_amount)

    ## Starting Fund Selection Algorithm
    if session_state.input_age != 0 and session_state.input_amount != 0:
        if session_state.input_amount <= 5000:
            if session_state.input_age < 18:
                st.write(f'Allocated Amount: \nEquity: {session_state.input_amount}')

                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Final Display of Portfolio
                if len(session_state.my_list) != 0:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
            else:
                per = (100-session_state.input_age)/100
                session_state.equity = session_state.input_amount * per
                session_state.hybrid = session_state.input_amount - session_state.equity
                st.write('Allocated Amount:')
                st.write(f'Equity: {session_state.equity}')
                st.write(f'Hybrid: {session_state.hybrid}')

                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Hybrid Fund
                if session_state.suggestions2 is None:
                    session_state.suggestions2 = options(data, 'Hybrid')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn2 = st.button("New Options for Hybrid")
                with col2:
                    enter_amc_btn2 = st.button("Enter AMC for Hybrid Fund")

                if new_options_btn2:
                    session_state.suggestions2 = options(data, 'Hybrid')

                submit_amc2 = st.selectbox("Select AMC for Hybrid Fund:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn2 and submit_amc2 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc2 = submit_amc2
                    st.write("AMC:", session_state.selected_amc2)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc2]
                    session_state.suggestions2 = options(temp_data, 'Hybrid')

                st.dataframe(session_state.suggestions2)
                selected_row2 = st.selectbox("Select a row", session_state.suggestions2.index.tolist()) # pylint: disable=line-too-long
                submit_selection2 = st.button("Submit Hybrid Selection")
                if submit_selection2 and selected_row2 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row2)
                    session_state.my_list.append(selected_row2)

                ## For Final Display for Portfolio
                if len(session_state.my_list) == 2:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
                if len(session_state.my_list) > 2:
                    st.error('''Only two funds are supposed to be Selected!\
                             \nPlease reload and Try Again''')
                    reset_button = st.button("Reset")
                    if reset_button:
                        reset_state()
                        st.experimental_rerun()

        if session_state.input_amount > 5000 and session_state.input_amount <= 10000:
            if session_state.input_age < 18:
                st.write(f'Allocated Amount: \nEquity: {session_state.input_amount}')

                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Equity Fund 2
                if session_state.suggestions2 is None:
                    session_state.suggestions2 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn2 = st.button("New Options for Equity 2")
                with col2:
                    enter_amc_btn2 = st.button("Enter AMC for Equity Fund 2")

                if new_options_btn2:
                    session_state.suggestions2 = options(data, 'Equity')

                submit_amc2 = st.selectbox("Select AMC for Equity Fund 2:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn2 and submit_amc2 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc2 = submit_amc2
                    st.write("AMC:", session_state.selected_amc2)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc2]
                    session_state.suggestions2 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions2)
                selected_row2 = st.selectbox("Select a row", session_state.suggestions2.index.tolist()) # pylint: disable=line-too-long
                submit_selection2 = st.button("Submit Equity 2 Selection")
                if submit_selection2 and selected_row2 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row2)
                    session_state.my_list.append(selected_row2)

                ## For Final Display for Portfolio
                if len(session_state.my_list) == 2:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
                if len(session_state.my_list) > 2:
                    st.error('''Only two funds are supposed to be Selected!\
                             \nPlease reload and Try Again''')
                    reset_button = st.button("Reset")
                    if reset_button:
                        reset_state()
                        st.experimental_rerun()
            else:
                per = (100-session_state.input_age)/100
                session_state.equity = session_state.input_amount * per
                temp = session_state.input_amount - session_state.equity
                session_state.hybrid = temp/2
                session_state.debt = temp/2
                st.write('Allocated Amount:')
                st.write(f'Equity: {session_state.equity}')
                st.write(f'Hybrid: {session_state.hybrid}')
                st.write(f'Debt: {session_state.debt}')
                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Equity Fund 2
                if session_state.suggestions2 is None:
                    session_state.suggestions2 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn2 = st.button("New Options for Equity 2")
                with col2:
                    enter_amc_btn2 = st.button("Enter AMC for Equity Fund 2")

                if new_options_btn2:
                    session_state.suggestions2 = options(data, 'Equity')

                submit_amc2 = st.selectbox("Select AMC for Equity Fund 2:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn2 and submit_amc2 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc2 = submit_amc2
                    st.write("AMC:", session_state.selected_amc2)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc2]
                    session_state.suggestions2 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions2)
                selected_row2 = st.selectbox("Select a row", session_state.suggestions2.index.tolist()) # pylint: disable=line-too-long
                submit_selection2 = st.button("Submit Equity 2 Selection")
                if submit_selection2 and selected_row2 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row2)
                    session_state.my_list.append(selected_row2)

                ## For Hybrid Fund
                if session_state.suggestions3 is None:
                    session_state.suggestions3 = options(data, 'Hybrid')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn3 = st.button("New Options for Hybrid")
                with col2:
                    enter_amc_btn3 = st.button("Enter AMC for Hybrid Fund")

                if new_options_btn3:
                    session_state.suggestions3 = options(data, 'Hybrid')

                submit_amc3 = st.selectbox("Select AMC for Hybrid Fund:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn3 and submit_amc3 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc3 = submit_amc3
                    st.write("AMC:", session_state.selected_amc3)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc3]
                    session_state.suggestions3 = options(temp_data, 'Hybrid')

                st.dataframe(session_state.suggestions3)
                selected_row3 = st.selectbox("Select a row", session_state.suggestions3.index.tolist()) # pylint: disable=line-too-long
                submit_selection3 = st.button("Submit Hybrid Selection")
                if submit_selection3 and selected_row3 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row3)
                    session_state.my_list.append(selected_row3)

                ## For Debt Fund
                if session_state.suggestions4 is None:
                    session_state.suggestions4 = options(data, 'Debt')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn4 = st.button("New Options for Debt")
                with col2:
                    enter_amc_btn4 = st.button("Enter AMC for Debt Fund")

                if new_options_btn4:
                    session_state.suggestions4 = options(data, 'Debt')

                submit_amc4 = st.selectbox("Select AMC for Debt Fund:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn4 and submit_amc4 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc4 = submit_amc4
                    st.write("AMC:", session_state.selected_amc4)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc4]
                    session_state.suggestions4 = options(temp_data, 'Debt')

                st.dataframe(session_state.suggestions4)
                selected_row4 = st.selectbox("Select a row", session_state.suggestions4.index.tolist()) # pylint: disable=line-too-long
                submit_selection4 = st.button("Submit Debt Selection")
                if submit_selection4 and selected_row4 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row4)
                    session_state.my_list.append(selected_row4)

                ## For Final Display for Portfolio
                if len(session_state.my_list) == 4:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
                if len(session_state.my_list) > 4:
                    st.error('''Only two funds are supposed to be Selected!\
                             \nPlease reload and Try Again''')
                    reset_button = st.button("Reset")
                    if reset_button:
                        reset_state()
                        st.experimental_rerun()

        if session_state.input_amount > 10000:
            if session_state.input_age < 18:
                st.write(f'Allocated Amount: \nEquity: {session_state.input_amount}')

                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Equity Fund 2
                if session_state.suggestions2 is None:
                    session_state.suggestions2 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn2 = st.button("New Options for Equity 2")
                with col2:
                    enter_amc_btn2 = st.button("Enter AMC for Equity Fund 2")

                if new_options_btn2:
                    session_state.suggestions2 = options(data, 'Equity')

                submit_amc2 = st.selectbox("Select AMC for Equity Fund 2:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn2 and submit_amc2 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc2 = submit_amc2
                    st.write("AMC:", session_state.selected_amc2)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc2]
                    session_state.suggestions2 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions2)
                selected_row2 = st.selectbox("Select a row", session_state.suggestions2.index.tolist()) # pylint: disable=line-too-long
                submit_selection2 = st.button("Submit Equity 2 Selection")
                if submit_selection2 and selected_row2 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row2)
                    session_state.my_list.append(selected_row2)

                ## For Equity Fund 3
                if session_state.suggestions3 is None:
                    session_state.suggestions3 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn3 = st.button("New Options for Equity 3")
                with col2:
                    enter_amc_btn3 = st.button("Enter AMC for Equity Fund 3")

                if new_options_btn3:
                    session_state.suggestions3 = options(data, 'Equity')

                submit_amc3 = st.selectbox("Select AMC for Equity Fund 3:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn3 and submit_amc3 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc3 = submit_amc3
                    st.write("AMC:", session_state.selected_amc3)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc3]
                    session_state.suggestions3 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions3)
                selected_row3 = st.selectbox("Select a row", session_state.suggestions3.index.tolist()) # pylint: disable=line-too-long
                submit_selection3 = st.button("Submit Equity 3 Selection")
                if submit_selection3 and selected_row3 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row3)
                    session_state.my_list.append(selected_row3)

                ## For Final Display for Portfolio
                if len(session_state.my_list) == 3:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
                if len(session_state.my_list) > 3:
                    st.error('''Only two funds are supposed to be Selected!\
                             \nPlease reload and Try Again''')
                    reset_button = st.button("Reset")
                    if reset_button:
                        reset_state()
                        st.experimental_rerun()
            else:
                per = (100-session_state.input_age)/100
                session_state.equity = session_state.input_amount * per
                temp = session_state.input_amount - session_state.equity
                session_state.hybrid = temp/2
                session_state.debt = temp/2
                st.write('Allocated Amount:')
                st.write(f'Equity: {session_state.equity}')
                st.write(f'Hybrid: {session_state.hybrid}')
                st.write(f'Debt: {session_state.debt}')
                data = load_data()

                ## For Equity Fund
                if session_state.suggestions is None:
                    session_state.suggestions = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn = st.button("New Options")
                with col2:
                    enter_amc_btn = st.button("Enter AMC")

                if new_options_btn:
                    session_state.suggestions = options(data, 'Equity')

                submit_amc = st.selectbox("Select AMC:", data.amc_name.unique().tolist())

                if enter_amc_btn and submit_amc is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc = submit_amc
                    st.write("AMC:", session_state.selected_amc)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc]
                    session_state.suggestions = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions)
                selected_row = st.selectbox("Select a row", session_state.suggestions.index.tolist()) # pylint: disable=line-too-long
                submit_selection = st.button("Submit Selection")
                if submit_selection and selected_row is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row)
                    session_state.my_list.append(selected_row)

                ## For Equity Fund 2
                if session_state.suggestions2 is None:
                    session_state.suggestions2 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn2 = st.button("New Options for Equity 2")
                with col2:
                    enter_amc_btn2 = st.button("Enter AMC for Equity Fund 2")

                if new_options_btn2:
                    session_state.suggestions2 = options(data, 'Equity')

                submit_amc2 = st.selectbox("Select AMC for Equity Fund 2:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn2 and submit_amc2 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc2 = submit_amc2
                    st.write("AMC:", session_state.selected_amc2)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc2]
                    session_state.suggestions2 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions2)
                selected_row2 = st.selectbox("Select a row", session_state.suggestions2.index.tolist()) # pylint: disable=line-too-long
                submit_selection2 = st.button("Submit Equity 2 Selection")
                if submit_selection2 and selected_row2 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row2)
                    session_state.my_list.append(selected_row2)

                ## For Equity Fund 3
                if session_state.suggestions3 is None:
                    session_state.suggestions3 = options(data, 'Equity')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn3 = st.button("New Options for Equity 3")
                with col2:
                    enter_amc_btn3 = st.button("Enter AMC for Equity Fund 3")

                if new_options_btn3:
                    session_state.suggestions3 = options(data, 'Equity')

                submit_amc3 = st.selectbox("Select AMC for Equity Fund 3:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn3 and submit_amc3 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc3 = submit_amc3
                    st.write("AMC:", session_state.selected_amc3)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc3]
                    session_state.suggestions3 = options(temp_data, 'Equity')

                st.dataframe(session_state.suggestions3)
                selected_row3 = st.selectbox("Select a row", session_state.suggestions3.index.tolist()) # pylint: disable=line-too-long
                submit_selection3 = st.button("Submit Equity 3 Selection")
                if submit_selection3 and selected_row3 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row3)
                    session_state.my_list.append(selected_row3)

                ## For Hybrid Fund
                if session_state.suggestions4 is None:
                    session_state.suggestions4 = options(data, 'Hybrid')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn4 = st.button("New Options for Hybrid")
                with col2:
                    enter_amc_btn4 = st.button("Enter AMC for Hybrid Fund")

                if new_options_btn4:
                    session_state.suggestions4 = options(data, 'Hybrid')

                submit_amc4 = st.selectbox("Select AMC for Hybrid Fund:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn4 and submit_amc4 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc4 = submit_amc4
                    st.write("AMC:", session_state.selected_amc4)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc4]
                    session_state.suggestions4 = options(temp_data, 'Hybrid')

                st.dataframe(session_state.suggestions4)
                selected_row4 = st.selectbox("Select a row", session_state.suggestions4.index.tolist()) # pylint: disable=line-too-long
                submit_selection4 = st.button("Submit Hybrid Selection")
                if submit_selection4 and selected_row4 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row4)
                    session_state.my_list.append(selected_row4)

                ## For Debt Fund
                if session_state.suggestions5 is None:
                    session_state.suggestions5 = options(data, 'Debt')

                col1, col2 = st.columns(2)
                with col1:
                    new_options_btn5 = st.button("New Options for Debt")
                with col2:
                    enter_amc_btn5 = st.button("Enter AMC for Debt Fund")

                if new_options_btn5:
                    session_state.suggestions5 = options(data, 'Debt')

                submit_amc5 = st.selectbox("Select AMC for Debt Fund:", data.amc_name.unique().tolist()) # pylint: disable=line-too-long

                if enter_amc_btn5 and submit_amc5 is not None:
                    st.success("AMC selected!")
                    session_state.selected_amc5 = submit_amc5
                    st.write("AMC:", session_state.selected_amc5)
                    temp_data = data.loc[data.amc_name == session_state.selected_amc5]
                    session_state.suggestions5 = options(temp_data, 'Debt')

                st.dataframe(session_state.suggestions5)
                selected_row5 = st.selectbox("Select a row", session_state.suggestions5.index.tolist()) # pylint: disable=line-too-long
                submit_selection5 = st.button("Submit Debt Selection")
                if submit_selection5 and selected_row5 is not None:
                    st.success('Selected Row Submitted Succesfully!')
                    st.write("Selected Row:", selected_row5)
                    session_state.my_list.append(selected_row5)

                ## For Final Display for Portfolio
                if len(session_state.my_list) == 5:
                    print("List: ",session_state.my_list)
                    calculate(data, session_state.input_amount, session_state.input_age, session_state.my_list) # pylint: disable=line-too-long
                if len(session_state.my_list) > 5:
                    st.error('''Only two funds are supposed to be Selected!\
                             \nPlease reload and Try Again''')
                    reset_button = st.button("Reset")
                    if reset_button:
                        reset_state()
                        st.experimental_rerun()






if __name__ == "__main__":
    main()


    st.write("---")
    st.header("Feedback Form")
    st.write("We value your feedback! Please share your thoughts below.")

    # Feedback form fields
    name = st.text_input("Name")
    email = st.text_input("Email")
    feedback = st.text_area("Your Feedback")
    rating = st.slider("Rate Your Experience", 1, 5, 3)

    # Submit feedback button
    if st.button("Submit Feedback"):
        if name and email and feedback:
            st.success(f"Thank you, {name}! Your feedback has been submitted.")
            # Optional: Save the feedback to a database or log
        else:
            st.error("Please fill out all the fields before submitting.")

    # Email button
    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <a href="mailto:Group15@gmail.com?subject=Feedback&body=Hello Team,%0A%0A">
                <button style="background-color:green;color:white;border:none;padding:10px 15px;border-radius:5px;cursor:pointer;">
                    Send Email
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
# End-of-file (EOF)
