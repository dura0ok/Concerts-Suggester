FROM openjdk:17-jdk-alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY concert-suggester-backend .

EXPOSE 8080

RUN ./gradlew build

CMD ["java", "-jar", "build/libs/app.jar"]