''' This file contains necessary custom built functions '''
from random import sample
import streamlit as st

def recommend(df, category):
    ''' Filter for Fund Recommendation '''
    categorized = df.loc[df['category']==category]
    sortinized = categorized.loc[df['sortino'] > 0.9 ]
    beta = sortinized.loc[(df['beta'] < 1)]
    sharpe = beta.loc[df['sharpe'] > 1 ]
    alpha = sharpe.loc[df['alpha'] > 0 ]
    alpha = alpha.sort_values(by='alpha', ascending=False)
    return alpha.head(15)

def options(df, category):
    ''' Function displays 3 randomly choosen rows from the dataset '''
    df1 = recommend(df, category)
    row_numbers = df1.index.to_list()
    try:
        random_rows = sample(row_numbers, 3)
    except:
        random_rows = row_numbers
    df2 = df.loc[random_rows]
    return df2

def options2(df, category):
    ''' Function displays 3 randomly choosen rows from the dataset '''
    df2 = df.loc[df['category'] == category]
    return df2

def calculator(investment, rating, years):
    ''' This Function will calculate the Future Value of Individual Funds '''
    months = years * 12

    i = rating/100/12 #Compound Interest

    a = (1+i)**months-1
    b = (1+i)/i

    futval = investment * a * b # Future Value

    return futval

