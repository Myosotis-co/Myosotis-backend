# About DeleteMeHere

In a world where almost every online service requires you to create an account, it's easy to lose track of all the websites and apps you've signed up for. Many of these services offer trial periods and if not monitored closely, one could end up with a long list of unwanted subscriptions or even worse, surprise charges on your credit card.

This is where DeleteMeHere comes in. Our application is designed to empower users to take control of their digital footprint. It offers a simple and efficient way to view and manage all your online accounts in one place.

## Setup

1. Install nvm and Node 18.

```shell
   docker ps
```

2. Clone the project: `git clone https://github.com/ZinnurovArtur/DeleteMeHere.git`

3. `cd` into the directory you checked the project code out into.

4. Start docker and initiate Redis:
   ```shell
   docker compose up --build
   ```
   To verify that the two images are running you can check with:
   ```shell
   docker ps
   ```
   Should look like this:
   ```
   CONTAINER ID     IMAGE
   9d5416dd7273     deletemehere_app
   123304c59a4b     postgres:15
   ```
5. To run the server and see all FastAPI endpoints go to localhost:8008/docs

## Database setup

1.  Install PostgreSQL

2.  Install pgAdmin



# Troubleshooting

### - Unable to connect to PostgreSQL server: SCRAM authentication requires libpq version 10 or above (M1 Mac users).

This issue was fixed in psycopg2 version 2.9.6. Go to requirements.txt and make a local change by updating from 2.9.5. to 2.9.6 and run the docker build:
```shell
   docker compose up --build
   ```