
# API Reference

For each table defined by our models, the associated routes perform all basic CRUD operations.

## Character Endpoints

#### GET /characters
- An endpoint that retrieves the list of characters.
- Requires the'get:characters' permission.
- Returns a success value and list of characters in the character.profile representation.
> Example : `curl --location --request GET "localhost:5000/characters" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"character":[{"age":"17","astrological_sign":"Aries","birthday":"April 3rd","bloodtype":"O","class_type":"Vocal","handedness":"Right","height":"158 cm","hobbies":"Baking cakes, Karaoke, Long Phone Calls","id":1,"name":"NEW","three_sizes":"83/56/82","weight":"46 kg"},{"age":"15","astrological_sign":"Pisces","birthday":"August 10th","bloodtype":"B","class_type":"Cool","handedness":"Right","height":"165 cm","hobbies":"Dancing","id":2,"name":"NEW NAME","three_sizes":"80/56/81","weight":"44 kg"},{"age":"24","astrological_sign":"Gemini","birthday":"June 12th","bloodtype":"A","class_type":"Angel","handedness":"Right","height":"143 cm","hobbies":"Appreciating North American Dramas","id":3,"name":"Baba Konomi","three_sizes":"75/55/79","weight":"37 kg"},{"age":"19","astrological_sign":"Pisces","birthday":"February 25th","bloodtype":"B","class_type":"L'Antica","handedness":"Left","height":"165 cm","hobbies":"\"My excellent home cookin'!\"","id":4,"name":"Tsukioka Kogane","three_sizes":"93/60/91","weight":"58 kg"},{"age":"16","astrological_sign":"Virgo","birthday":"September 12th","bloodtype":"O","class_type":"Pure","handedness":null,"height":"159 cm","hobbies":"Making Sweets","id":5,"name":"Minami Kotori","three_sizes":"80/58/80","weight":null},{"age":"15","astrological_sign":"Cancer","birthday":"July 13th","bloodtype":"O","class_type":"Cool","handedness":null,"height":"156 cm","hobbies":"\"Little devil\"-style fashion","id":6,"name":"Tsushima Yoshiko","three_sizes":"79/58/80","weight":null},{"age":null,"astrological_sign":"Scorpio","birthday":"July 13th","bloodtype":null,"class_type":"Roselia","handedness":null,"height":"155 cm","hobbies":"None","id":7,"name":"Yukina Minato","three_sizes":null,"weight":null}],"success":true}
```

#### GET /characters/\<id>
- An endpoint that retrieves the character of a given id.
- Requires the'get:characters' permission.
- Returns a success value and list containing only the requested character in the character.profile representation.
> Example : `curl --location --request GET "localhost:5000/characters/1" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"character":[{"age":"17","astrological_sign":"Aries","birthday":"April 3rd","bloodtype":"O","class_type":"Vocal","handedness":"Right","height":"158 cm","hobbies":"Baking cakes, Karaoke, Long Phone Calls","id":1,"name":"NEW","three_sizes":"83/56/82","weight":"46 kg"}],"success":true}
```

#### POST /characters
- An endpoint that creates a new row in the characters table. 
- Requires the 'post:character' permission.
- Returns a success value and list containing only the newly created character in the character.profile representation.
> Example: `curl http://127.0.0.1:5000/characters -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Ohishi Izumi", "age": "15", "height": "157 cm", "weight": "41 kg", "birthday": "November 11th", "astrological_sign": "Scorpio", "bloodtype": "A", "three_sizes": "83/55/82", "handedness": "Right", "hobbies": "Programming", "class_type": "Cool"}'`
```
{"character":[{"age":"15","astrological_sign":"Scorpio","birthday":"November 11th","bloodtype":"A","class_type":"Cool","handedness":"Right","height":"157 cm","hobbies":"Programming","id":2,"name":"Ohishi Izumi","three_sizes":"83/55/82","weight":"41 kg"}],"success":true}
```

