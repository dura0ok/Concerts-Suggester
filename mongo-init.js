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


userDB.createCollection('logs', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["logType", "timestamp", "message", "serviceType"],
      properties: {
        logType: {
          bsonType: "string",
          description: "Тип лога"
        },
        timestamp: {
          bsonType: "date",
          description: "Временная метка лога"
        },
        message: {
          bsonType: "string",
          description: "Сообщение лога"
        },
        serviceType: {
          bsonType: "string",
          enum: ["bot", "backend", "yandex-music-service", "parser-service"],
          description: "Тип сервиса (enum)"
        }
       
      }
    }
  }
});
