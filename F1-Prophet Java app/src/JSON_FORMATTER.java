public class JSON_FORMATTER {
    public static String formatJson(String jsonString) {
        if (jsonString == null || jsonString.isBlank()) {
            return "";
        }

        StringBuilder prettyJson = new StringBuilder();
        int indentLevel = 0;
        boolean inQuotes = false;

        for (int i = 0; i < jsonString.length(); i++) {
            char current = jsonString.charAt(i);

            if (current == '"' && (i == 0 || jsonString.charAt(i - 1) != '\\')) {
                inQuotes = !inQuotes;
            }

            if (inQuotes) {
                prettyJson.append(current);
                continue;
            }

            switch (current) {
                case '{':
                case '[':
                    prettyJson.append(current).append("\n");
                    indentLevel++;
                    prettyJson.append("  ".repeat(indentLevel));
                    break;
                case '}':
                case ']':
                    while (prettyJson.length() > 0 && Character.isWhitespace(prettyJson.charAt(prettyJson.length() - 1))) {
                        prettyJson.deleteCharAt(prettyJson.length() - 1);
                    }
                    indentLevel--;
                    prettyJson.append("\n").append("  ".repeat(indentLevel));
                    prettyJson.append(current);
                    break;
                case ',':
                    prettyJson.append(current).append("\n");
                    prettyJson.append("  ".repeat(indentLevel));
                    break;
                case ':':
                    prettyJson.append(current).append(" ");
                    break;
                default:
                    if (!Character.isWhitespace(current)) {
                        prettyJson.append(current);
                    }
                    break;
            }
        }
        return prettyJson.toString();
    }
}