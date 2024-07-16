## Transaction Table

**Fields:**
- `TransactionDT`: Timedelta from a given reference datetime (not an actual timestamp)
- `TransactionAMT`: Transaction payment amount in USD
- `ProductCD`: Product code, the product for each transaction
- `card1 - card6`: Payment card information, such as card type, card category, issue bank, country, etc.
- `addr`: Address
- `dist`: Distance
- `P_` and `R__` emaildomain: Purchaser and recipient email domain
- `C1-C14`: Counting, such as how many addresses are found to be associated with the payment card, etc. (The actual meaning is masked)
- `D1-D15`: Timedelta, such as days between previous transaction, etc.
- `M1-M9`: Match, such as names on card and address, etc.
- `Vxxx`: Vesta engineered rich features, including ranking, counting, and other entity relations.

**Categorical Features:**
- `ProductCD`
- `card1 - card6`
- `addr1`, `addr2`
- `P_emaildomain`
- `R_emaildomain`
- `M1 - M9`

## Identity Table

**Fields:**
- Variables in this table are identity information – network connection information (IP, ISP, Proxy, etc.) and digital signature (UA/browser/os/version, etc.) associated with transactions.
- They're collected by Vesta’s fraud protection system and digital security partners.
- (The field names are masked and pairwise dictionary will not be provided for privacy protection and contract agreement)

**Categorical Features:**
- `DeviceType`
- `DeviceInfo`
- `id_12 - id_38`
