import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards1=pd.read_csv("card_security.csv",dtype=str)

# Class 1
class Hotels:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        #get the hotel name from the csv file
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    # Method 1
    def book(self):
        """Book the hotel by changing the hotel's availability"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    # Method 2
    def available(self):
        """Update the availabilty in the csv file"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == 'yes'

# Class 2
class ReservationTicket:
    def __init__(self, cust_name, hotel_object):
        self.cust_name = cust_name
        self.hotel = hotel_object

    # Method 1
    def generate(self):
        return f"Hello {self.cust_name}, your hotel: {self.hotel.name} is booked" 

# Class 3
class CreditCard:
    def __init__(self, number):
        self.number = number

    #Method 1
    def validate(self, expiration, holder, cvv):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvv": cvv}
        
        #check if the dictionary matches the data in csv file
        if card_data in df_cards:
            return True
        return False

#inherting Credit Card class
class CCSecurity(CreditCard):
    def aunthenticate(self,given_password):
        password=df_cards1.loc[df_cards1["number"]==self.number,"password"].squeeze()
        print(password)
        if password==given_password:
            return True
        return False

class HotelSpa(Hotels):
    def generate(self,customer_name):
        self.cust_name=customer_name
        content=f"Hello {self.cust_name}, Your Hotel and Spa booking is confirmed at {self.name}"
        return content

print(df)
hotel_id = input("Enter the id of the hotel: ")

# Hotel instance
hotel = HotelSpa(hotel_id)
if hotel.available():
    #credit card instance
    credit_card = CCSecurity(number="1234")
    if credit_card.validate(expiration="12/26", holder='JOHN SMITH', cvv="123"):
        if credit_card.aunthenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            # Creating an instance
            reserv_ticket = ReservationTicket(name, hotel)
            print(reserv_ticket.generate())
            spa=input("Do you want Spa Package?:").lower()
            if spa =='yes':
                print(hotel.generate(name))
        else:
            print("Aunthetication failed")
    else:
        print("Payment issue")
else:
    print("Sorry, the hotel is not available.")
