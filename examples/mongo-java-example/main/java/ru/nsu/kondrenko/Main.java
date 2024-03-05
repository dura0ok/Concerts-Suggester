package ru.nsu.kondrenko;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;

public class Main {
    public static void main(String[] args) {
        final String uri = "mongodb://durachok:123321@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=concert-suggester";

        try (MongoClient mongoClient = MongoClients.create(uri)) {
            final MongoDatabase dataBase = mongoClient.getDatabase("concert-suggester");

            for (final var it : dataBase.listCollections()) {
                System.out.println(it);
                System.out.println("\n");
            }
        } catch (Exception exception) {
            System.err.println(exception.getLocalizedMessage());
        }
    }
}