#### PATCH /characters/\<id>
-   An endpoint that updates the corresponding row for \<id>. 
-   Requires the 'patch:character' permission.
-   Returns a success value and list containing only the updated character in the character.profile representation.
> Example: `curl http://127.0.0.1:5000/characters/1 -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"hobbies": "Web Development"}'`
```
{"character":[{"age":"15","astrological_sign":"Scorpio","birthday":"November 11th","bloodtype":"A","class_type":"Cool","handedness":"Right","height":"157 cm","hobbies":"Web Development","id":2,"name":"Ohishi Izumi","three_sizes":"83/55/82","weight":"41 kg"}],"success":true}
```

#### DELETE /characters/\<id>
- An endpoint that deletes the corresponding row for \<id>.
- Requires the 'delete:character' permission.
- Returns a success value and the id of the deleted record.
> Example : `curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/characters/1`
```
{"delete":1,"success":true}
```
## Card Endpoints

#### GET /cards
- An endpoint that retrieves the list of cards.
- Requires the'get:cards' permission.
- Returns a success value and list of cards in the card.info representation.
> Example : `curl --location --request GET "localhost:5000/cards" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"card":[{"character":1,"id":1,"name":"Fuwafuwa Dreaming","rarity":"SSR","skill":1,"stat_1":40,"stat_2":6416,"stat_3":3466,"stat_4":4914},{"character":1,"id":2,"name":"Cooking study!","rarity":"SSR","skill":2,"stat_1":40,"stat_2":3390,"stat_3":4828,"stat_4":6204},{"character":2,"id":3,"name":"Stage of Magic","rarity":"SSR","skill":3,"stat_1":40,"stat_2":2001,"stat_3":2028,"stat_4":2006},{"character":3,"id":4,"name":"Twinkle Star","rarity":"SR","skill":4,"stat_1":35,"stat_2":4864,"stat_3":2652,"stat_4":3786},{"character":4,"id":5,"name":"To ~ Ryanse!","rarity":"P-SR","skill":5,"stat_1":220,"stat_2":220,"stat_3":122,"stat_4":160},{"character":5,"id":6,"name":"Christmas","rarity":"UR","skill":6,"stat_1":4140,"stat_2":4830,"stat_3":3920,"stat_4":6},{"character":5,"id":7,"name":"Uniform / Natsuiro Egao de 1,2,Jump!","rarity":"R","skill":7,"stat_1":3000,"stat_2":2180,"stat_3":1810,"stat_4":3},{"character":7,"id":8,"name":"In the Glistening Waters","rarity":"4-star","skill":8,"stat_1":7401,"stat_2":6720,"stat_3":6338,"stat_4":20459}],"success":true}
```

#### GET /cards/\<id>
- An endpoint that retrieves the card of a given id.
- Requires the'get:cards' permission.
- Returns a success value and list containing only the requested card in the card.info representation.
> Example : `curl --location --request GET "localhost:5000/cards/1" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"card":[{"character":1,"id":1,"name":"Fuwafuwa Dreaming","rarity":"SSR","skill":1,"stat_1":40,"stat_2":6416,"stat_3":3466,"stat_4":4914}],"success":true}
```

#### POST /cards
- An endpoint that creates a new row in the cards table. 
- Requires the 'post:card' permission.
- Returns a success value and list containing only the newly created card in the card.info representation.
> Example: `curl http://127.0.0.1:5000/cards -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Diva of the Birdcage", "character": 7, "skill": 8, "rarity": "4-star", "stat_1": "8491", "stat_2": "4505", "stat_3": "5832", "stat_4": "18828"}'`
```
{"card":[{"character":7,"id":9,"name":"Diva of the Birdcage","rarity":"4-star","skill":8,"stat_1":8491,"stat_2":4505,"stat_3":5832,"stat_4":18828}],"success":true}
```
#### PATCH /cards/\<id>
-   An endpoint that updates the corresponding row for \<id>. 
-   Requires the 'patch:card' permission.
-   Returns a success value and list containing only the updated card in the card.info representation.
> Example: `curl http://127.0.0.1:5000/cards/1 -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"name": "FluffyFluffy Dreaming"}'`
```
{"card":[{"character":1,"id":1,"name":"FluffyFluffy Dreaming","rarity":"SSR","skill":1,"stat_1":40,"stat_2":6416,"stat_3":3466,"stat_4":4914}],"success":true}
```