def calculate(df, amount, age, row):
    ''' This Function will calculate Future Value of Entire Portfolio '''
    st.title("Your Expected Portfolio:")
    st.write("Following are the Funds you have chosen: ")
    data = df.loc[row]
    st.dataframe(data)

    if amount <= 5000:
        if age < 18:
            equity = amount

            a = df.loc[row]
            rate = a.returns_1yr
            equity1 = calculator(equity, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(equity, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(equity, rate, 5)

            #Calculating Returns
            
            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            equity1 = float(equity1)
            st.write(f'Total Portfolio Value = {equity1:.2f}')

            totalgain = equity1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            equity3 = float(equity3)
            st.write(f'Total Portfolio Value = {equity3:.2f}')

            totalgain = equity3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            equity5 = float(equity5)
            st.write(f'Total Portfolio Value = {equity5:.2f}')

            totalgain = equity5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

        else:
            var = 100 - age
            per = var/100
            equity = amount * per
            hybrid = amount - equity

            #For Equity
            a = df.loc[row[0]]
            rate = a.returns_1yr
            equity1 = calculator(equity, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(equity, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(equity, rate, 5)

            #For Hybrid
            a = df.loc[row[1]]
            rate = a.returns_1yr
            hybrid1 = calculator(hybrid, rate, 1)

            rate = a.returns_3yr
            hybrid3 = calculator(hybrid, rate, 3)

            rate = a.returns_5yr
            hybrid5 = calculator(hybrid, rate, 5)

            #Calculating Returns

            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year1 = float(equity1) + float(hybrid1)
            st.write(f'Total Portfolio Value = {year1:.2f}')

            totalgain = year1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year3 = float(equity3) + float(hybrid3)
            st.write(f'Total Portfolio Value = {year3:.2f}')

            totalgain = year3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year5 = float(equity5) + float(hybrid5)
            st.write(f'Total Portfolio Value = {year5:.2f}')

            totalgain = year5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

    elif amount > 5000 and amount <= 10000:
        if age < 18:
            amount1 = amount/2
            amount2 = amount/2

            a = df.loc[row[0]]
            rate = a.returns_1yr
            equity1 = calculator(amount1, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(amount1, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(amount1, rate, 5)

            b = df.loc[row[1]]
            rate = b.returns_1yr
            equity21 = calculator(amount2, rate, 1)

            rate = b.returns_3yr
            equity23 = calculator(amount2, rate, 3)

            rate = b.returns_5yr
            equity25 = calculator(amount2, rate, 5)


            #Calculating Returns

            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year1 = equity1 + equity21
            st.write(f'Total Portfolio Value = {year1:.2f}')

            totalgain = year1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year3 = equity3 + equity23
            st.write(f'Total Portfolio Value = {year3:.2f}')

            totalgain = year3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year5 = equity5 + equity25
            st.write(f'Total Portfolio Value = {year5:.2f}')

            totalgain = year5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

        else:
            var = 100 - age
            per = var/100
            equity = amount * per
            var2 = amount - equity
            hybrid = var2 / 2
            debt = var2 / 2

            #for equity funds
            fund1 = equity/2
            fund2 = equity/2

            #For Equity Fund 1
            a = df.loc[row[0]]
            rate = a.returns_1yr
            equity1 = calculator(fund1, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(fund1, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(fund1, rate, 5)

            #For Equity Fund 2
            a = df.loc[row[1]]
            rate = a.returns_1yr
            equity21 = calculator(fund2, rate, 1)

            rate = a.returns_3yr
            equity23 = calculator(fund2, rate, 3)

            rate = a.returns_5yr
            equity25 = calculator(fund2, rate, 5)

            #For Hybrid
            a = df.loc[row[2]]
            rate = a.returns_1yr
            hybrid1 = calculator(hybrid, rate, 1)

            rate = a.returns_3yr
            hybrid3 = calculator(hybrid, rate, 3)

            rate = a.returns_5yr
            hybrid5 = calculator(hybrid, rate, 5)

            #For Debt
            a = df.loc[row[3]]
            rate = a.returns_1yr
            debt1 = calculator(debt, rate, 1)

            rate = a.returns_3yr
            debt3 = calculator(debt, rate, 3)

            rate = a.returns_5yr
            debt5 = calculator(debt, rate, 5)

            #Calculating Returns

            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year1 = equity1 + equity21 + hybrid1 + debt1
            st.write(f'Total Portfolio Value = {year1:.2f}')

            totalgain = year1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year3 = equity3 + equity23 + hybrid3 + debt3
            st.write(f'Total Portfolio Value = {year3:.2f}')

            totalgain = year3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year5 = equity5 + equity25 + hybrid5 + debt5
            st.write(f'Total Portfolio Value = {year5:.2f}')

            totalgain = year5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

    elif amount > 10000:
        if age < 18:
            amount1 = amount/3
            amount2 = amount/3
            amount3 = amount/3

            a = df.loc[row[0]]
            rate = a.returns_1yr
            equity1 = calculator(amount1, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(amount1, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(amount1, rate, 5)

            b = df.loc[row[1]]
            rate = b.returns_1yr
            equity21 = calculator(amount2, rate, 1)

            rate = b.returns_3yr
            equity23 = calculator(amount2, rate, 3)

            rate = b.returns_5yr
            equity25 = calculator(amount2, rate, 5)

            c = df.loc[row[2]]
            rate = c.returns_1yr
            equity31 = calculator(amount3, rate, 1)

            rate = c.returns_3yr
            equity33 = calculator(amount3, rate, 3)

            rate = c.returns_5yr
            equity35 = calculator(amount3, rate, 5)

            #Calculating Returns

            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year1 = equity1 + equity21 + equity31
            st.write(f'Total Portfolio Value = {year1:.2f}')

            totalgain = year1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year3 = equity3 + equity23 + equity33
            st.write(f'Total Portfolio Value = {year3:.2f}')

            totalgain = year3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year5 = equity5 + equity25 + equity35
            st.write(f'Total Portfolio Value = {year5:.2f}')

            totalgain = year5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

        else:
            var = 100 - age
            per = var/100
            equity = amount * per
            var2 = amount - equity
            hybrid = var2 / 2
            debt = var2 / 2

            #for equity funds
            fund1 = equity/3
            fund2 = equity/3
            fund3 = equity/3

            #For Equity Fund 1
            a = df.loc[row[0]]
            rate = a.returns_1yr
            equity1 = calculator(fund1, rate, 1)

            rate = a.returns_3yr
            equity3 = calculator(fund1, rate, 3)

            rate = a.returns_5yr
            equity5 = calculator(fund1, rate, 5)

            #For Equity Fund 2
            a = df.loc[row[1]]
            rate = a.returns_1yr
            equity21 = calculator(fund2, rate, 1)

            rate = a.returns_3yr
            equity23 = calculator(fund2, rate, 3)

            rate = a.returns_5yr
            equity25 = calculator(fund2, rate, 5)

            #For Equity Fund 3
            c = df.loc[row[2]]
            rate = c.returns_1yr
            equity31 = calculator(fund3, rate, 1)

            rate = c.returns_3yr
            equity33 = calculator(fund3, rate, 3)

            rate = c.returns_5yr
            equity35 = calculator(fund3, rate, 5)

            #For Hybrid
            a = df.loc[row[3]]
            rate = a.returns_1yr
            hybrid1 = calculator(hybrid, rate, 1)

            rate = a.returns_3yr
            hybrid3 = calculator(hybrid, rate, 3)

            rate = a.returns_5yr
            hybrid5 = calculator(hybrid, rate, 5)

            #For Debt
            a = df.loc[row[4]]
            rate = a.returns_1yr
            debt1 = calculator(debt, rate, 1)

            rate = a.returns_3yr
            debt3 = calculator(debt, rate, 3)

            rate = a.returns_5yr
            debt5 = calculator(debt, rate, 5)

            #Calculating Returns

            ## for 1 year
            st.write("Returns for 1 Year \n")
            totalinv = amount * 12
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year1 = equity1 + equity21 + equity31 + hybrid1 + debt1
            st.write(f'Total Portfolio Value = {year1:.2f}')

            totalgain = year1 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 3 years
            st.write('\nReturns for 3 Years\n')
            totalinv = amount * 36
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year3 = equity3 + equity23 + equity33 + hybrid3 + debt3
            st.write(f'Total Portfolio Value = {year3:.2f}')

            totalgain = year3 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')

            ## for 5 years
            st.write('\nReturns for 5 Years\n')
            totalinv = amount * 60
            st.write(f'Total Amount Invested = {totalinv:.2f}')

            year5 = float(equity5) + float(equity25) + float(equity35) + float(hybrid5) + float(debt5) # pylint: disable=line-too-long
            st.write(f'Total Portfolio Value = {year5:.2f}')

            totalgain = year5 - totalinv
            st.write(f'Net Profit = {totalgain:.2f}')

            gainper = totalgain/totalinv*100
            st.write(f'Percentage Gained = {gainper:.2f}')
