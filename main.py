from fuzzywuzzy import fuzz
import math

class Profile:
  
  def __init__(self, first_name,last_name,date_of_birth, class_year, email_field):
      self.first_name = first_name
      self.last_name = last_name
      self.date_of_birth = date_of_birth
      self.class_year = class_year
      self.email_field = email_field

  def getDetails(self):
    print(self.first_name , self.last_name)

class ProfileComparator:

  class Name_Email:
    name_email = []

    def add_field(self, field):
      self.name_email.append(field)

    def get_name_email(self):
      return self.name_email

      
  total_score = 0
  firstName_lastName_email_match_score = 0
  matching_attributes = []
  none_matching_attributes = []
  all_fields = ["first_name" , "last_name", "email_field", "class_year","date_of_birth"]
  name_email = Name_Email()

  def remove_field(self, field):
    self.all_fields.remove(field)
  
  def get_similarity(self , p1 , p2 , field):
    return fuzz.ratio(getattr(p1, field), getattr(p2, field))

  def check_if_null(self, p1, p2, field):
    return getattr(p1, field) == None or getattr(p2, field) == None

  def check_if_matches(self, p1, p2, field):
    return getattr(p1, field) == getattr(p2, field)

  def increase_score(self):
    self.total_score += 1

  def decrease_score(self):
    self.total_score -= 1

  

  def find_duplicates_between_two_profiles(self,p1, p2, fields):
    for field in fields:
      if field == 'first_name':
        self.remove_field(field)
        self.firstName_lastName_email_match_score += self.get_similarity(p1, p2, field)
        self.name_email.add_field(field)
        continue
      if field == 'last_name':
        self.remove_field(field)
        self.firstName_lastName_email_match_score += self.get_similarity(p1, p2, field)
        self.name_email.add_field(field)
        continue
      if field == 'email_field':
        self.remove_field(field)
        self.firstName_lastName_email_match_score += self.get_similarity(p1, p2, field)
        self.name_email.add_field(field)
        continue
      if field == 'date_of_birth':
        if self.check_if_null(p1, p2, field): 
          continue
        if self.check_if_matches(p1, p2, field):
          self.remove_field(field)
          self.matching_attributes.append(field)
          self.increase_score()
        else :
          self.none_matching_attributes.append(field)
          self.decrease_score()
          
      if field == 'class_year':
        if self.check_if_null(p1, p2, field):
          continue
        if self.check_if_matches(p1, p2, field):
          self.remove_field(field)
          self.matching_attributes.append(field)
          self.increase_score()
        else :
          self.none_matching_attributes.append(field)
          self.decrease_score()

    name_email_fields = self.name_email.get_name_email()
    length_of_name_email_fields = len(name_email_fields)
    if(math.floor(self.firstName_lastName_email_match_score / length_of_name_email_fields) > 80):
      self.increase_score()
      for field in name_email_fields:
        self.matching_attributes.append(field)
    else:
      for field in name_email_fields:
        self.none_matching_attributes.append(field)
      
    
    if(self.total_score >= 0):
      print(p1.first_name , p2.first_name)
      print("total match score :" + str(self.total_score))
      print("matching attribute :",self.matching_attributes if len(self.matching_attributes) else "None")
      print("non matching attributes : ", self.none_matching_attributes if len(self.none_matching_attributes) else "None")
      print("ignored attributes : ", self.all_fields if len(self.all_fields) else "None")
    return self.total_score



def find_duplicates(profiles , fields):
  length = len(profiles)
  compareProfiles = ProfileComparator()
  for i in range(length - 1):
    print(profiles[i].first_name , profiles[i + 1].first_name)
    compareProfiles.find_duplicates_between_two_profiles(profiles[i], profiles[i + 1] , fields)
    
    

pf1 = Profile("Kanhai" , "Shah", None , None , "knowkanhai@gmail.com")
# pf1.getDetails()

pf2 = Profile("Kanhai1" , "Shah", "1999-05-03" , 2012 , "knowkanhai+donotcompare@gmail.com")
# pf2.getDetails()

find_duplicates(profiles = [pf1 , pf2] , fields = ["first_name" , "last_name","email_field","date_of_birth","class_year"])

