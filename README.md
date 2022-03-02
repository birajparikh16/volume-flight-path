# Volume Python Take-Home Test

**Task** 

<b>Story:</b> There are over 100,000 flights a day, with millions of people and cargo being transferred around the world. With so many people, and different carrier/agency groups it can be hard to track where a person might be. In order to determine the flight path of a person, we must sort through all of their flight records.

<b>Goal:</b> To create a microservice API that can help us understand and track how a particular person’s flight path may be queried. The API should accept a request that includes a list of flights, which are defined by a source and destination airport code. These flights may not be listed in order and will need to be sorted to find the total flight paths starting and ending airports.

<b>Examples:</b>

[['SFO', 'EWR']]                                                 => ['SFO', 'EWR']\
[['ATL', 'EWR'], ['SFO', 'ATL']]                                   => ['SFO', 'EWR']\
[['IND', 'EWR'], ['SFO', 'ATL'], ['GSO', 'IND'], ['ATL', 'GSO']]   => ['SFO', 'EWR']

**microservice API**

1. FASTAPI is used to create a microservice API which accepts the list of flight routes and return the unique flight path of the person.
2. Heroku is used to host the API.

<b>API Deployment link -</b> https://volume-flight-path.herokuapp.com/

<b>Test API:</b>

1. Click on this link - https://volume-flight-path.herokuapp.com/docs to open FASTAPI Swagger page.
2. Next click on the <b>POST</b> (Green Button)
3. Hover the cursor on the <b>"Try it out"</b> and click.
4. Update the response body with the list of flight routes.\
For example:
```
{
  "routes": [
    ["IND", "EWR"], ["SFO", "ATL"], ["GSO", "IND"], ["ATL", "GSO"]
  ]
}
```
5. Finally click on <b>"Execute"</b> and API returns the result in the Response body.

P.S: While submitting the request to the API please use double quotes as mentioned in the example in step 4.