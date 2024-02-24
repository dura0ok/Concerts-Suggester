const requiredEnvVariables = ['MONGO_INITDB_ROOT_USERNAME', 'MONGO_INITDB_ROOT_PASSWORD', 'MONGO_INITDB_DATABASE', 'MONGO_APP_USERNAME', 'MONGO_APP_PASSWORD'];

for (const envVar of requiredEnvVariables) {
  if (!process.env[envVar]) {
    print(`Error: Environment variable ${envVar} is not set.`);
    quit();
  }
}


const rootUsername = process.env.MONGO_INITDB_ROOT_USERNAME;
const rootPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;
const dbName = process.env.MONGO_INITDB_DATABASE;
const appUsername = process.env.MONGO_APP_USERNAME;
const appPassword = process.env.MONGO_APP_PASSWORD;


const adminDB = db.getSiblingDB("admin");
adminDB.auth(rootUsername, rootPassword);

const userDB = db.getSiblingDB(dbName);


userDB.createUser({
  user: appUsername,
  pwd: appPassword,
  roles: [
    {
      role: 'readWrite',
      db: dbName
    }
  ]
});


userDB.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["username", "telegram_id", "city_list", "favorite_artists"],
      properties: {
        username: {
          bsonType: "string",
          description: "Имя пользователя"
        },
        telegram_id: {
          bsonType: "string",
          description: "ID в Телеграме"
        },
        city_list: {
          bsonType: "array",
          description: "Список городов"
        },
        yandex_playlist_id: {
          bsonType: "string",
          description: "ID плейлиста в Яндексе"
        },
        favorite_artists: {
          bsonType: "array",
          description: "Список любимых исполнителей"
        }
      }
    }
  }
});

// Создание коллекции "concerts"
userDB.createCollection('concerts', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["artist", "date", "city", "link"],
      properties: {
        artist: {
          bsonType: "string",
          description: "Исполнитель концерта"
        },
        date: {
          bsonType: "date",
          description: "Дата и время концерта"
        },
        city: {
          bsonType: "string",
          description: "Город концерта"
        },
        link: {
          bsonType: "string",
          description: "Ссылка на концерт"
        }
      }
    }
  }
});