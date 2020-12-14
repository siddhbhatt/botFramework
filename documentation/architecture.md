<h1 align="center">BotFramework Architecture</h1>

## Terms
1. Client - User interacting with the chatbot
2. Channel - Medium of communication with the chatbot. Can be a web-based custom UI integrated to your portal, commonly used chat apps like Slack, Skype, Whatsapp etc or even text messages
3. Channel adapters - Programs (RESTful services) to interact with specific channels
4. Journey - A number of tasks performed by the chatbot towards an unique goal
5. Blocks - Unit task within a Journey
6. Session Manager - Session is a stateful interchange of data between client and chatbot persisted temporarily and Session Manager is responsible for managing all sessions
7. Intent Identification - Identify intent from client input e.g.- messages like "Hi", "Hello", "How are you today?" indicate a greeting message from user
8. Named Entity Resolution (NER) - Identify entity of interest from a client input e.g. - In a message "Show me options in Kolkata" chatbot may be interested in city name of "Kolkata".

## Concept
Any chatbot can be represented as a combination of:
* collection of Journeys where each Journey involves a bunch of Blocks
* Session Manager managing a session between a client and the chatbot app
* Channel adapters to integrate to specific channels

<img src="./images/arc1.png"  width="100%">