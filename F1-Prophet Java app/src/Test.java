import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Test {
    private static final String API_ENDPOINT_JOLPICA = "https://api.jolpi.ca/ergast/f1/2026/drivers/";
    private static final String API_ENDPOINT_BACKEND = "http://localhost:5000/api/drivers/max_verstappen";

    public static void main(String[] args) {
        try (HttpClient client = HttpClient.newHttpClient()) {

            /*HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(API_ENDPOINT_BACKEND))
                    .POST(HttpRequest.BodyPublishers.ofString("{\"key\":\"value\"}"))
                    .header("Content-Type", "application/json")
                    .build();*/

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(API_ENDPOINT_BACKEND))
                    .GET()
                    .header("Content-Type", "application/json")
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                System.out.println("Status Code: " + response.statusCode());
                String formattedJson = JSON_FORMATTER.formatJson(response.body());
                System.out.println(formattedJson);
            } else {
                System.out.println("Request failed. Status Code: " + response.statusCode());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
