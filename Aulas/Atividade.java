import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

public class Main {
    public static void main(String[] args) {
        LocalDateTime agora = LocalDateTime.now();
        Locale locale = new Locale("pt", "BR");

        String diaSemana = agora.format(DateTimeFormatter.ofPattern("EEEE", locale));
        String dia = agora.format(DateTimeFormatter.ofPattern("dd", locale));
        String mes = agora.format(DateTimeFormatter.ofPattern("MMMM", locale));
        String ano = agora.format(DateTimeFormatter.ofPattern("yyyy", locale));
        String hora = agora.format(DateTimeFormatter.ofPattern("HH", locale));
        String minuto = agora.format(DateTimeFormatter.ofPattern("mm", locale));

        String dataPorExtenso = String.format("Hoje é %s, dia %s de %s de %s e agora são %s horas e %s minutos.", diaSemana, dia, mes, ano, hora, minuto);
        System.out.println(dataPorExtenso);
    }
}
