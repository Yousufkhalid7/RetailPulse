# RetailPulse Data Dictionary

## Source: 
    - E-commerce Business Transaction [ Kaggle ]
    - File: 'Sales Transaction v.4a.csv'
    - License - CC0 ( Pulic Domain )
    - Date downloaded - 20th October 2026

## Column Table:
    - TransactionNo - Transaction ID [ C stands for Cancellation ] - Many product line have same TransactionNo - String
    - Date - Date on which the transaction was made - String (MM/DD/YYYY) -> Date 
    - ProductNo - ProductID - String
    - ProductName - Name of the Product - String
    - Price - Unit price in pounds - float64 -> decimal 
    - Quantity - Number of products purchased in 1-transaction number ( unique transaction ) [ Negative (-ve) values means cancelled transaction ] - Integer
    - CustomerNo - Identification Number of the customer - float64 -> String 
    - Country - Name of the country from where the order was placed - String

## Findings: 
    - 536500 rows x 8 columns
    - Dates are MM/DD/YYYY ranging from 2018-12-01 to 2019-12-09
    - 8585 rows are cancellations [ Every "C" row has negative quantity and no other rows do]
    - Price ranges from 5.13 to 660.62, with no zero or negative values
    - Quantity ranges from -80995 to 80995 ( median = 3 ), probably one order placed was fully cancelled
    - 55 rows have no customer, encoded in the raw file as the text NA. pandas converts this to NaN (and the column to float); Spark keeps it as text.
    - 5200 rows are exact duplicate ( about 1% ) 

## Planned decisions for Silver:
    - Convert Date into 'MM/DD/YYYY'
    - Convert CustomerNo from float64 -> nullable integer -> string
    - Keep quantity signed; add 'is_cancellation' flag [ C and negative quantity match exactly ]. If we delete cancellations - revenue is overstated, keep them unflagged and order counts includes refunds
    - Add 'has_customer' flag; 55 rows have no columns. If we drop them, we lose real sales or refunds, if we keep them unflagged, the customer couts get distorted. Convert the NA marker to null, cast CustomerNo to integer, then to string.
    - Drop exact duplicates in Silver - 5200 identical rows; If we ignore them and dont count them, the revenue and counts are inlated by 1%
    - Churn features uses non-cancellation values only because cancellation can make a returner look like an active buyer; model learns wrong behaviour if we keep cancellation rows aswell.

    
    