#### DELETE /cards/\<id>
- An endpoint that deletes the corresponding row for \<id>.
- Requires the 'delete:card' permission.
- Returns a success value and the id of the deleted record.
> Example : `curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/cards/1`
```
{"delete":1,"success":true}
```


## Skill Endpoints

#### GET /skills
- An endpoint that retrieves the list of skills.
- Requires the'get:skills' permission.
- Returns a success value and list of skills in the skill.info representation.
> Example : `curl --location --request GET "localhost:5000/skills" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"skill":[{"description":"Every 9 seconds there is a 40% chance that the Perfect / Great score will increase by 30% for 5 seconds","id":1,"name":"One sheep ... two ... \u266a"},{"description":"Combo bonus increases by 26% for 6 seconds with a probability of 40% every 11 seconds","id":2,"name":"Delicious music, eat together \u266a"},{"description":"(Extreme Perfect Lock) Every 12 seconds: there is a 40..60% chance that Bad/Nice/Great notes will become Perfect notes for 4..6 seconds","id":3,"name":"Dashing Will"},{"description":"every 9 seconds has a 40% chance to increase Perfect score by 26% for 5 seconds","id":4,"name":"Enchanted lip"},{"description":"Vocal 3.5 times appeal / Reduce mental by 30%","id":5,"name":"Ryanse!"},{"description":"Every 10 seconds, there is a 36% chance of increasing players score by 200 points","id":6,"name":"Timer Charm"},{"description":"For every 17 hit combo string, there is a 36% chance of increasing players score by 200 points","id":7,"name":"Rhythmical Charm"},{"description":"410 Life Recovery and Score increased by 60% for 7.5 seconds","id":8,"name":"The Water's Vocals"}],"success":true}
```

#### GET /skills/\<id>
- An endpoint that retrieves the skill of a given id.
- Requires the'get:skills' permission.
- Returns a success value and list containing only the requested skill in the skill.info representation.
> Example : `curl --location --request GET "localhost:5000/skills/1" -H "Authorization: Bearer <ACCESS_TOKEN>"`
```
{"skill":[{"description":"Every 9 seconds there is a 40% chance that the Perfect / Great score will increase by 30% for 5 seconds","id":1,"name":"One sheep ... two ... \u266a"}],"success":true}
```

#### POST /skills
- An endpoint that creates a new row in the skills table. 
- Requires the 'post:skill' permission.
- Returns a success value and list containing only the newly created skill in the skill.info representation.
> Example: `curl http://127.0.0.1:5000/skills -X POST -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Violent shout", "description": "For the next 5 seconds, score of all notes boosted by +100.0%"}`
```
{"skill":[{"description":"For the next 5 seconds, score of all notes boosted by +100.0%","id":9,"name":"Violent shout"}],"success":true}
```
#### PATCH /skills/\<id>
-   An endpoint that updates the corresponding row for \<id>. 
-   Requires the 'patch:skill' permission.
-   Returns a success value and list containing only the updated skill in the skill.info representation.
> Example: `curl http://127.0.0.1:5000/skills/8 -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"description": "390 Life Recovery and Score increased by 70% for 8 seconds"}'`
```
{"skill":[{"description":"390 Life Recovery and Score increased by 70% for 8 seconds","id":8,"name":"The Water's Vocals"}],"success":true}
```

#### DELETE /skills/\<id>
- An endpoint that deletes the corresponding row for \<id>.
- Requires the 'delete:skill' permission.
- Returns a success value and the id of the deleted record.
> Example : `curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/skills/1`
```
{"delete":1,"success":true}
```

# Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 401,
    "message": "Unauthorized"
}
```
The API will return three error types when requests fail:
- 401: Unauthorized
- 404: Resource Not Found
- 422: Unprocessable
