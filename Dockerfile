# Use the official OpenJDK base image
FROM openjdk:17-jdk-alpine

RUN apk add --no-cache bash

# Set the working directory in the container
WORKDIR /app

# Copy the application source code
COPY concert-suggester-backend .

# Build the application with Gradle, specifying the output JAR name
RUN ./gradlew build && mv build/libs/app.jar app.jar


#ENTRYPOINT ["tail", "-f", "/dev/null"]
EXPOSE 8080

CMD ["java", "-jar", "app.jar"]