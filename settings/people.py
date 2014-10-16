class People(object):
  def __init__(self, info):
    self.name   = info[0]
    self.title  = info[1]
    self.email  = info[2]
    self.phone  = info[3]

  def __unicode__(self):
    return self.name

#Development Team
Tom = People(info = (
          'Tom Counsell',
          'Technical Director',
          'tom@theanou.com',
          '212662750819',
        )
      )

#Suport Team
Dan = People(info = (
          'Dan Driscoll',
          'Founder',
          'dan@theanou.com',
          '212653827628',
        )
      )

Tifawt = People(info = (
          'Tifawt Belaid',
          'Community Supporter',
          'tifawt@theanou.com',
          '212613342325',
        )
      )

Latifa = People(info= (
          'Latifa Mahna',
          'Intern',
          'latifamahna@gmail.com',
          '',
        )
      )

#Directors
Brahim = People(info = (
          'Brahim El Mansouri',
          'Director',
          'brahim@theanou.com',
          '212673753163',
        )
      )

Rabha = People(info = (
          'Rabha Akkaouai',
          'Director',
          'rabha@theanou.com',
          '212623045998',
        )
      )

Mustapha = People(info = (
          'Mustapha Chaouai',
          'Director',
          'mustapha@theanou.com',
          '212637637569',
        )
      )

Kenza = People(info = (
          'Kenza Oulaghda',
          'Director',
          'kenza@theanou.com',
          '0637637565',
        )
      )

developer_team = [Tom,]
operations_team = [Dan, Tifawt, Latifa, Brahim, Rabha, Mustapha, Kenza,]
directors = [person for person in operations_team if person.title == "Director"]
support_team = [person for person in operations_team if person.title != "Director"]

#todo: remove this whole file and use admin account information
#todo: or use this file to define groups (trainers, translators, etc)
