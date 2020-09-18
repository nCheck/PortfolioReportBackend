import pandas as pd
import datetime


writer = pd.ExcelWriter('Portfolio_Report.xlsx', engine='xlsxwriter')
client_id='J001'

broker_name='AIM'

def createExcel(sheetname,cid,sheet_st,broker,df):
   
    
    
    df.to_excel(writer, sheet_name=sheetname,startrow=10,startcol=1)
    worksheet = writer.sheets[sheetname]
    worksheet.set_column('B:M',18)
    cell_format = writer.book.add_format({'bold': True, 'italic': True,'color':'blue'})
    worksheet.write('B2',broker,cell_format)
    worksheet.write('B5','Client ID')
    worksheet.write('C5',cid)
    worksheet.write('B7',sheet_st)
  
#summary method


def summary(security,holdings,currentval,unrealized,unrealizedper):
    # data for SUMMARY********************************
    #sec_type=['Equity','Bond','TOTAL']
    #holdings_buy_value=[1770.5,1766,3536.5]
    #current_value=[1936,1777,3674]
    #unrealized_pl=[165.5,-28,137.5]
    #unrealized_pl_percent=[9.3476,-1.5855,7.7621]
    sec_type=security
    holdings_buy_value=holdings
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    
    sheetname='SUMMARY'
    summary_st='SUMMARY Statement as on '+str(datetime.date.today())
    summary = {'Security Type': sec_type,
            'Holdings Buy Value': holdings_buy_value,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent
            }
    df1 = pd.DataFrame(summary, columns = ['Security Type', 'Holdings Buy Value','Current Value','Unrealized P&L','Unrealized P&L%'])
    df1.set_index('Security Type', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df1)

    
def equity(symbol,isin,sector,quant,buy,holdings,prevprice,currentval,unrealized,unrealizedper):
    #data for equity holdings****************************

    #Symbol=['LLL','HDFC']
    #ISIN=['IJIIJI87987','IHINJKN898']
    #SECTOR=['Health Care','Financials']
    #qty=[2,1]
    #buy_av=[885,1766]
    #holdings_buy_value=[1770.5,1766]
    #prev_clos_price=[444,1788]
    #current_value=[1936,1777]
    #unrealized_pl=[165.5,-28]
    #unrealized_pl_percent=[9.3476,-1.5855]
    Symbol=symbol
    ISIN=isin
    SECTOR=sector
    qty=quant
    buy_av=buy
    holdings_buy_value=holdings
    prev_clos_price=prevprice
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    
    sheetname='EQ HOLDINGS'
    summary_st='Eq Holdings Statement as on '+str(datetime.date.today())
    eqholding={'Symbol':Symbol,'ISIN':ISIN,'SECTOR':SECTOR,'Qty Available':qty,'Buy Average':buy_av,'Holdings Buy Value':holdings_buy_value,'Previous Closing Price':prev_clos_price,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent}
    df2 = pd.DataFrame(eqholding, columns = ['Symbol', 'ISIN','SECTOR','Qty Available','Buy Average','Holdings Buy Value','Previous Closing Price','Current Value','Unrealized P&L','Unrealized P&L%'])
    df2.set_index('Symbol', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df2)
    
    
def bonds(symbol,isin,sector,quant,buy,holdings,prevprice,currentval,unrealized,unrealizedper,accrued,maturity):
    #data for bond holdings****************************

    #Symbol=['LLL','HDFC']
    #ISIN=['IJIIJI87987','IHINJKN898']
    #SECTOR=['Health Care','Financials']
    #qty=[2,1]
    #buy_av=[885,1766]
    #holdings_buy_value=[1770.5,1766]
    #prev_clos_price=[444,1788]
    #current_value=[1936,1777]
    #unrealized_pl=[165.5,-28]
    #unrealized_pl_percent=[9.3476,-1.5855]
    #accrued_int=[40,30]
    #mat_date=['1/31/2021','4/25/2023']
    Symbol=symbol
    ISIN=isin
    SECTOR=sector
    qty=quant
    buy_av=buy
    holdings_buy_value=holdings
    prev_clos_price=prevprice
    current_value=currentval
    unrealized_pl=unrealized
    unrealized_pl_percent=unrealizedper
    accrued_int=accrued
    mat_date=maturity

    sheetname='BOND HOLDINGS'
    summary_st='BOND Holdings Statement as on '+str(datetime.date.today())
    bondholding={'Symbol':Symbol,'ISIN':ISIN,'SECTOR':SECTOR,'Qty Available':qty,'Buy Average':buy_av,'Holdings Buy Value':holdings_buy_value,'Previous Closing Price':prev_clos_price,'Current Value':current_value,'Unrealized P&L':unrealized_pl,'Unrealized P&L%':unrealized_pl_percent,'Accrued Interest':accrued_int,'Maturity Date':mat_date}
    df3 = pd.DataFrame(bondholding, columns = ['Symbol', 'ISIN','SECTOR','Qty Available','Buy Average','Holdings Buy Value','Previous Closing Price','Current Value','Unrealized P&L','Unrealized P&L%','Accrued Interest','Maturity Date'])
    df3.set_index('Symbol', inplace=True)

    createExcel(sheetname,client_id,summary_st,broker_name,df3)

def saveExcel():
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()