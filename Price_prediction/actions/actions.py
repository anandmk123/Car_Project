from rasa_sdk.events import SlotSet
import requests
from typing import Text, Any, Dict, List
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from fuzzywuzzy import process

class ValidateCarDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_car_details_form"
    
    def validate_brand(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            """Validate `brand` value with case-insensitive fuzzy matching and format the output correctly."""

            ALLOWED_BRANDS = [
                'maruti', 'hyundai', 'ford', 'renault', 'mini', 'mercedes-benz', 
                'toyota', 'volkswagen', 'honda', 'mahindra', 'datsun', 'tata', 
                'kia', 'bmw', 'audi', 'land rover', 'jaguar', 'mg', 'isuzu', 
                'porsche', 'skoda', 'volvo', 'lexus', 'jeep', 'maserati', 
                'bentley', 'nissan', 'ferrari', 'mercedes-amg', 
                'rolls-royce', 'force'
            ]

            # Convert user input to lowercase for case-insensitive matching
            slot_value_lower = slot_value.lower()

            # Perform fuzzy matching
            result = process.extractOne(slot_value_lower, ALLOWED_BRANDS, score_cutoff=80)

            if result:  # Check if a match was found
                match, score = result
                # Format the matched brand with proper capitalization
                formatted_brand = match.capitalize() if ' ' not in match else ' '.join(word.capitalize() for word in match.split())
                
                dispatcher.utter_message(text=f"Great! You have a {formatted_brand} car.")
                return {"brand": formatted_brand}
            else:
                dispatcher.utter_message(text="Sorry, I didn't recognize that brand. Please try again.")
                return {"brand": None}

    def validate_model(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `model` value with case-insensitive fuzzy matching and format the output."""

        ALLOWED_MODELS = [
            "alto", "grand", "i20", "ecosport", "wagon r", "i10", "venue", "swift", "verna", "duster",
            "cooper", "ciaz", "c-class", "innova", "baleno", "swift dzire", "vento", "creta", "city",
            "bolero", "fortuner", "kwid", "amaze", "santro", "xuv500", "kuv100", "ignis", "redigo",
            "scorpio", "marazzo", "aspire", "figo", "vitara", "tiago", "polo", "seltos", "celerio", "go",
            "cr-v", "endeavour", "kuv", "jazz", "a4", "tigor", "ertiga", "safari", "thar", "hexa", "rover",
            "eeco", "a6", "e-class", "q7", "z4", "xf", "x5", "hector", "civic", "d-max", "cayenne", "x1",
            "rapid", "freestyle", "superb", "nexon", "xuv300", "dzire vxi", "s90", "wr-v", "xl6", "triber",
            "es", "wrangler", "camry", "elantra", "yaris", "gl-class", "s-presso", "dzire lxi", "aura",
            "xc", "ghibli", "continental", "cr", "kicks", "s-class", "tucson", "harrier", "x3", "octavia",
            "compass", "cls", "redi-go", "glanza", "macan", "x4", "dzire zxi", "xc90", "f-pace", "a8",
            "mux", "gtc4lusso", "gls", "x-trail", "xe", "xc60", "panamera", "alturas", "altroz", "nx",
            "carnival", "rx", "ghost", "quattroporte", "gurkha"
        ]

        # Convert user input to lowercase for case-insensitive matching
        slot_value_lower = slot_value.lower()

        # Find the closest match with a threshold of 80% similarity
        result = process.extractOne(slot_value_lower, ALLOWED_MODELS, score_cutoff=80)

        if result:  # Check if a match was found
            match, score = result
            # Format the match to title case (First letter capital, rest lowercase)
            formatted_match = match.capitalize()
            dispatcher.utter_message(text=f"Nice! Your car model is {formatted_match}.")
            return {"model": formatted_match}  # Fill slot with title-cased match
        else:
            dispatcher.utter_message(text="Sorry, I didn't recognize that model. Please try again.")
            return {"model": None}

    def validate_km_driven(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `km_driven` value."""
        
        try:
            # Convert slot_value to an integer
            km_driven_value = int(slot_value)
            
            # Check if the value is valid
            if km_driven_value < 0:
                dispatcher.utter_message(text="Please provide a valid number for kilometers driven (greater than or equal to 0).")
                return {"km_driven": None}

            dispatcher.utter_message(text=f"Great! Your car has driven {km_driven_value} kilometers.")
            return {"km_driven": km_driven_value}
        
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid number for kilometers driven.")
            return {"km_driven": None}
  
    def validate_fuel_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `fuel_type` value with case-insensitive fuzzy matching and format the output correctly."""
        
        # List of allowed fuel types in lowercase for matching
        ALLOWED_FUEL_TYPES = [
            'petrol', 'diesel', 'electric'
        ]
        
        # Convert user input to lowercase for matching
        slot_value_lower = slot_value.lower()

        # Find the closest match with a threshold of 80% similarity
        match, score = process.extractOne(slot_value_lower, ALLOWED_FUEL_TYPES, score_cutoff=80)

        if match:
            # Format the matched fuel type with proper capitalization
            formatted_fuel_type = match.capitalize()
            
            dispatcher.utter_message(text=f"Nice choice! Your car uses {formatted_fuel_type} fuel.")
            return {"fuel_type": formatted_fuel_type}
        else:
            dispatcher.utter_message(text="Sorry, I didn't recognize that fuel type. Please try again with options like petrol, diesel, or electric.")
            return {"fuel_type": None}    


    def validate_transmission_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `transmission_type` value using fuzzy matching with proper formatting."""

        # List of allowed transmission types in lowercase for matching
        ALLOWED_TRANSMISSION_TYPES = [
            'automatic', 'manual'
        ]
        
        # Convert user input to lowercase for matching
        slot_value_lower = slot_value.lower()

        # Find the closest match with a threshold of 80% similarity
        matched_transmission, score = process.extractOne(slot_value_lower, ALLOWED_TRANSMISSION_TYPES, score_cutoff=80)

        if matched_transmission:
            # Format the matched transmission type with proper capitalization
            formatted_transmission_type = matched_transmission.capitalize()
            
            dispatcher.utter_message(text=f"Got it! Your car has a {formatted_transmission_type} transmission.")
            return {"transmission_type": formatted_transmission_type}
        else:
            dispatcher.utter_message(text="Sorry, I didn't recognize that transmission type. Please try again with options like automatic or manual.")
            return {"transmission_type": None}   


    def validate_mileage(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `mileage` value."""
        try:
            # Convert slot_value to float
            mileage_value = float(slot_value)

            # Validate that mileage is greater than or equal to 0 and less than 50
            if mileage_value < 0:
                dispatcher.utter_message(text="Please provide a valid mileage value (greater than or equal to 0).")
                return {"mileage": None}
            elif mileage_value >= 50:
                dispatcher.utter_message(text="Mileage should be less than 50 km/l.")
                return {"mileage": None}
            
            dispatcher.utter_message(text=f"Your car has a mileage of {mileage_value} km/l.")
            return {"mileage": mileage_value}
        
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid number for mileage.")
            return {"mileage": None}


    def validate_engine(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `engine` value."""
        try:
            # Convert slot_value to integer
            engine_value = int(slot_value)

            # Validate that engine is within the range of 500 to 5000 cc
            if engine_value < 500:
                dispatcher.utter_message(text="Engine capacity must be at least 500 cc.")
                return {"engine": None}
            elif engine_value > 5000:
                dispatcher.utter_message(text="Engine capacity must not exceed 5000 cc.")
                return {"engine": None}

            dispatcher.utter_message(text=f"Your car has an engine capacity of {engine_value} cc.")
            return {"engine": engine_value}
        
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid engine capacity in cc.")
            return {"engine": None}


    def validate_max_power(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `max_power` value (bhp)."""
        try:
            bhp_value = float(slot_value)
            if bhp_value <= 10 or bhp_value >= 1000:
                dispatcher.utter_message(text="Please provide a valid bhp value (between 10 and 1000).")
                return {"max_power": None}
            dispatcher.utter_message(text=f"Your car has a maximum power of {bhp_value} bhp.")
            return {"max_power": bhp_value}
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid number for maximum power.")
            return {"max_power": None}


    def validate_seats(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `seats` value."""
        try:
            seats_value = int(slot_value)
            if seats_value < 1 or seats_value >= 10:
                dispatcher.utter_message(text="Please provide a valid number of seats (between 1 and 9).")
                return {"seats": None}
            dispatcher.utter_message(text=f"Your car has {seats_value} seats.")
            return {"seats": seats_value}
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid number for the number of seats.")
            return {"seats": None}


    def validate_year_of_manufacture(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `year_of_manufacture` value."""
        try:
            year = int(slot_value)
            if year <= 1900 or year > 2024:
                dispatcher.utter_message(text="Please provide a valid year of manufacture (between 1901 and 2024).")
                return {"year_of_manufacture": None}
            dispatcher.utter_message(text=f"Got it! Your car was manufactured in {year}.")
            return {"year_of_manufacture": year}
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid number for the year of manufacture.")
            return {"year_of_manufacture": None}



class ActionClearSlots(Action):
    def name(self) -> str:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) -> list:

        # List of slots to clear
        slots_to_clear = [
            "brand",
            "model",
            "km_driven",
            "mileage",
            "fuel_type",
            "transmission_type",
            "engine",
            "max_power",
            "seats",
            "year_of_manufacture"
        ]
        
        # Clear the slots by setting them to None
        cleared_slots = [SlotSet(slot, None) for slot in slots_to_clear]

        # Print statement after clearing slots
        dispatcher.utter_message(text="Got it! I've cleared the details. Ready to start fresh? Just type 'hi' whenever you're set to go again!")

        # Return cleared slots
        return cleared_slots

class ActionPredictCarPrice(Action):
    def name(self) -> str:
        return "action_predict_car_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Extract the required slot values
        brand = tracker.get_slot('brand')
        model = tracker.get_slot('model')
        year_of_manufacture = tracker.get_slot('year_of_manufacture')
        km_driven = tracker.get_slot('km_driven')
        fuel_type = tracker.get_slot('fuel_type')
        transmission_type = tracker.get_slot('transmission_type')
        mileage = tracker.get_slot('mileage')
        engine = tracker.get_slot('engine')
        max_power = tracker.get_slot('max_power')
        seats = tracker.get_slot('seats')

        # Construct the API URL
        api_url = f"http://127.0.0.1:5000/predict_price?brand={brand}&model={model}&year_of_manufacture={year_of_manufacture}&km_driven={km_driven}&fuel_type={fuel_type}&transmission_type={transmission_type}&mileage={mileage}&engine={engine}&max_power={max_power}&seats={seats}"

        try:
            # Make a GET request to the API
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses

            # Extract price from the response
            price_data = response.json()  # Assuming the API returns JSON
            price = price_data.get('predicted_price', 'Not available')  # Adjust key as necessary

            # Send the price back to the user
            dispatcher.utter_message(text=f"The predicted price of the car is: {price:.2f}")

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the price. Please try again later.")
            print(f"Error occurred: {e}")  # Log the error for debugging

        return []


class ActionMaxContribution(Action):
    def name(self) -> str:
        return "action_max_contribution"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # List of required slots
        required_slots = [
            'brand', 
            'model', 
            'year_of_manufacture', 
            'km_driven', 
            'fuel_type', 
            'transmission_type', 
            'mileage', 
            'engine', 
            'max_power', 
            'seats'
        ]

        # Check if all required slots are filled
        missing_slots = [slot for slot in required_slots if not tracker.get_slot(slot)]

        if missing_slots:
            # Generate message indicating which slots are missing
            missing_slot_names = ', '.join(missing_slots)
            dispatcher.utter_message(
                text=f"Sorry, I need the following information to proceed: {missing_slot_names}. Please provide them."
            )
            return []

        # Extract the required slot values
        brand = tracker.get_slot('brand')
        model = tracker.get_slot('model')
        year_of_manufacture = tracker.get_slot('year_of_manufacture')
        km_driven = tracker.get_slot('km_driven')
        fuel_type = tracker.get_slot('fuel_type')
        transmission_type = tracker.get_slot('transmission_type')
        mileage = tracker.get_slot('mileage')
        engine = tracker.get_slot('engine')
        max_power = tracker.get_slot('max_power')
        seats = tracker.get_slot('seats')

        # Construct the API URL with the car details
        api_url = f"http://127.0.0.1:5000/max_contribution?brand={brand}&model={model}&year_of_manufacture={year_of_manufacture}&km_driven={km_driven}&fuel_type={fuel_type}&transmission_type={transmission_type}&mileage={mileage}&engine={engine}&max_power={max_power}&seats={seats}"

        try:
            # Make a GET request to the API
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses

            # Extract data from the JSON response
            contribution_data = response.json()
            highest_contributing_feature = contribution_data.get("highest_contributing_feature", "Unknown feature")
            # Remove 'remainder__' from the feature name if it exists
            highest_contributing_feature = highest_contributing_feature.replace("remainder__", "")
            percentage_contribution = contribution_data.get("percentage_contribution", 0)

            # Send a message with the highest contributing feature and percentage
            dispatcher.utter_message(
                text=f"The feature contributing the most to the price is '{highest_contributing_feature}', "
                     f"accounting for approximately {percentage_contribution:.2f}% of the prediction."
            )

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the information. Please try again later.")
            print(f"Error occurred: {e}")  # Log the error for debugging

        return []